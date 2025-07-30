#!/usr/bin/env python3
"""
wds notes:

It looks like there is some .index sidecar file that wids can use, but if it
doesn't exist it creates it in the cache. But it only does this when use_mmap
is False.


Using DDP with WebDataset in pytorch lightning #250

https://github.com/webdataset/webdataset/issues/250
https://discuss.pytorch.org/t/using-ddp-with-webdataset/173035/2
https://github.com/tmbdev-archive/webdataset-lightning/blob/main/train.py
https://github.com/samar-khanna/DiffusionSat/blob/main/train_text_to_image.py
"""
import scriptconfig as scfg
import ubelt as ub
from pathlib import Path
from typing import List, Dict, Any, Tuple
import webdataset as wds
from torch.utils import data as torch_data


__notes__ = r"""


"""


class BuildWebdatasetCLI(scfg.DataConfig):
    """
    Convert to a training-ready structure.

    Note:
        this is not a good format for sharing the dataset as it can be
        redundant and preprocessed.
    """
    in_fpath = scfg.Value(None, help="Input kwcoco file")
    out_dpath = scfg.Value(None, help="The output directory the webdataset shards will be written to.")
    data_config = scfg.Value(None, type=str, help='YAML configuration passed to KWCocoVideoDataset')
    maxcount = scfg.Value(1000, help='max number of samples per shard')
    num_workers = 0

    # param1 = scfg.Value(None, help='param1')

    @classmethod
    def main(cls, argv=1, **kwargs):
        """
        Example:
            >>> # xdoctest: +REQUIRES(module:webdataset)
            >>> import kwcoco
            >>> import ubelt as ub
            >>> import kwcoco_dataloader
            >>> from kwcoco_dataloader.cli.build_webdataset import *  # NOQA
            >>> import numpy as np
            >>> coco_dset = kwcoco_dataloader.coerce_kwcoco(
            >>>     'vidshapes2', num_frames=10, anchors=np.array([[0.1, 0.1]]),
            >>>     num_tracks=3,
            >>> )
            >>> dpath = ub.Path.appdir('kwcoco_dataloader/tests/webdataset/converted_1')
            >>> dpath.delete().ensuredir()
            >>> data_config = {
            >>>     'window_dims': (256, 256),
            >>>     'time_steps': 3,
            >>> }
            >>> kwargs = {
            >>>     'in_fpath': coco_dset.fpath,
            >>>     'out_dpath': dpath,
            >>>     'data_config': data_config,
            >>>     'maxcount': 20,
            >>>     'num_workers': 0,
            >>> }
            >>> argv = 0
            >>> cls = BuildWebdatasetCLI
            >>> config = cls(**kwargs)
            >>> cls.main(argv=argv, **config)

        Ignore:
            import xdev
            xdev.DirectoryWalker(dpath, sort=True).build().write_report()

            dataset = LocalWebdatasetBuckets(dpath)
            self._build()
        """
        import rich
        from rich.markup import escape
        config = cls.cli(argv=argv, data=kwargs, strict=True)
        rich.print('config = ' + escape(ub.urepr(config, nl=1)))
        assert config.out_dpath is not None
        out_dpath = ub.Path(config.out_dpath)

        import kwutil
        import kwcoco
        from kwcoco_dataloader.tasks.fusion.datamodules.kwcoco_dataset import KWCocoVideoDataset

        # The specific weights don't matter here.
        balance_config = None
        balance_config = kwutil.Yaml.coerce(
            '''
            - attribute: contains_annotation
            - attribute: class
            ''')
        balance_attrs = [b['attribute'] for b in balance_config]

        buckets = BucketShardWriter(
            out_dpath, balance_attrs,
            maxcount=config.maxcount
        )

        # If we have a balance config, then for each item we need to determine
        # which "bucket" it falls into. We need to convert that bucket into a
        # string to prefix the shards with.

        data_config = kwutil.Yaml.coerce(config['data_config'])
        if not isinstance(data_config, dict):
            raise TypeError('Bad input config: {data_config!r}')

        coco_dset = kwcoco.CocoDataset.coerce(config.in_fpath)

        # Force simplifications for now.
        data_config['output_type'] = 'homogeneous'

        torch_dataset = KWCocoVideoDataset(coco_dset, mode='test', **data_config)

        torch_loader = torch_dataset.make_loader(batch_size=1, num_workers=config.num_workers,
                                                 shuffle=True)

        from kwutil import util_progress
        pman = util_progress.ProgressManager()

        with pman, buckets:
            prog = pman.progiter(torch_loader, desc='convert batch items', verbose=1)
            iter_ = iter(prog)
            for batch_items in iter_:
                assert len(batch_items) == 1
                batch_item = batch_items[0]
                item = batch_item._frame_collated()

                annot_ids = list(ub.flatten([d['ann_aids'] for d in item['non_collatable']]))
                contains_annotation = len(annot_ids) > 0
                cnames = tuple(sorted(set(coco_dset.annots(annot_ids).cnames)))
                # Construct a superset of what we can consider as balancable.
                balancable_attributes = ub.udict({
                    'contains_annotation': contains_annotation,
                    'class': cnames,
                })
                bucket_key = balancable_attributes.subdict(balance_attrs)
                sample = custom_subset(item)
                buckets.write(sample, bucket_key)


class BucketShardWriter:
    def __init__(
        buckets,
        out_dir: str,
        balance_keys: List[str],
        shard_pattern: str = "%06d.tar",
        maxcount: int = 1000,
    ):
        """
        Args:
            out_dir (str): Base output directory.
            balance_keys (List[str]): Keys used to determine which bucket to write to.
            shard_pattern (str): Pattern for sub-shard filenames.
            maxcount (int): Max number of items per shard.
        """
        import webdataset as wds
        buckets.out_dir = Path(out_dir)
        buckets.balance_keys = balance_keys
        buckets.shard_pattern = shard_pattern
        buckets.maxcount = maxcount
        buckets.bucket_writers: Dict[Tuple[Any, ...], wds.ShardWriter] = {}

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.finalize()

    def _get_bucket_key(buckets, sample: Dict[str, Any]) -> Tuple[Any, ...]:
        """Extracts a tuple of values used to identify a bucket."""
        key = tuple(sample[k] for k in buckets.balance_keys)
        return key

    def _get_or_create_writer(buckets, bucket_key: Dict[str, Any]):
        """Returns an existing writer or creates a new one for this bucket."""
        # import webdataset as wds
        bucket_vals = tuple(bucket_key.values())
        if bucket_vals not in buckets.bucket_writers:
            # Create a new subdirectory path from key
            import kwutil
            dnames = [f'{k}={v}' for k, v in bucket_key.items()]
            dnames = [
                kwutil.util_path.sanitize_path_name(
                    n, replacements={' ': '_'}, safe=True) for n in dnames]
            subdir = buckets.out_dir.joinpath(*dnames)
            subdir.mkdir(parents=True, exist_ok=True)
            # writer = wds.ShardWriter(
            writer = IndexedShardWriter(
                str(subdir / buckets.shard_pattern), maxcount=buckets.maxcount
            )
            buckets.bucket_writers[bucket_vals] = writer
        return buckets.bucket_writers[bucket_vals]

    def write(buckets, sample: Dict[str, Any], bucket_key: Dict[str, Any]):
        """
        Writes a sample to the appropriate shard bucket based on its attribute values.
        """
        # bucket_key = buckets._get_bucket_key(sample)
        writer = buckets._get_or_create_writer(bucket_key)
        writer.write(sample)

    def finalize(buckets):
        """Closes all underlying shard writers."""
        for writer in buckets.bucket_writers.values():
            writer.close()


class IndexedShardWriter(wds.ShardWriter):
    """
    Hacky extension of ShardWriter to also write index sidecars and a summary
    header for a dataset.
    """
    def __init__(self, pattern, maxcount=10000, **kwargs):
        super().__init__(pattern, maxcount=maxcount, **kwargs)
        self._index_fnames = []
        self._index_offsets = []
        self._shardpaths = []
        self._current_tarfile = None
        self._current_fileobj = None

        if 1:
            # Optionally write global summary header that indicates what we are about to do.
            import os
            footer_path = os.path.join(os.path.dirname(self.fname), "__header__.json")
            header_info = {
                "pattern": os.path.basename(self.pattern),
                "maxcount": self.maxcount,
                "maxsize": self.maxsize,
            }
            import json
            with open(footer_path, "w") as f:
                json.dump(header_info, f, indent='    ')
            print(f"[WIDS] Wrote header summary to {footer_path}")

    def next_stream(self):
        print('Next Stream')

        # curr_fname = self.fname
        if self.tarstream is not None:
            self._finish_shard()
            ...
        super().next_stream()

        # Should not need this. We should have enough info to write by ourselves
        # if curr_fname is not None:
        #     # write out index using internal logic
        #     from wids.wids_tar import TarFileReader
        #     TarFileReader(curr_fname)

        # Save tarfile and fileobj references
        self._current_tarfile = self.tarstream.tarstream
        self._current_fileobj = self.tarstream.stream
        self._offsets = []
        self._fnames = []

    def write(self, sample):
        import time
        import tarfile
        import io
        # Pre-track current offset before writing
        # offset = self._current_fileobj.tell()
        # super().write(sample)

        ### ORIG CODE write
        obj = sample
        if (
            self.tarstream is None
            or self.count >= self.maxcount
            or self.size >= self.maxsize
        ):
            self.next_stream()

        if 0:
            size = self.tarstream.write(obj)
        else:
            # Monkey patch
            orig_self = self
            ### start tarstream write
            self = self.tarstream
            total = 0
            obj = self.encoder(obj)
            if "__key__" not in obj:
                raise ValueError("object must contain a __key__")
            for k, v in list(obj.items()):
                if k[0] == "_":
                    continue
                if not isinstance(v, (bytes, bytearray, memoryview)):
                    raise ValueError(
                        f"{k} doesn't map to a bytes after encoding ({type(v)})"
                    )
            key = obj["__key__"]
            for k in sorted(obj.keys()):
                if k == "__key__":
                    continue
                if not self.keep_meta and k[0] == "_":
                    continue
                v = obj[k]
                if isinstance(v, str):
                    v = v.encode("utf-8")
                now = time.time()
                ti = tarfile.TarInfo(key + "." + k)
                ti.size = len(v)
                ti.mtime = self.mtime if getattr(self, 'mtime', None) else now
                ti.mode = self.mode
                ti.uname = self.user
                ti.gname = self.group
                if not isinstance(v, (bytes, bytearray, memoryview)):
                    raise ValueError(f"converter didn't yield bytes: {k}, {type(v)}")
                stream = io.BytesIO(v)

                # Hack in tracking.
                # before = self.tarstream.fileobj.tell()
                self.tarstream.addfile(ti, stream)
                after = self.tarstream.fileobj.tell()
                # tar files are aligned at 512 bytes, so find the nearest
                # bound, which should be the start point.
                before = ((after - ti.size) // 512) * 512

                orig_self._fnames.append(ti.name)
                orig_self._offsets.append([before, ti.size])
                total += ti.size
            size = total
            ### end tarstream write
            self = orig_self

        self.count += 1
        self.total += 1
        self.size += size
        #### END ORIG write

    def _finish_shard(self):
        import json
        # Write index file
        index_path = self.fname + ".index.json"
        index_data = {
            "fnames": self._fnames,
            "index": self._offsets,
        }
        with open(index_path, "w") as f:
            json.dump(index_data, f)
        print(f"[WIDS] Wrote index to {index_path}")

        # Write the index file in pickle format (expected)
        index_path = self.fname + ".index"
        import pickle
        pickle.dumps((self._fnames, self._offsets))

        # Track all index data for summary later (optional)
        import os
        self._shardpaths.append({
            'url': os.path.basename(self.fname),
            'nsamples': self.count,
        })

    def close(self):
        import json
        import os
        if self.tarstream is not None:
            self._finish_shard()
        super().close()
        if self.fname is not None:
            # Optionally write global summary file for all shards
            footer_path = os.path.join(os.path.dirname(self.fname), "__footer__.json")
            footer_info = {
                "pattern": self.pattern,
                "maxcount": self.maxcount,
                "shards": self._shardpaths,
            }
            with open(footer_path, "w") as f:
                json.dump(footer_info, f, indent='    ')
            print(f"[WIDS] Wrote footer summary to {footer_path}")


class LocalWebdataModuleConfig(scfg.DataConfig):
    """
    Arguments for LocalWebdataModule
    """
    train_dataset = scfg.Value(None, help='path to the train shards dpath', group='datasets')
    vali_dataset = scfg.Value(None, help='path to the validation shards dpath', group='datasets', alias=['validation_dataset'])
    test_dataset = scfg.Value(None, help='path to the test shards dpath', group='datasets')

    batch_size = scfg.Value(4, type=int, help=None)

    pin_memory = scfg.Value(True, isflag=True, type=bool, help=ub.paragraph(
        '''
        Can increase speed, but is potentially unstable. For details,
        see https://pytorch.org/docs/stable/data.html#memory-pinning
        '''
    ))

    num_workers = scfg.Value(4, type=str, alias=['workers'], help=ub.paragraph(
            '''
            number of background workers. Can be auto or an avail
            expression.
            '''))

    request_rlimit_nofile = scfg.Value('auto', help=ub.paragraph(
        '''
        As a convinience, on Linux systems this automatically requests that
        ulimit raises the maximum number of open files allowed. Auto currently
        simply sets this to 8192, so use a number higher than this if you run
        into too many open file errors, or set your ulimit explicitly before
        running this software.
        '''), group='resources')

    torch_sharing_strategy = scfg.Value('default', help=ub.paragraph(
            '''
            Torch multiprocessing sharing strategy. Can be 'default',
            "file_descriptor", "file_system". On linux, the default is
            "file_descriptor". See https://pytorch.org/docs/stable/multi
            processing.html#sharing-strategies for descriptions of
            options. When using sqlview=True, using "file_system" can
            help prevent the "received 0 items of ancdata" Error. It is
            unclear why using "file_descriptor" fails in this case for
            some datasets.
            '''), group='resources')

    torch_start_method = scfg.Value('default', help=ub.paragraph(
            '''
            Torch multiprocessing sharing strategy. Can be "default",
            "fork", "spawn", "forkserver". The default method on Linux
            is "spawn".
            '''), group='resources')

    dataset_stats = scfg.Value(None, type=str, help='Need to pass in the dataset stats here')


import pytorch_lightning as pl  # NOQA


class LocalWebdataModule(pl.LightningDataModule):
    __scriptconfig__ = LocalWebdataModuleConfig

    def __init__(self, verbose=1, **kwargs):
        super().__init__()
        self.verbose = verbose
        self.config = self.__scriptconfig__(**kwargs)
        # cfgdict = self.config.to_dict()
        # self.save_hyperparameters(cfgdict)  # Causes name conflict
        self.torch_datasets: Dict[str, LocalWebdatasetBuckets] = {}
        # from kwutil import util_parallel
        # self.num_workers = util_parallel.coerce_num_workers(cfgdict['num_workers'])
        self.did_setup = False

        # HACK because our fit and model needs this for now
        import kwutil
        self.dataset_stats = kwutil.Yaml.coerce(self.config.dataset_stats)
        print(f'DATA: self.dataset_stats = {ub.urepr(self.dataset_stats, nl=1)}')
        print(f'self.dataset_stats={self.dataset_stats}')
        assert self.dataset_stats is not None
        self.predictable_classes = ['dummy1', 'dummy2']

    def setup(self, stage):
        if self.did_setup:
            print('datamodules are already setup. Ignoring extra setup call')
            return

        from kwcoco_dataloader.utils import util_globals
        util_globals.configure_global_attributes(**{
            'num_workers': self.config['num_workers'],
            'torch_sharing_strategy': self.config['torch_sharing_strategy'],
            'torch_start_method': self.config['torch_start_method'],
            'request_rlimit_nofile': self.config['request_rlimit_nofile'],
        })

        if stage in {'fit', 'train'} or stage is None:
            if self.config.train_dataset is not None:
                self.torch_datasets['train'] = LocalWebdatasetBuckets(self.config.train_dataset)
                self.torch_datasets['train']._build()
                # Can we get rid of inject method?
                # Unfortunately lightning seems to only enable / disables
                # validation depending on the methods that are defined, so we are
                # not able to statically define them.
                ub.inject_method(self, lambda self: self._make_dataloader('train', shuffle=True, pin_memory=self.config['pin_memory']), 'train_dataloader')
            if self.config.vali_dataset is not None:
                self.torch_datasets['vali'] = LocalWebdatasetBuckets(self.config.vali_dataset)
                ub.inject_method(self, lambda self: self._make_dataloader('test', shuffle=False, pin_memory=self.config['pin_memory']), 'test_dataloader')

        if stage == 'test' or stage is None:
            raise NotImplementedError

        self.did_setup = True

    @property
    def train_dataset(self):
        return self.torch_datasets.get('train', None)

    @property
    def test_dataset(self):
        return self.torch_datasets.get('test', None)

    @property
    def vali_dataset(self):
        return self.torch_datasets.get('vali', None)

    def _make_dataloader(self, stage, shuffle=False, pin_memory=True):
        """
        If the stage doesn't exist, resturns None.

        Returns:
            torch.utils.data.DataLoader | None
        """
        dataset = self.torch_datasets.get(stage, None)
        if dataset is None:
            return None
        loader = dataset.make_loader(
            batch_size=self.config['batch_size'],
            num_workers=self.config['num_workers'],
            shuffle=shuffle,
            pin_memory=pin_memory,
        )
        return loader


class LocalWebdatasetBuckets(torch_data.Dataset):
    """
    Ignore:
        from kwcoco_dataloader.cli.build_webdataset import *  # NOQA
        self = LocalWebdatasetBuckets(dpath)
        self._build()
        bucket = self.buckets[0]
        print(f'bucket.transformations = {ub.urepr(bucket.transformations, nl=1)}')
        sample = bucket[0]
        print(f'sample = {ub.urepr(sample, nl=1)}')

        sample = self[0]
        print(f'sample = {ub.urepr(sample, nl=1)}')

        print(len(self))
        for index in range(len(self)):
            sample = self[index]
            print(sample['__shard__'], sample['__shardindex__'], sample['__key__'])

        loader = self.make_loader(batch_size=2)
        loader_iter = iter(loader)
        # batch = next(loader_iter)
        batch_ids1 = []
        for batch in loader_iter:
            for sample in batch:
                identifier = (sample['__shard__'], sample['__shardindex__'], sample['__key__'])
                batch_ids1.append(identifier)

        datamodule = LocalWebdataModule(train_dataset=dpath, batch_size=2)
        datamodule.setup('train')
        loader = datamodule.train_dataloader()
        loader_iter = iter(loader)
        # batch = next(loader)
        batch_ids2 = []
        for batch in loader_iter:
            for sample in batch:
                identifier = (sample['__shard__'], sample['__shardindex__'], sample['__key__'])
                batch_ids2.append(identifier)
    """

    def __init__(self, dpath, autobuild=True):
        self.dpath = ub.Path(dpath)
        self.buckets = None
        self.bucket_indexer = None
        if autobuild:
            self._build()

    def __len__(self):
        return len(self.bucket_indexer)

    def __getitem__(self, index):
        outer, inner = self.bucket_indexer.unravel(index)
        bucket = self.buckets[outer]
        sample = bucket[inner]
        return sample

    def make_loader(self, subset=None, batch_size=1, num_workers=0, shuffle=False,
                    pin_memory=False, collate_fn='identity'):
        """
        Use this to make the dataloader so we ensure that we have the right
        worker init function.
        """
        if subset is None:
            dataset = self
        else:
            dataset = subset

        if collate_fn is None:
            collate_fn = ub.identity
        elif isinstance(collate_fn, str):
            if collate_fn == 'identity':
                collate_fn = ub.identity
            elif collate_fn in {'stack', 'torch-default'}:
                import torch.utils.data as torch_data
                collate_fn = torch_data.dataloader.default_collate
            else:
                raise KeyError(collate_fn)

        import torch
        loader = torch.utils.data.DataLoader(
            dataset, batch_size=batch_size, num_workers=num_workers,
            shuffle=shuffle, pin_memory=pin_memory,
            # worker_init_fn=worker_init_fn,
            collate_fn=collate_fn,
        )
        return loader

    def _build(self):
        import kwutil
        import wids
        import os
        headers = list(self.dpath.glob('**/__header__.json'))
        footers = list(self.dpath.glob('**/__footer__.json'))
        assert len(headers) == len(footers), 'write was not complete'

        if 1:
            # from wids.wids_decode import decode_basic
            # Attempt ShardListDataset, these buckets are indexable
            buckets = []
            for footer_path in footers:
                shard_infos = kwutil.Json.load(footer_path)['shards']
                wids_paths = [ub.udict(d) | {'url': str(footer_path.parent / os.path.basename(d['url']))} for d in shard_infos]
                # test wids stuff
                # wids_paths = [{'url': p, 'nsamples': 1000} for p in sorted(paths)]
                # cache_dir = ub.Path('./tmp-cache').ensuredir()

                cache_dir = footer_path.parent  # set cache to be the local dir
                transformations = [
                    our_decode_basic,
                ]
                wids_bucket = wids.ShardListDataset(
                    wids_paths,
                    cache_dir=str(cache_dir),
                    transformations=transformations,
                )
                buckets.append(wids_bucket)

            import kwarray
            self.buckets = buckets
            self.bucket_indexer = kwarray.FlatIndexer(list(map(len, buckets)))
        else:
            # Attempt WebDataset, these buckets are not indexable
            buckets = []
            for footer_path in footers:
                shard_footer = kwutil.Json.load(footer_path)
                shard_infos = shard_footer['shards']
                total_samples = sum(d['nsamples'] for d in shard_infos)
                wds_paths = sorted([str(footer_path.parent / os.path.basename(d['url'])) for d in shard_infos])
                wds_bucket = wds.WebDataset(wds_paths)
                wds_bucket.with_length(total_samples)
                buckets.append(wds_bucket)

            if 0:
                from collections import Counter
                seen_keys1 = Counter()
                for bucket in buckets:
                    for item in bucket.iterator():
                        seen_keys1[item['__key__']] += 1

                maxlen = max(map(len, buckets))
                buckets2 = [b.repeat(nbatches=maxlen) for b in buckets]
                combo2 = wds.RandomMix(buckets2, probs=[1 / len(buckets) for b in buckets])
                seen_keys2 = Counter()
                for item in combo2:
                    seen_keys2[item['__key__']] += 1

                combo3 = wds.RandomMix(buckets, probs=[1 / len(buckets) for b in buckets], longest=True)
                seen_keys3 = Counter()
                for item in combo3:
                    seen_keys3[item['__key__']] += 1

                print(len(seen_keys1))
                print(len(seen_keys2))
                print(len(seen_keys3))

        # for b in buckets:
        #     print(len(b))
        #     # wids_bucket[0]
        #     # for idx, item in ub.ProgIter(enumerate(wids_bucket)):
        #     #     ...
        #     # max_idx = idx + 1
        #     # print(f'max_idx={max_idx}')

        # if 0:
        #     buckets = []
        #     for shards in leaf_shards:
        #         # .to_tuple("jpg", "json")
        #         # .map_tuple(ToTensor(), lambda meta: meta)
        #         paths = [str(s) for s in shards]
        #         bucket = wds.WebDataset(paths)
        #         bucket = bucket.decode()
        #         # bucket.decode('pyd')
        #         item = next(bucket.iterator1())
        #         print(f'item = {ub.urepr(item, nl=1)}')
        #         buckets.append(bucket)


def our_decode_basic(sample: Dict[str, Any], format=True):
    """
    Hacked version of decode_basic for pyd and npz suppot
    """
    from wids.wids_decode import check_keys
    import io
    import numpy as np

    check_keys(sample)

    for key, stream in sample.items():
        if key.startswith("__"):
            continue
        extensions = key.split(".")
        if len(extensions) == 1:
            continue
        extension = extensions[-1].lower()
        if isinstance(stream, bytes):
            stream = io.BytesIO(stream)
        if extension in ["gz"] and len(extensions) >= 2:
            # we're assuming that .gz extensions are already decoded
            extension = extensions[-2].lower()
        if extension in ["txt", "text"]:
            value = stream.read()
            sample[key] = value.decode("utf-8")
        elif extension in ["cls", "cls2"]:
            value = stream.read()
            sample[key] = int(value.decode("utf-8"))
        elif extension == "safetensors":
            import safetensors.torch

            sample[key] = safetensors.torch.load_file(stream)
        elif extension == "json":
            import json

            value = stream.read()
            sample[key] = json.loads(value)
        elif extension == "npy":
            sample[key] = np.load(stream)
        elif extension == "npz":
            import numpy.lib.format  # noqa
            sample[key] = dict(np.load(stream))
        elif extension == "mp":
            import msgpack

            value = stream.read()
            sample[key] = msgpack.unpackb(value, raw=False)
        elif extension in ["pt", "pth"]:
            import torch

            sample[key] = torch.load(stream)
        elif extension in ["pickle", "pkl", "pyd"]:
            import pickle

            sample[key] = pickle.load(stream)

    check_keys(sample)

    return sample


def custom_subset(item):
    USE_SUBSET = 1
    if USE_SUBSET:
        # Which subset is right?
        collated_subkeys = {
            'imdata_tchw',
            'saliency',
            'saliency_weights',
        }
        import kwarray
        collated_subdict = ub.udict.intersection(item['collated'], collated_subkeys)
        collated_subdict = ub.udict.map_values(collated_subdict, kwarray.ArrayAPI.numpy)
        # NOTE:
        # webdataset wants pyd for pickle, but wids decode_basic wants pkl
        # We will make a custom decode i guess.
        sample = {
            '__key__': str(item['meta']['resolved_index']),
            'meta.pyd': item['meta'],
            'collated.npz': collated_subdict,
            'non_collatable.pyd': item['non_collatable'],
        }
    else:
        sample = {
            '__key__': str(item['meta']['resolved_index']),
            'meta.pyd': item['meta'],
            'collated.pyd': item['collated'],
            'non_collatable.pyd': item['non_collatable'],
        }
    return sample


def to_test():
    """
        kernprof -lrvp wids webdataset -m xdoctest -m kwcoco_dataloader.cli.build_webdataset to_test
    """
    # xdoctest: +REQUIRES(module:webdataset)
    import numpy as np
    import ubelt as ub
    import kwcoco_dataloader
    from kwcoco_dataloader.cli.build_webdataset import BuildWebdatasetCLI
    out_dpath = ub.Path.appdir('kwcoco_dataloader/tests/webdataset/converted_2')

    if 1:
        coco_dset = kwcoco_dataloader.coerce_kwcoco(
            'vidshapes2', num_frames=10, anchors=np.array([[0.1, 0.1]]),
            num_tracks=3,
        )
        out_dpath.delete().ensuredir()
        data_config = {
            'window_dims': (256, 256),
            'time_steps': 3,
        }
        kwargs = {
            'in_fpath': coco_dset.fpath,
            'out_dpath': out_dpath,
            'data_config': data_config,
        }
        argv = 0
        cls = BuildWebdatasetCLI
        config = BuildWebdatasetCLI(**kwargs)
        cls.main(argv=argv, **config)

    import webdataset as wds
    leaf_shards = []
    shard_footers = []
    for r, ds, fs in out_dpath.walk():
        if len(ds) == 0 and len(fs):
            for f in fs:
                if f == '__footer__.json':
                    shard_footers.append(r / f)
            shards = [r / f for f in fs]
            leaf_shards.append(shards)

    buckets = []
    for shards in leaf_shards:
        # .to_tuple("jpg", "json")
        # .map_tuple(ToTensor(), lambda meta: meta)
        paths = [str(s) for s in shards]

    buckets = []
    import wids
    import os
    if 0:
        for shards in leaf_shards:
            # .to_tuple("jpg", "json")
            # .map_tuple(ToTensor(), lambda meta: meta)
            paths = [str(s) for s in shards]
            bucket = wds.WebDataset(paths, shardshuffle=True)
            bucket = bucket.shuffle(100).decode()
            buckets.append(bucket)

    import kwutil
    for footer_path in shard_footers:
        shard_infos = kwutil.Json.load(footer_path)['shards']
        wids_paths = [(ub.udict(d)) | {'url': str(footer_path.parent / os.path.basename(d['url']))} for d in shard_infos]
        # test wids stuff
        # wids_paths = [{'url': p, 'nsamples': 1000} for p in sorted(paths)]
        # cache_dir = ub.Path('./tmp-cache').ensuredir()

        cache_dir = footer_path.parent  # set cache to be the local dir
        os.environ['WIDS_VERBOSE'] = '1'
        wids_bucket = wids.ShardListDataset(
            wids_paths,
            cache_dir=str(cache_dir),
            transformations=lambda x: x,
        )
        wids_bucket[0]
        for idx, item in ub.ProgIter(enumerate(wids_bucket)):
            ...
        max_idx = idx + 1
        print(f'max_idx={max_idx}')


def quickcheck(out_dpath):
    import webdataset as wds
    leaf_shards = []
    for r, ds, fs in out_dpath.walk():
        if len(ds) == 0 and len(fs):
            shards = [r / f for f in fs]
            leaf_shards.append(shards)

    buckets = []
    for shards in leaf_shards:
        # .to_tuple("jpg", "json")
        # .map_tuple(ToTensor(), lambda meta: meta)
        paths = [str(s) for s in shards]
        bucket = wds.WebDataset(paths)
        bucket = bucket.decode()
        # bucket.decode('pyd')

        item = next(bucket.iterator1())
        print(f'item = {ub.urepr(item, nl=1)}')
        buckets.append(bucket)

    # It looks like you can mix RandomMix datasets.
    ds1, ds2, ds3, ds4, *_ = buckets
    ub.peek(ds1.iterator())
    dsA = wds.RandomMix([ds1, ds2], probs=[0.1, 0.9])
    dsB = wds.RandomMix([ds2, ds4], probs=[0.1, 0.9])
    ds = wds.RandomMix([dsA, dsB], probs=[0.1, 0.9])

    _iter = iter(ds)
    for item in _iter:
        print(item['__key__'])
        ...

    ub.peek(ds.iterator())

    # Try wids
    import wids
    wids.ShardListDataset


def infer_shard_pattern_printf(tar_fnames):
    """
    References:
        https://chat.deepseek.com/a/chat/s/5bb89bac-30e8-48fc-bdba-85adaad6ad2a
    """
    import re
    if not tar_fnames:
        return ""

    # Extract prefix, numeric part, and extension using regex
    pattern = re.compile(r'^([^\d]*)(\d+)\.([a-zA-Z0-9]+)$')
    matches = [pattern.match(fname) for fname in tar_fnames]

    if not all(matches):
        # Fallback: Just use the extension (no numeric pattern)
        return f"%s.{tar_fnames[0].split('.')[-1]}"  # %s for arbitrary prefix

    prefixes = [m.group(1) for m in matches]
    padding = len(matches[0].group(2))
    ext = matches[0].group(3)

    # Check if all prefixes are the same
    if len(set(prefixes)) == 1:
        return f"{prefixes[0]}%0{padding}d.{ext}"

    # Fallback: Generic pattern if prefixes differ
    return f"%s%0{padding}d.{ext}"  # %s for arbitrary prefix


def reindex(shard_dpath):
    """
    Update the index structure of a folder of shards.

    This will attempt to write any missing header / footer / sidecar
    information in a directory of tar files.

    TODO:
        This needs to be a tool that can be independently run over a shard dir.

    Ignore:
        # developer hacks for running this over nested shard directories.

        import webdataset as wds
        leaf_shards = []
        shard_footers = []
        for r, ds, fs in out_dpath.walk():
            if len(ds) == 0 and len(fs):
                for f in fs:
                    if f == '__footer__.json':
                        shard_footers.append(r / f)
                shards = [r / f for f in fs]
                leaf_shards.append(shards)
    """
    from wids.wids_tar import TarFileReader
    import os
    import kwutil
    tar_fpaths = sorted(shard_dpath.glob('*.tar'))

    header_fpath = shard_dpath / '__header__.json'
    footer_fpath = shard_dpath / '__footer__.json'

    tar_fnames = [p.name for p in tar_fpaths]
    pattern = infer_shard_pattern_printf(tar_fnames)

    if footer_fpath.exists():
        footer_info = kwutil.Json.coerce(footer_fpath)
    else:
        footer_info = {
            'pattern': pattern,
            'shards': [],
        }

    if header_fpath.exists():
        header_info = kwutil.Json.coerce(header_fpath)
    else:
        header_info = {
            "pattern": pattern,
            # "maxcount": self.maxcount,
            # "maxsize": self.maxsize,
        }

    shard_infos = []
    for tar_fpath in ub.ProgIter(tar_fpaths, desc='write tar indexes'):
        # Write the pickle index data structure
        tar_reader = TarFileReader(os.fspath(tar_fpath))
        tar_fnames = tar_reader.fnames
        tar_keys = list(ub.unique([n.split('.', 1)[0] for n in tar_fnames]))
        shard_infos.append({
            'url': tar_fpath.name,
            'nsamples': len(tar_keys)
        })

    # Infer the maximum number of items that can be in a tar shard
    new_maxcount = max(d['nsamples'] for d in shard_infos)

    old_maxcount = header_info.get('maxcount', 0)
    if old_maxcount < new_maxcount:
        header_info['maxcount'] = new_maxcount

    old_maxcount = footer_info.get('maxcount', 0)
    if old_maxcount < new_maxcount:
        footer_info['maxcount'] = new_maxcount

    footer_info['shards'] = shard_infos

    footer_fpath.write_text(kwutil.Json.dumps(footer_info))
    header_fpath.write_text(kwutil.Json.dumps(header_info))


__cli__ = BuildWebdatasetCLI

if __name__ == '__main__':
    """

    CommandLine:
        python ~/code/kwcoco_dataloader/kwcoco_dataloader/cli/build_webdataset.py
        python -m kwcoco_dataloader.cli.build_webdataset
    """
    __cli__.main()
