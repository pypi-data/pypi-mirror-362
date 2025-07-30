"""
Adds fields needed by ndsampler to correctly "watch" a region.

Some of this is done hueristically. We assume images come from certain sensors.
We assume input is orthorectified.  We assume some GSD "target" gsd for video
and image processing. Note a video GSD will typically be much higher (i.e.
lower resolution) than an image GSD.
"""
import warnings
import numpy as np
import ubelt as ub
import kwimage
import numbers
import kwcoco

from os.path import join
from kwcoco_dataloader.utils import util_raster
from kwcoco_dataloader import exceptions


def filter_image_ids(coco_dset, gids=None, include_sensors=None,
                     exclude_sensors=None, select_images=None,
                     select_videos=None):
    """
    Filters to a specific set of images given query parameters
    """
    def coerce_set(x):
        return set(x.split(',')) if isinstance(x, str) else set(x)

    def filter_by_attribute(table, key, include, exclude):
        if include is not None or exclude is not None:
            if include is not None:
                include = coerce_set(include)
            if exclude is not None:
                exclude = coerce_set(exclude)
            values = table.lookup(key, default=None)
            if include is None:
                flags = [v not in exclude for v in values]
            elif exclude is None:
                flags = [v in include for v in values]
            else:
                flags = [v in include and v not in exclude for v in values]
            table = table.compress(flags)
        return table
    valid_images = coco_dset.images(gids)
    valid_images = filter_by_attribute(
        valid_images, 'sensor_coarse', include_sensors, exclude_sensors)
    valid_gids = set(valid_images)

    if select_images is not None:
        try:
            import jq
        except Exception:
            print('The jq library is required to run a generic image query')
            raise

        try:
            query_text = ".images[] | select({}) | .id".format(select_images)
            query = jq.compile(query_text)
            image_selected_gids = set(query.input(coco_dset.dataset).all())
            valid_gids &= image_selected_gids
        except Exception as ex:
            print('JQ Query Failed: {}, ex={}'.format(query_text, ex))
            raise

    if select_videos is not None:

        if isinstance(select_videos, list):
            # Interpret as video_ids
            ...
        else:
            try:
                import jq
            except Exception:
                print('The jq library is required to run a generic image query')
                raise

            try:
                query_text = ".videos[] | select({}) | .id".format(select_videos)
                query = jq.compile(query_text)
                selected_vidids = query.input(coco_dset.dataset).all()
                vid_selected_gids = set(ub.flatten(coco_dset.index.vidid_to_gids[vidid]
                                                   for vidid in selected_vidids))
                valid_gids &= vid_selected_gids
            except Exception:
                print('JQ Query Failed: {}'.format(query_text))
                raise

    valid_gids = sorted(valid_gids)
    return valid_gids


def populate_watch_fields(
    coco_dset,
    target_gsd=10.0,
    vidids=None,
    overwrite=False,
    default_gsd=None,
    conform=True,
    enable_video_stats=True,
    enable_valid_region=False,
    enable_intensity_stats=False,
    workers=0,
    mode='thread',
    remove_broken=False,
    skip_populate_errors=False,
):
    """
    Aggregate populate function for fields useful to GeoWATCH.

    Args:
        coco_dset (Dataset): dataset to work with

        target_gsd (float): target gsd in meters

        overwrite (bool | List[str]):
            if True or False overwrites everything or nothing. Otherwise it can
            be a list of strings indicating what is
            overwritten. Valid keys are warp, band, and channels.

        default_gsd (None | float):
            if specified, assumed any images without geo-metadata have this
            GSD'

    Ignore:
        >>> # xdoctest: +REQUIRES(env:DVC_DPATH)
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> dvc_dpath = kwcoco_dataloader.utils.util_data.find_dvc_dpath()
        >>> fpath = dvc_dpath / 'drop0_aligned/data.kwcoco.json')
        >>> coco_dset = kwcoco.CocoDataset(fpath)
        >>> target_gsd = 5.0
        >>> populate_watch_fields(coco_dset, target_gsd)
        >>> print('coco_dset.index.videos = {}'.format(ub.urepr(coco_dset.index.videos, nl=-1)))
        >>> print('coco_dset.index.imgs[1] = ' + ub.urepr(coco_dset.index.imgs[1], nl=1))

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> # TODO: make a demo dataset with some sort of gsd metadata
        >>> coco_dset = kwcoco.CocoDataset.demo('vidshapes8-multispectral')
        >>> print('coco_dset = {!r}'.format(coco_dset))
        >>> target_gsd = 13.0
        >>> populate_watch_fields(coco_dset, target_gsd, default_gsd=1)
        >>> print('coco_dset.index.imgs[1] = ' + ub.urepr(coco_dset.index.imgs[1], nl=2))
        >>> print('coco_dset.index.videos = {}'.format(ub.urepr(coco_dset.index.videos, nl=1)))

        >>> # TODO: make a demo dataset with some sort of gsd metadata
        >>> coco_dset = kwcoco.CocoDataset.demo('vidshapes8')
        >>> print('coco_dset = {!r}'.format(coco_dset))
        >>> target_gsd = 13.0
        >>> populate_watch_fields(coco_dset, target_gsd, default_gsd=1)
        >>> print('coco_dset.index.imgs[1] = ' + ub.urepr(coco_dset.index.imgs[1], nl=2))
        >>> print('coco_dset.index.videos = {}'.format(ub.urepr(coco_dset.index.videos, nl=1)))
    """
    # Load your KW-COCO dataset (conform populates information like image size)
    if conform:
        # Note: we will handle imgsize in a later part
        coco_dset.conform(pycocotools_info=False, workers=workers,
                          ensure_imgsize=False)

    if 1:
        from kwcoco_dataloader import heuristics
        heuristics.register_known_fsspec_s3_buckets()

    if vidids is None:
        vidids = list(coco_dset.index.videos.keys())
        gids = list(coco_dset.index.imgs.keys())
    else:
        gids = list(ub.flatten(coco_dset.images(video_id=video_id) for video_id in vidids))

    coco_populate_geo_heuristics(
        coco_dset, gids=gids, overwrite=overwrite, default_gsd=default_gsd,
        workers=workers, mode=mode,
        enable_intensity_stats=enable_intensity_stats,
        enable_valid_region=enable_valid_region,
        remove_broken=remove_broken,
        skip_populate_errors=skip_populate_errors,
    )

    # Modify videos to include cleared status
    if 1:
        from kwcoco_dataloader import heuristics
        from kwutil import util_pattern
        region_id_to_cleared = {d['region_id']: d['cleared'] for d in heuristics.REGION_STATUS}
        pat = util_pattern.Pattern.coerce(r'\w+_R\d+(_\d+)?', 'regex')
        for video in coco_dset.videos().objs:
            video_name = video['name']
            if pat.match(video_name):
                region_id = '_'.join(video_name.split('_')[0:2])
                cleared = region_id_to_cleared.get(region_id, False)
                video['cleared'] = cleared
                video['domain'] = region_id

    if enable_video_stats:
        for video_id in ub.ProgIter(vidids, total=len(vidids), desc='populate videos'):
            coco_populate_geo_video_stats(coco_dset, video_id, target_gsd=target_gsd)

    # serialize intermediate objects
    coco_dset._ensure_json_serializable()


def coco_populate_geo_heuristics(coco_dset: kwcoco.CocoDataset,
                                 gids=None,
                                 overwrite=False,
                                 default_gsd=None,
                                 workers=0,
                                 mode='thread',
                                 remove_broken=False, **kw):
    """
    Example:
        >>> # xdoctest: +REQUIRES(env:DVC_DPATH)
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> from kwcoco_dataloader.utils.util_data import find_dvc_dpath
        >>> import kwcoco
        >>> dvc_dpath = find_dvc_dpath()
        >>> coco_fpath = dvc_dpath / 'drop1-S2-L8-aligned/data.kwcoco.json'
        >>> coco_dset = kwcoco.CocoDataset(coco_fpath)
        >>> coco_populate_geo_heuristics(coco_dset, overwrite=True, workers=12,
        >>>                              keep_geotiff_metadata=False,
        >>>                              mode='process')

    Example:
        >>> # xdoctest: +REQUIRES(env:DVC_DPATH)
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> from kwcoco_dataloader.utils.util_data import find_dvc_dpath
        >>> import kwcoco
        >>> dvc_dpath = find_dvc_dpath()
        >>> coco_fpath = dvc_dpath / 'drop1-S2-L8-aligned/data.kwcoco.json'
        >>> coco_dset = kwcoco.CocoDataset(coco_fpath)
        >>> coco_populate_geo_heuristics(coco_dset, overwrite=True, workers=12,
        >>>                              keep_geotiff_metadata=False,
        >>>                              mode='process')
    """
    import rich
    gids = coco_dset.images(gids)._ids
    # Cant multiprocess because of SwigPyObjects... bleh
    # keep_geotiff_metadata must be False to use mode=process
    keep_geotiff_metadata = kw.get('keep_geotiff_metadata', False)
    if keep_geotiff_metadata and mode == 'process':
        raise NotImplementedError(ub.paragraph(
            '''
            Cannot keep keep geotiff metadata when using process parallelism.

            Need to serialize gdal objects (i.e. RPC transforms and
            SwigPyObject) returned from ``kwgis.gis.geotiff.geotiff_metadata``
            to be able do this.
            '''))

    jobs = ub.JobPool(mode, max_workers=workers, transient=True)
    for gid in ub.ProgIter(gids, desc='submit populate imgs'):
        coco_img = coco_dset.coco_image(gid)
        if mode == 'process':
            coco_img = coco_img.detach()

        job_args = (coco_img,)
        job_kwargs = dict(overwrite=overwrite, default_gsd=default_gsd, **kw)
        job = jobs.submit(coco_populate_geo_img_heuristics2,
                          *job_args, **job_kwargs)
        if 0:
            # For debugging
            job.job_func = coco_populate_geo_img_heuristics2
            job.job_args = job_args
            job.job_kwargs = job_kwargs
        job.gid = gid

    broken_image_ids = []
    working_image_ids = []
    for job in ub.ProgIter(jobs.as_completed(), total=len(jobs), desc='collect populate imgs'):
        gid = job.gid
        try:
            img = job.result()
        except Exception as ex:
            # Check for known error messages that might cause errors grabbing
            # data
            known_errors = {}
            known_errors['has_404'] = remove_broken and "404" in repr(ex)
            known_errors['has_acc_problem'] = "not recognized as a supported file format" in repr(ex)
            known_errors['connection_reset'] = "Connection reset by peer" in repr(ex)
            known_errors['failed_to_read'] = 'Failed to read' in repr(ex)

            print('')
            print(f'known_errors = {ub.urepr(known_errors, nl=1)}')
            if any(known_errors.values()):
                broken_image_ids.append(gid)
                print('')
                rich.print('[yellow]WARNING: KNOWN ERROR IN GEO HEURISTICS')
                print(f'ex={ex!r}')
                print(f'ex={ex}')
                print(f'ex.__dict__={ex.__dict__}')
                print('num_broken = {}'.format(len(broken_image_ids)))
                print('num_working = {}'.format(len(working_image_ids)))
                rich.print('[yellow]WARNING: KNOWN ERROR IN GEO HEURISTICS')
            else:
                coco_img = coco_dset.coco_image(gid)

                # Check for remote existence and handle the case where the data
                # might be at a remote location
                from kwcoco_dataloader.utils import util_fsspec
                missing_paths = []
                existing_paths = []
                forbidden_paths = []

                HACK_CHECK_EXISTS = 1
                if HACK_CHECK_EXISTS:
                    """
                    NOTE:
                        For L2 data, we need to assume the user called

                        from kwcoco_dataloader import heuristics
                        heuristics.register_known_fsspec_s3_buckets()

                        And populated the appropriate mapping from s3-bucket to
                        s3 configurations.
                    """
                    for p in coco_img.iter_image_filepaths():
                        # Use fsspec to check if the files exist
                        fspath = util_fsspec.FSPath.coerce(p)
                        try:
                            if not fspath.exists():
                                missing_paths.append(fspath)
                            else:
                                existing_paths.append(fspath)
                        except PermissionError:
                            forbidden_paths.append(fspath)

                if missing_paths or forbidden_paths:
                    broken_image_ids.append(gid)
                    print('')
                    rich.print('[yellow]WARNING: OTHER ERROR IN GEO HEURISTICS')
                    print(f'existing_paths = {ub.urepr(existing_paths, nl=1)}')
                    print(f'missing_paths = {ub.urepr(missing_paths, nl=1)}')
                    print(f'forbidden_paths = {ub.urepr(forbidden_paths, nl=1)}')
                    print(f'ex={ex!r}')
                    print(f'ex={ex}')
                    print(f'ex.__dict__={ex.__dict__}')
                    print('coco_img = {}'.format(ub.urepr(coco_img.img, nl=3)))
                    print('num_broken = {}'.format(len(broken_image_ids)))
                    print('num_working = {}'.format(len(working_image_ids)))
                    rich.print('[yellow]WARNING: OTHER ERROR IN GEO HEURISTICS')
                    print('')
                    # raise FileNotFoundError(str(missing_paths))
                else:
                    print('')
                    rich.print('[red]ERROR: UNKNOWN ERROR IN GEO HEURISTICS')
                    print(f'ex={ex!r}')
                    print(f'ex={ex}')
                    print(f'ex.__dict__={ex.__dict__}')
                    print('coco_img = {}'.format(ub.urepr(coco_img.img, nl=3)))
                    print('num_broken = {}'.format(len(broken_image_ids)))
                    print('num_working = {}'.format(len(working_image_ids)))
                    rich.print('[red]ERROR: UNKNOWN ERROR IN GEO HEURISTICS')
                    print('')
                    # if 0:
                    #     job.job_args
                    #     job.job_kwargs
                    #     coco_img, = job.job_args
                    #     globals().update(**job.job_kwargs)
                    #     # result = coco_populate_geo_img_heuristics2(*job.job_args, **job.job_kwargs)
                    raise
        else:
            working_image_ids.append(gid)
            if mode == 'process':
                # for multiprocessing
                real_img = coco_dset.index.imgs[gid]
                real_img.update(img)
    if broken_image_ids:
        print(f'There were {len(broken_image_ids)} / {len(gids)} broken images')
        coco_dset.remove_images(broken_image_ids, verbose=True)


def coco_populate_geo_img_heuristics2(
    coco_img,
    overwrite=False,
    default_gsd=None,
    keep_geotiff_metadata=False,
    enable_intensity_stats=False,
    enable_valid_region=False,
    skip_populate_errors=False,
):
    """
    Note: this will not overwrite existing channel info unless specified

    Commandline
        xdoctest -m ~/code/watch/kwcoco_dataloader/utils/kwcoco_extensions.py --profile

    TODO:
        - [ ] Use logic in the align demo classmethod to make an example
              that uses a real L8 / S2 image.

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco_dataloader
        >>> import json
        >>> coco_dset = kwcoco_dataloader.coerce_kwcoco('kwcoco_dataloader-msi-geodata-dates-heatmap-videos1-frames2-gsize64')
        >>> gid = 1
        >>> overwrite = {'warp', 'band'}
        >>> default_gsd = None
        >>> kw = {}
        >>> coco_img = coco_dset.coco_image(gid)
        >>> before_img_attrs = list(coco_img.img.keys())
        >>> before_aux_attr_hist = ub.dict_hist(ub.flatten([list(aux) for aux in coco_img.img['auxiliary']]))
        >>> print('before_img_attrs = {!r}'.format(before_img_attrs))
        >>> print('before_aux_attr_hist = {}'.format(ub.urepr(before_aux_attr_hist, nl=1)))
        >>> coco_populate_geo_img_heuristics2(coco_img)
        >>> img = coco_dset.index.imgs[gid]
        >>> after_img_attrs = list(coco_img.img.keys())
        >>> after_aux_attr_hist = ub.dict_hist(ub.flatten([list(aux) for aux in coco_img.img['auxiliary']]))
        >>> new_img_attrs = set(after_img_attrs) - set(before_img_attrs)
        >>> new_aux_attrs = {k: after_aux_attr_hist[k] - before_aux_attr_hist.get(k, 0) for k in after_aux_attr_hist}
        >>> new_aux_attrs = {k: v for k, v in new_aux_attrs.items() if v > 0}
        >>> print('new_img_attrs = {}'.format(ub.urepr(new_img_attrs, nl=1)))
        >>> print('new_aux_attrs = {}'.format(ub.urepr(new_aux_attrs, nl=1)))
        >>> #print('after_img_attrs = {}'.format(ub.urepr(after_img_attrs, nl=1)))
        >>> #print('after_aux_attr_hist = {}'.format(ub.urepr(after_aux_attr_hist, nl=1)))
        >>> assert 'geos_corners' in img
        >>> #assert 'default_nodata' in img
        >>> #assert 'default_nodata' in new_aux_attrs
        >>> print(ub.varied_values(list(map(lambda x: ub.map_vals(json.dumps, x), coco_img.img['auxiliary'])), default=None))

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> ###
        >>> gid = 1
        >>> dset = kwcoco.CocoDataset.demo('vidshapes8-multispectral')
        >>> coco_img = dset.coco_image(gid)
        >>> coco_populate_geo_img_heuristics2(coco_img, overwrite=True)
        >>> ###
        >>> gid = 1
        >>> dset2 = kwcoco.CocoDataset.demo('shapes8')
        >>> coco_img = dset2.coco_image(gid)
        >>> coco_populate_geo_img_heuristics2(coco_img, overwrite=True)
    """
    from kwgis.gis.geotiff import geotiff_metadata
    bundle_dpath = coco_img.bundle_dpath
    img = coco_img.img

    primary_obj = coco_img.primary_asset()
    asset_objs = list(coco_img.iter_asset_objs())

    overwrite = _coerce_overwrite(overwrite)

    # Note: for non-geotiffs we could use the aux_to_img transformation
    # provided with them to determine their geo-properties.
    asset_errors = []
    for obj in asset_objs:
        try:
            errors = _populate_canvas_obj(
                bundle_dpath, obj, overwrite=overwrite, default_gsd=default_gsd,
                keep_geotiff_metadata=keep_geotiff_metadata,
                enable_intensity_stats=enable_intensity_stats)
            asset_errors.append(errors)
        except Exception as ex:
            if skip_populate_errors:
                asset_errors.append(str(ex))
            else:
                raise

    if all(asset_errors):
        info = ub.dict_isect(img, {'name', 'file_name', 'id'})
        warnings.warn(f'img {info} has issues introspecting')

    if keep_geotiff_metadata:
        info = primary_obj.get('geotiff_metadata', None)
        if info is None:
            dem_hint = primary_obj.get('dem_hint', 'use')
            metakw = {}
            if dem_hint == 'ignore':
                metakw['elevation'] = 0
            primary_fname = primary_obj.get('file_name', None)
            primary_fpath = join(bundle_dpath, primary_fname)
            info = geotiff_metadata(primary_fpath, **metakw)
            primary_obj['geotiff_metadata'] = info

    # if 'default_nodata' not in img:
    #     img['default_nodata'] = primary_obj['default_nodata']
    if overwrite:
        # Update image space to correspond to one of the assets
        # (typically the one with the largest size)
        if img.get('file_name', None) is None:
            assets = list(coco_img.assets)
            asset_dsizes = [
                (asset['width'], asset['height'])
                for asset in assets
                if ("width" in asset) and ("height" in asset)
            ]
            idx = ub.argmax(asset_dsizes)
            main_asset = assets[idx]

            img['width'] = main_asset['width']
            img['height'] = main_asset['height']

            if 'warp_to_wld' in main_asset:
                # Also update world information (does the image need this?)
                img['wld_to_pxl'] = kwimage.Affine.coerce(main_asset['warp_to_wld']).inv().concise()
                img['wld_crs_info'] = main_asset['wld_crs_info']
            else:
                img.pop('wld_to_pxl', None)
                img.pop('wld_crs_info', None)

            _recompute_auxiliary_transforms(img)

    if ('width' not in img or 'height' not in img):
        # or overwrite:
        # TODO: better test to see if we need to recompute auxiliary transforms
        _recompute_auxiliary_transforms(img)

    valid_region_utm = img.get('valid_region_utm', None)
    if enable_valid_region and (valid_region_utm is None or 'warp' in overwrite):
        _populate_valid_region(coco_img)

    if keep_geotiff_metadata:
        img['geotiff_metadata'] = primary_obj['geotiff_metadata']

    if 'date_captured' in img:
        from kwutil import util_time
        img['timestamp'] = util_time.coerce_datetime(img['date_captured']).timestamp()

    if 'geos_corners' in primary_obj:
        # FIXME: we are assuming this maps perfectly onto the image
        # which is should for the SMART data, but perhaps in the future
        # this will not be safe?
        img['geos_corners'] = primary_obj['geos_corners']
    else:
        print('None of the assets had geo information')
    return img


def _populate_valid_region(coco_img):
    """
    Ignore:
        >>> # Make a dummy image with nodata to test that this works
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import _populate_valid_region
        >>> import kwcoco
        >>> H, W = 1024, 1024
        >>> nodata = 0  #
        >>> dpath = ub.Path.appdir('kwcoco_dataloader/tests/valid_region').ensuredir()
        >>> imdata = ((np.random.rand(H, W) * 240) + 3).astype(np.uint8)
        >>> # Fill in nodata values
        >>> imdata[:, 0:20] = nodata
        >>> imdata[:, -20:] = nodata
        >>> poly1 = kwimage.Polygon.random(rng=432).scale((W, H))
        >>> poly1.data['exterior'] = poly1.data['exterior'].round()
        >>> poly1.fill(imdata, nodata)
        >>> poly2 = kwimage.Polygon.circle((0, 0), W / 2)
        >>> poly2.fill(imdata, nodata)
        >>> # Write image to disk with nodata info
        >>> img_fpath = dpath / 'test_img.tif'
        >>> kwimage.imwrite(img_fpath, imdata, backend='gdal', nodata=0, overviews=3)
        >>> # # Register the image with a kwcoco dataset
        >>> dset = kwcoco.CocoDataset()
        >>> dset.fpath = dpath / 'data.kwcooc.json'
        >>> gid = dset.add_image(file_name=img_fpath, channels='gray')
        >>> dset.conform()
        >>> #
        >>> coco_img = dset.coco_image(gid)
        >>> _populate_valid_region(coco_img)
        >>> valid_region = kwimage.MultiPolygon.coerce(coco_img.img['valid_region'])
        >>> print('valid_region.data = {!r}'.format(valid_region.data))
        >>> #
        >>> import kwplot
        >>> kwplot.autompl()
        >>> canvas = imdata.copy()
        >>> canvas = valid_region.draw_on(canvas, fill=0, border=True)
        >>> kwplot.imshow(canvas)

        from rasterio import features
        shapes = [(valid_region.to_geojson(), 255)]
        canvasR = features.rasterize(shapes, out=canvas[:, :, 0].copy())
        kwplot.imshow(canvasR, doclf=1)
    """
    from kwgis.gis.geotiff import geotiff_metadata
    # _ = ub.cmd('gdalinfo -stats {}'.format(fpath), check=True)
    bundle_dpath = coco_img.bundle_dpath
    img = coco_img.img
    primary_obj = coco_img.primary_asset()
    if primary_obj is None:
        warnings.warn('No primary asset found for img={}'.format(img))
        return
    primary_fname = primary_obj.get('file_name', None)
    primary_fpath = join(bundle_dpath, primary_fname)

    # NOTE: THIS POLYGON IS COMPUTED VIA RASTERIO, NOT SURE HOW WELL THIS AGREES
    # WITH OTHER POLYGONS WE DRAW (USUALLY VIA CV2)
    # TODO: get a better heuristic here
    sh_poly = util_raster.mask(
        primary_fpath,
        tolerance=4,
        # tolerance=None,
        default_nodata=primary_obj.get('default_nodata', None),
        # max_polys=100,
        use_overview=2,
        convex_hull=True,
    )
    kw_asset_poly = kwimage.MultiPolygon.from_shapely(sh_poly)

    info = primary_obj.get('geotiff_metadata', None)
    if info is None:
        metakw = {}
        dem_hint = primary_obj.get('dem_hint', 'use')
        if dem_hint == 'ignore':
            metakw['elevation'] = 0
        info = geotiff_metadata(primary_fpath, **metakw)

    warp_img_from_asset = kwimage.Affine.coerce(primary_obj.get('warp_aux_to_img', None))
    if warp_img_from_asset.isclose_identity():
        kw_img_poly = kw_asset_poly
    else:
        kw_img_poly = kw_asset_poly.warp(warp_img_from_asset)

    # TODO: we probably should not add the valid region to the asset.
    # Not sure if its used anywhere though.
    primary_obj['valid_region'] = kw_asset_poly.to_coco(style='new')
    img['valid_region'] = kw_img_poly.to_coco(style='new')

    if 'pxl_to_wld' in info:
        wld_from_asset = info['pxl_to_wld']
        kw_poly_utm = kw_asset_poly.warp(wld_from_asset).warp(info['wld_to_utm'])
        poly_utm = kw_poly_utm.to_geojson()
        poly_utm['properties'] = {}
        poly_utm['properties']['crs'] = info['utm_crs_info']
        # TODO: we probably should only add this to the image and not the
        # asset?
        primary_obj['valid_region_utm'] = poly_utm
        img['valid_region_utm'] = poly_utm


def _populate_canvas_obj(bundle_dpath, obj, overwrite=False, with_wgs=False,
                         default_gsd=None, keep_geotiff_metadata=False,
                         enable_intensity_stats=False):
    """
    obj can be an img or aux

    Ignore:
        from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        from kwcoco_dataloader.demo.smart_kwcoco_demodata import demo_kwcoco_with_heatmaps
        coco_dset = demo_kwcoco_with_heatmaps()
        coco_img = coco_dset.coco_image(1)
        obj = coco_img.primary_asset()
        bundle_dpath = coco_dset.bundle_dpath
        overwrite = True
        with_wgs = False
        default_gsd = None
        keep_geotiff_metadata = False
    """
    from kwgis.gis.geotiff import geotiff_metadata
    sensor_coarse = obj.get('sensor_coarse', None)  # not reliable
    num_bands = obj.get('num_bands', None)
    channels = obj.get('channels', None)
    fname = obj.get('file_name', None)
    warp_to_wld = obj.get('warp_to_wld', None)
    approx_meter_gsd = obj.get('approx_meter_gsd', None)

    overwrite = _coerce_overwrite(overwrite)

    errors = []
    # Can only do this for images with file names
    if fname is not None:
        fpath = join(bundle_dpath, fname)

        info = None
        dem_hint = obj.get('dem_hint', 'use')
        metakw = {}
        if dem_hint == 'ignore':
            metakw['elevation'] = 0

        # TODO: ensure real nodata exists (maybe write helper file to disk?)
        sensor_coarse = obj.get('sensor_coarse', None)
        # if sensor_coarse in {'S2', 'L8', 'WV'}:
        #     default_nodata = 0
        # else:
        #     default_nodata = None
        # # Heuristic for no-data
        # obj['default_nodata'] = default_nodata

        if 'warp' in overwrite or warp_to_wld is None or approx_meter_gsd is None:
            try:
                if info is None:
                    info = geotiff_metadata(
                        fpath, strict=True, **metakw)

                if keep_geotiff_metadata:
                    obj['geotiff_metadata'] = info

                try:
                    height, width = info['img_shape'][0:2]
                except Exception:
                    print('info = {}'.format(ub.urepr(info, nl=1)))
                    raise

                obj['height'] = height
                obj['width'] = width
                # print('info = {!r}'.format(info))

                # WE NEED TO ACCOUNT FOR WLD_CRS TO USE THIS
                if info['is_rpc']:
                    obj_to_wld = None
                else:
                    obj_to_wld = kwimage.Affine.coerce(info['pxl_to_wld'])

                geos_corners = info['geos_corners']
                wld_crs_info = ub.dict_diff(info['wld_crs_info'], {'type'})
                obj.update({
                    'geos_corners': geos_corners,  # always in geojson
                    'wld_crs_info': wld_crs_info,
                })
                obj['band_metas'] = info['band_metas']
                obj['is_rpc'] = info['is_rpc']

                if with_wgs:
                    obj.update({
                        'wgs84_to_wld': info['wgs84_to_wld'],
                        'wld_to_pxl': info['wld_to_pxl'],
                    })

                approx_meter_gsd = info['approx_meter_gsd']
            except exceptions.GeoMetadataNotFound as ex:
                if default_gsd is not None:
                    obj['approx_meter_gsd'] = default_gsd
                    obj['warp_to_wld'] = kwimage.Affine.eye().__json__()
                else:
                    # FIXME: This might not be the best way to report errors
                    # raise
                    errors.append('no_crs_info: {!r}'.format(ex))
            else:
                obj['approx_meter_gsd'] = approx_meter_gsd
                if obj_to_wld is not None:
                    obj['warp_to_wld'] = kwimage.Affine.coerce(obj_to_wld).__json__()

        if 'band' in overwrite or num_bands is None:
            try:
                num_bands = _introspect_num_bands(fpath)
            except Exception:
                channels = obj.get('channels', None)
                if channels is not None:
                    num_bands = kwcoco.ChannelSpec(channels).numel()
                else:
                    raise
            obj['num_bands'] = num_bands

        if 'channels' in overwrite or channels is None:
            if sensor_coarse is not None:
                channels = _sensor_channel_hueristic(sensor_coarse, num_bands)
            elif num_bands is not None:
                channels = _num_band_hueristic(num_bands)
            else:
                raise Exception(ub.paragraph(
                    f'''
                    no methods to introspect channels
                    sensor_coarse={sensor_coarse},
                    num_bands={num_bands}
                    for obj={obj}
                    '''))
            obj['channels'] = channels

        # TODO: determine nodata defaults based on sensor_coarse

        if enable_intensity_stats:
            from kwcoco_dataloader.cli import coco_spectra
            coco_spectra.ensure_intensity_sidecar(fpath)

        return errors


@ub.memoize
def _is_writeable(dpath):
    " https://stackoverflow.com/questions/2113427/determining-whether-a-directory-is-writeable "
    import os
    return os.access(dpath, os.W_OK) and os.path.isdir(dpath)


def _coerce_overwrite(overwrite):
    """
    Im not a big fan of the way overwrite currently works, might want to
    refactor.
    """
    valid_overwrites = {'warp', 'band', 'channels'}
    default_overwrites = {'warp', 'band'}
    if isinstance(overwrite, str):
        overwrite = set(overwrite.split(','))
    if overwrite is True:
        overwrite = default_overwrites
    elif overwrite is False:
        overwrite = {}
    else:
        overwrite = set(overwrite)
        unexpected = overwrite - valid_overwrites
        if unexpected:
            raise ValueError(f'Got unexpected overwrites: {unexpected}')
    return overwrite


def coco_populate_geo_video_stats(coco_dset, video_id, target_gsd='max-resolution'):
    """
    Create a "video-space" for all images in a video sequence at a specified
    resolution.

    For this video, this chooses the "best" image as the "video canvas /
    region" and registers everything to that canvas/region. This creates the
    "video-space" for this image sequence. Currently the "best" image is the
    one that has the GSD closest to the target-gsd. This hueristic works well
    in most cases, but no all.

    Notes:
        * Currently the "best image" exactly define the video canvas / region.

        * Areas where other images do not overlap the vieo canvas are
          effectively lost when sampling in video space, because anything
          outside the video canvas is cropped out.

        * Auxilary / asset images are required to have an "approx_meter_gsd"
          and a "warp_to_wld" attribute to use this function atm.

    TODO:
        - [ ] Allow choosing of a custom "video-canvas" not based on any one image.
        - [ ] Allow choosing a "video-canvas" that encompases all images
        - [ ] Allow the base image to contain "approx_meter_gsd" /
              "warp_to_wld" instead of the auxiliary image
        - [ ] Is computing the scale factor based on approx_meter_gsd safe?

    Args:
        coco_dset (CocoDataset): coco dataset to be modified inplace
        video_id (int): video_id to modify
        target_gsd (float | str): string code, or float target gsd


    Example:
        >>> # xdoctest: +REQUIRES(env:DVC_DPATH)
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> from kwcoco_dataloader.utils.util_data import find_dvc_dpath
        >>> import kwcoco
        >>> dvc_dpath = find_dvc_dpath()
        >>> coco_fpath = dvc_dpath / 'Drop2-Aligned-TA1-2022-02-15/data.kwcoco.json'
        >>> video_id = 2

        >>> coco_fpath = dvc_dpath / 'Aligned-Drop2-TA1-2022-03-07/data.kwcoco.json'
        >>> coco_dset = kwcoco.CocoDataset(coco_fpath)
        >>> target_gsd = 10.0
        >>> video_id = 1
        >>> # We can check transforms before we apply this function
        >>> coco_dset.images(video_id=video_id).lookup('warp_img_to_vid', None)
        >>> # Apply the function
        >>> coco_populate_geo_video_stats(coco_dset, video_id, target_gsd)
        >>> # Check these transforms to make sure they look right
        >>> popualted_video = coco_dset.index.videos[video_id]
        >>> popualted_video = ub.dict_isect(popualted_video, ['width', 'height', 'warp_wld_to_vid', 'target_gsd'])
        >>> print('popualted_video = {}'.format(ub.urepr(popualted_video, nl=-1)))
        >>> coco_dset.images(video_id=video_id).lookup('warp_img_to_vid')

        # TODO: make a demo dataset with some sort of gsd metadata
        coco_dset = kwcoco.CocoDataset.demo('vidshapes8-multispectral')
        print('coco_dset = {!r}'.format(coco_dset))

        coco_fpath = ub.expandpath('~/data/dvc-repos/smart_watch_dvc/drop0_aligned/data.kwcoco.json')
        coco_fpath = '/home/joncrall/data/dvc-repos/smart_watch_dvc/drop1-S2-L8-aligned/combo_data.kwcoco.json'
        coco_dset = kwcoco.CocoDataset(coco_fpath)
        video_id = 1

        target_gsd = 2.8


        # Check drawing the valid region on the image
        frac = 1

        valid_regions = coco_dset.images().lookup('valid_region')
        cands = []
        for idx, valid_region in enumerate(valid_regions):
            valid_region_img = kwimage.MultiPolygon.coerce(valid_region)
            frac = valid_region_img.to_shapely().area / valid_region_img.bounding_box().area
            if frac < 0.6:
                cands.append(idx)
        gid = coco_dset.images().take(cands).lookup('id')[0]

        coco_img = coco_dset.coco_image(gid)
        imdata = coco_img.imdelay('blue').finalize(nodata='float')
        valid_region_img = kwimage.MultiPolygon.coerce(coco_img.img['valid_region'])
        frac = valid_region_img.to_shapely().area / valid_region_img.bounding_box().area
        print('frac = {!r}'.format(frac))

        canvas_imgspace = kwimage.normalize_intensity(imdata)
        kwplot.autompl()
        kwplot.imshow(canvas_imgspace, doclf=1)

        valid_region_img = kwimage.MultiPolygon.coerce(coco_img.img['valid_region'])
        canvas_imgspace = valid_region_img.draw_on(canvas_imgspace, fill=0, color='green')
        kwplot.imshow(canvas_imgspace)


        # Check the nodata polygon returned raw pixel methods
        primary_data = kwimage.imread(primary_fpath, nodata='float')
        valid_mask = ~np.isnan(primary_data)
        kw_poly = kwimage.Mask(valid_mask.astype(np.uint8), 'c_mask').to_multi_polygon()
        print('kwimage kw_poly.data = {!r}'.format(kw_poly.data))

        # CHeck the one returned by util_raster
        primary_fpath = coco_img.primary_image_filepath()
        sh_poly = util_raster.mask(
            primary_fpath, tolerance=None,
            convex_hull=0)
        kw_poly = kwimage.MultiPolygon.from_shapely(sh_poly)
        print('rasterio kw_poly.data = {!r}'.format(kw_poly.data))
    """
    from kwcoco.coco_image import CocoImage
    # Compute an image-to-video transform that aligns all frames to some
    # common resolution.
    video = coco_dset.index.videos[video_id]
    gids = coco_dset.index.vidid_to_gids[video_id]

    check_unique_channel_names(coco_dset, gids=gids)

    frame_infos = {}

    for gid in gids:
        img = coco_dset.index.imgs[gid]
        coco_img = CocoImage(img)

        # If the base dictionary has "warp_to_wld" and "approx_meter_gsd"
        # information we use that.
        warp_wld_from_img = img.get('warp_to_wld', None)
        img_approx_meter_gsd = img.get('approx_meter_gsd', None)
        wld_crs_info = img.get('wld_crs_info', None)

        # Otherwise we try to obtain it from the auxiliary images
        if img_approx_meter_gsd is None or warp_wld_from_img is None:
            # Choose any one of the auxiliary images that has the required
            # attribute
            aux_chosen = coco_img.primary_asset(requires=[
                'warp_to_wld', 'approx_meter_gsd'])
            if aux_chosen is None:
                raise Exception(ub.paragraph(
                    '''
                    Image auxiliary images have no warp_to_wld and approx_meter
                    gsd. The auxiliary images may not have associated geo
                    metadata.
                    '''))

            warp_wld_from_asset = kwimage.Affine.coerce(aux_chosen.get('warp_to_wld', None))
            warp_img_from_asset = kwimage.Affine.coerce(aux_chosen['warp_aux_to_img'])

            warp_asset_from_img = warp_img_from_asset.inv()
            warp_wld_from_img = warp_wld_from_asset @ warp_asset_from_img

            scale_img_from_asset = np.mean(warp_img_from_asset.decompose()['scale'])

            asset_approx_meter_gsd = aux_chosen['approx_meter_gsd']
            img_approx_meter_gsd = asset_approx_meter_gsd / scale_img_from_asset

            wld_crs_info = aux_chosen.get('wld_crs_info', None)

        if img_approx_meter_gsd is None or warp_wld_from_img is None:
            raise Exception(ub.paragraph(
                '''
                Both the base image and its auxiliary images do not seem to
                have the required warp_to_wld and approx_meter_gsd fields.
                The image may not have associated geo metadata.
                '''))

        warp_wld_from_img = kwimage.Affine.coerce(warp_wld_from_img)

        asset_channels = []
        asset_gsds = []
        for obj in coco_img.iter_asset_objs():
            _gsd = obj.get('approx_meter_gsd')
            if _gsd is not None:
                _gsd = round(_gsd, 1)
            asset_gsds.append(_gsd)
            asset_channels.append(obj.get('channels', None))

        frame_infos[gid] = {
            'warp_wld_from_img': warp_wld_from_img,
            'wld_crs_info': wld_crs_info,
            # Note: division because gsd is inverted. This got me confused, but
            # I'm pretty sure this works.
            'target_gsd': target_gsd,
            'approx_meter_gsd': img_approx_meter_gsd,
            'width': img['width'],
            'height': img['height'],
            'asset_channels': asset_channels,
            'asset_gsds': asset_gsds,
        }

    sorted_gids = ub.argsort(frame_infos, key=lambda x: x['approx_meter_gsd'])
    if sorted_gids:
        min_gsd_gid = sorted_gids[0]
        max_gsd_gid = sorted_gids[-1]
        max_example = frame_infos[max_gsd_gid]
        min_example = frame_infos[min_gsd_gid]
        max_gsd = max_example['approx_meter_gsd']
        min_gsd = min_example['approx_meter_gsd']

        if target_gsd == 'max-resolution':
            target_gsd_ = min_gsd
        elif target_gsd == 'min-resolution':
            target_gsd_ = max_gsd
        else:
            target_gsd_ = target_gsd
            if not isinstance(target_gsd, numbers.Number):
                raise TypeError('target_gsd must be a code or number = {}'.format(type(target_gsd)))
        target_gsd_ = float(target_gsd_)

        # Compute the scale factor needed to be applied to each image to achieve
        # the target videospace GSD.
        for info in frame_infos.values():
            info['target_gsd'] = target_gsd_
            info['to_target_scale_factor'] = info['approx_meter_gsd'] / target_gsd_

        available_channels = set()
        available_gsds = set()
        for gid in gids:
            img = coco_dset.index.imgs[gid]
            for obj in coco_img.iter_asset_objs():
                available_channels.add(obj.get('channels', None))
                _gsd = obj.get('approx_meter_gsd')
                if _gsd is not None:
                    available_gsds.add(round(_gsd, 1))

        # Align to the base reference frame closest to the target GSD, which
        # has the "to_target_scale_factor" that is closest to 1.0
        base_gid, base_info = min(
            frame_infos.items(),
            key=lambda kv: abs(1 - kv[1]['to_target_scale_factor'])
        )
        scale = base_info['to_target_scale_factor']
        base_wld_crs_info = base_info['wld_crs_info']

        # Can add an extra transform here if the video is not exactly in
        # any specific image space
        warp_baseimg_from_wld = base_info['warp_wld_from_img'].inv()
        warp_vid_from_wld = kwimage.Affine.scale(scale) @ warp_baseimg_from_wld

        video['width'] = int(np.ceil(base_info['width'] * scale))
        video['height'] = int(np.ceil(base_info['height'] * scale))
        video['wld_crs_info'] = base_wld_crs_info

        if 'valid_region_geos' in video:
            import geopandas as gpd
            from kwgis.utils import util_gis
            # Project the valid region onto video space
            valid_region_crs84 = kwimage.MultiPolygon.coerce(video['valid_region_geos'])
            wld_crs = base_wld_crs_info['auth']
            crs84 = util_gis.get_crs84()
            crs84_region_gdf = gpd.GeoDataFrame({'geometry': [valid_region_crs84.to_shapely()]}, crs=crs84)
            wld_region_gdf = crs84_region_gdf.to_crs(wld_crs)
            wld_region_poly = wld_region_gdf['geometry'].iloc[0]
            wld_region_kwpoly = kwimage.MultiPolygon.from_shapely(wld_region_poly)
            valid_region = wld_region_kwpoly.warp(warp_vid_from_wld).to_geojson()

            if 0:
                import kwplot
                kwplot.autompl()
                wld_map_gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
                ax = wld_map_gdf.plot()
                wld_region_gdf.to_crs('OGC:CRS84').plot(ax=ax, color='red')
                wld_region_gdf.plot(ax=ax, color='red')

            video['valid_region'] = valid_region

        # Store metadata in the video
        video['warp_wld_to_vid'] = warp_vid_from_wld.__json__()
        video['target_gsd'] = target_gsd_
        video['resolution'] = f'{target_gsd_}GSD'
        video['min_gsd'] = min_gsd
        video['max_gsd'] = max_gsd

    video['num_frames'] = len(gids)

    # Remove old cruft (can remove in future versions)
    video.pop('available_channels', None)

    for gid in gids:
        img = coco_dset.index.imgs[gid]
        frame_info = frame_infos[gid]
        wld_crs_info = frame_info['wld_crs_info']
        warp_wld_from_img = frame_info['warp_wld_from_img']
        warp_vid_from_img = warp_vid_from_wld @ warp_wld_from_img
        img['warp_img_to_vid'] = warp_vid_from_img.concise()

        if base_wld_crs_info != wld_crs_info:
            import warnings
            warnings.warn(ub.paragraph(
                f'''
                Video alignment is warping images with different World
                Coordinate Reference Systems, but still treating them as the
                same. FIXME
                base_wld_crs_info={base_wld_crs_info!r},
                wld_crs_info={wld_crs_info!r}
                '''))


def check_kwcoco_spatial_transforms(coco_dset):
    """
    import kwplot
    kwplot.plt.ion()
    import kwcoco
    dset = kwcoco.CocoDataset('/home/joncrall/remote/toothbrush/data/dvc-repos/smart_data_dvc-ssd/Drop6_MeanYear/imgonly-KR_R001.kwcoco.zip')

    import kwcoco_dataloader
    data_dvc_dpath = kwcoco_dataloader.find_dvc_dpath(tags='phase2_data', hardware='auto')
    dset = kwcoco.CocoDataset(data_dvc_dpath / 'Drop6-MeanYear10GSD/imganns-NZ_R001.kwcoco.zip')

    dset = kwcoco.CocoDataset('/home/joncrall/quicklinks/toothbrush_smart_expt_dvc/_debug/pred.kwcoco.zip')
    """

    import kwimage
    from kwgis.utils import util_gdal
    import numpy as np

    for video in coco_dset.videos().objs:

        video_box = kwimage.Box.from_dsize((video['width'], video['height']))
        print('video_box = {}'.format(ub.urepr(video_box, nl=1)))

        video_target_gsd = video['target_gsd']

        images = coco_dset.images(video_id=video['id'])

        for coco_img in images.coco_images:

            image_box = kwimage.Box.from_dsize((coco_img['width'], coco_img['height']))
            sensor = coco_img['sensor_coarse']

            image_summary = {
                'sensor': sensor,
                'video_box': video_box,
                'image_box': image_box,
            }
            warp_vid_from_img = coco_img.warp_vid_from_img
            scale_vid_from_img = warp_vid_from_img.decompose()['scale']
            recon_video_box = image_box.scale(scale_vid_from_img).quantize()
            image_summary['scale_vid_from_img'] = scale_vid_from_img
            image_summary['reconstructed_video_box'] = recon_video_box
            image_summary['img_gsd'] = video_target_gsd / (1 / np.mean(scale_vid_from_img))

            img = ub.udict(coco_img.img)
            img = img - {'has_predictions'}
            # print('coco_img.img = {}'.format(ub.urepr(img, nl=-1)))
            asset_summaries = []

            for asset in coco_img.assets:
                warp_img_from_asset = kwimage.Affine.coerce(asset['warp_aux_to_img'])
                scale_img_from_asset = warp_img_from_asset.decompose()['scale']

                warp_vid_from_asset = warp_vid_from_img @ warp_img_from_asset

                scale_vid_from_asset = warp_vid_from_asset.decompose()['scale']
                scale_asset_from_vid = np.mean(warp_vid_from_asset.inv().decompose()['scale'])

                asset_box = kwimage.Box.from_dsize((asset['width'], asset['height']))
                recon_img_box = asset_box.scale(scale_img_from_asset)
                recon_vid_box = asset_box.scale(scale_vid_from_asset)
                fpath = ub.Path(coco_img.bundle_dpath) / asset['file_name']
                gdal_dset = util_gdal.GdalOpen(fpath)
                asset_shape = (gdal_dset.RasterYSize, gdal_dset.RasterXSize, gdal_dset.RasterCount)
                info = gdal_dset.info()
                disk_gsd = np.mean(np.abs(kwimage.Affine.from_gdal(info['geoTransform']).decompose()['scale']))
                asset_summaries.append({
                    'video_box': video_box,
                    'image_box': image_box,
                    'asset_box': asset_box,
                    'asset_disk_shape': asset_shape,
                    'asset_disk_gsd': disk_gsd,

                    'asset_gsd': video_target_gsd / scale_asset_from_vid,

                    'scale_img_from_asset': scale_img_from_asset,
                    'scale_vid_from_asset': scale_vid_from_asset,
                    'reconstructed_img_box': recon_img_box.quantize(),
                    'reconstructed_vid_box': recon_vid_box.quantize(),
                })
                # assert len(info['bands']) == coco_img.channels.numel()

            image_summary['assets'] = asset_summaries
            print('image_summary = {}'.format(ub.urepr(image_summary, nl=3, sv=1)))


def check_geo_transform_consistency(coco_dset):
    """
    Checks the consistency of transforms between world, video, image, and asset
    space in a coco dataset.

    Ignore:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> #coco_dset = kwcoco.CocoDataset('/home/joncrall/remote/toothbrush/data/dvc-repos/smart_data_dvc-ssd/Drop6-MeanYear10GSD/imgonly-NZ_R001_v2.kwcoco.json')
        >>> coco_dset = kwcoco.CocoDataset('/home/joncrall/quicklinks/toothbrush_smart_data_dvc-ssd/Drop6/imgonly-NZ_R001.kwcoco.json')
        >>> coco_dset = kwcoco.CocoDataset('/home/joncrall/remote/toothbrush/data/dvc-repos/smart_data_dvc-ssd/Drop6-MeanYear10GSD/imganns-NZ_R001_v2.kwcoco.json')
        >>> populate_watch_fields(coco_dset, target_gsd=10, overwrite=True)
        >>> check_geo_transform_consistency(coco_dset)

        coco_dset = kwcoco.CocoDataset('/home/joncrall/quicklinks/toothbrush_smart_data_dvc-ssd/Drop6/imgonly-KR_R001.kwcoco.json')
        coco_dset = kwcoco.CocoDataset('/home/joncrall/quicklinks/toothbrush_smart_data_dvc-ssd/Drop6-MeanYear10GSD/imganns-KR_R001.kwcoco.zip')
    """

    def check_space_graph_concistency(graph_v3):
        errors = []

        # Test for consistency between video / image / asset spaces
        wld_boxes = graph_v3.nodes['wld']['boxes']

        spaces = ['asset', 'img', 'vid']
        space_crs_infos = ub.udict()
        for space in spaces:
            wld_crs_info = graph_v3.nodes[space].get('wld_crs_info', None)
            if wld_crs_info is not None:
                space_crs_infos[space] = wld_crs_info

        space_crs_infos_hash = space_crs_infos.map_values(ub.hash_data)
        if not ub.allsame(space_crs_infos_hash.values()):
            errors.append({
                'message': 'CRS is not the same in all spaces',
                'data': {
                    'space_crs_infos': space_crs_infos,
                    'space_crs_infos_hash': space_crs_infos_hash,
                }
            })

        import itertools as it
        ious = {}
        for s1, s2 in it.combinations(spaces, 2):
            if s1 in wld_boxes and s2 in wld_boxes:
                b1 = wld_boxes[s1]
                b2 = wld_boxes[s2]
                ious[(s1, s2)] = b1.iou(b2)

        if not all(v > 0.95 for v in ious.values()):
            errors.append({
                'message': 'World boxes do not line up',
                'data': {
                    'wld_boxes': wld_boxes,
                    'ious': ious,
                },
            })

        # Compute any remaining warps to complete the graph
        import operator as op
        from functools import reduce
        missing_edges = set(nx.transitive_closure(graph_v3).edges) - graph_v3.edges
        missing_edges = [(u, v) for u, v in missing_edges if u != v]
        for n1, n2 in missing_edges:
            path = nx.shortest_path(graph_v3, n1, n2)
            path_warps = []
            for edge in ub.iter_window(path, 2):
                warp = graph_v3.edges[edge]['warp']
                path_warps.append(warp)
            warp_n2_from_n1 = reduce(op.matmul, path_warps[::-1])
            graph_v3.add_edge(n1, n2, warp=warp_n2_from_n1)

        # For all paths in the graph, determine if the warps are
        # consistent
        pairs1 = list(it.combinations(graph_v3.nodes, 2))
        pairs2 = [e[::-1] for e in pairs1]
        pairs = pairs1 + pairs2

        for n1, n2 in pairs:
            all_paths = list(nx.all_simple_paths(graph_v3, n1, n2))
            for path in all_paths:
                path_warps = []
                for u, v in ub.iter_window(path, 2):
                    warp = graph_v3.edges[(u, v)]['warp']
                    path_warps.append(warp)
                warp_indirect = reduce(op.matmul, path_warps[::-1])
                warp_direct = graph_v3.edges[(n1, n2)]['warp']
                effective = warp_indirect.inv() @ warp_direct
                if not effective.isclose_identity(rtol=1e-3, atol=1e-3):
                    errors.append({
                        'message': 'Transforms are inconsistent',
                        'data': {
                            'nodes': (n1, n2),
                            'path': path,
                            'warp_indirect': warp_indirect.concise(),
                            'warp_direct': warp_direct.concise(),
                        },
                    })

        if 0:
            from cmd_queue.util.util_networkx import write_network_text
            write_network_text(graph_v3)

        if errors:
            import copy
            node_summaries = copy.deepcopy(dict(graph_v3.nodes))
            # print(ub.urepr(dict(graph_v3.nodes)))
            for key, val in node_summaries.items():
                if 'boxes' in val:
                    val['boxes'] = ub.udict(val['boxes']).map_values(lambda x: x.bounding_box().to_xywh().astype(float).data)
                if 'box' in val:
                    val['box'] = val['box'].bounding_box().to_xywh().data
                if 'corners_crs84' in val:
                    val['corners_crs84'] = val['corners_crs84'].bounding_box().to_xywh().data
                if 'wld_crs_info' in val:
                    val['wld_crs_info'] = val['wld_crs_info']['auth'][1]

                val['warp_to'] = {}
                for other, data in sorted(graph_v3.adj[key].items()):
                    val['warp_to'][other] = ub.urepr(data['warp'].concise(), precision=2, nl=0)
                    ...
            print('node_summaries = {}'.format(ub.urepr(node_summaries, nl=True, precision=2)))

        return errors

    error_ids = set()
    seen_ids = set()

    all_errors = {}

    from kwutil import util_progress
    pman = util_progress.ProgressManager()
    with pman:
        # Create graphs with relationships between videos / images / assets
        import networkx as nx
        for video_id in pman.progiter(coco_dset.videos(), desc='check video consistency'):

            video = coco_dset.index.videos[video_id]

            # vid_valid_crs84 = kwimage.MultiPolygon.coerce(video['valid_region_geos'])
            # vid_valid_vidspace = kwimage.MultiPolygon.coerce(video['valid_region'])
            vid_box_vidspace = kwimage.Box.from_dsize((video['width'], video['height'])).to_polygon()
            warp_vid_from_wld = kwimage.Affine.coerce(video['warp_wld_to_vid'])

            graph_v1 = nx.DiGraph()
            graph_v1.add_node('wld')
            graph_v1.add_node('vid')

            # Add a node with video properties
            graph_v1.nodes['vid']['box'] = vid_box_vidspace
            # graph_v1.nodes['vid']['valid_region'] = vid_valid_vidspace
            graph_v1.nodes['vid']['wld_crs_info'] = video['wld_crs_info']

            # Add relationship between video and world space
            graph_v1.add_edge('wld', 'vid', warp=warp_vid_from_wld)
            graph_v1.add_edge('vid', 'wld', warp=warp_vid_from_wld.inv())

            # Warp the video box into world space
            graph_v1.nodes['wld']['boxes'] = {}
            graph_v1.nodes['wld']['boxes']['vid'] = graph_v1.nodes['vid']['box'].warp(graph_v1.edges[('vid', 'wld')]['warp'])

            for gid in pman.progiter(coco_dset.images(), desc='check image consistency'):

                coco_img = coco_dset.coco_image(gid)
                img_corners_crs84 = kwimage.Polygon.coerce(coco_img['geos_corners'])
                img_box_imgspace = kwimage.Box.from_dsize((coco_img['width'], coco_img['height'])).to_polygon()
                warp_vid_from_img = kwimage.Affine.coerce(coco_img['warp_img_to_vid'])

                if coco_img.get('wld_to_pxl', None) is not None:
                    warp_img_from_wld = kwimage.Affine.coerce(coco_img['wld_to_pxl'])
                else:
                    warp_img_from_wld = None

                # Create a copy of the existing video graph for this image
                graph_v2 = graph_v1.copy()

                # Create a node with image properties
                graph_v2.add_node('img')
                graph_v2.nodes['img']['box'] = img_box_imgspace
                graph_v2.nodes['img']['corners_crs84'] = img_corners_crs84

                # Add relationship between image and video / world space
                graph_v2.add_edge('img', 'vid', warp=warp_vid_from_img)
                graph_v2.add_edge('vid', 'img', warp=warp_vid_from_img.inv())

                if warp_img_from_wld is not None:
                    graph_v2.add_edge('wld', 'img', warp=warp_img_from_wld)
                    graph_v2.add_edge('img', 'wld', warp=warp_img_from_wld.inv())
                    # Warp the image box into world space.
                    graph_v2.nodes['wld']['boxes']['img'] = graph_v2.nodes['img']['box'].warp(graph_v2.edges[('img', 'wld')]['warp'])
                    graph_v2.nodes['img']['wld_crs_info'] = coco_img['wld_crs_info']

                for asset in coco_img.assets:

                    channels = asset['channels']

                    asset_box_assetspace = kwimage.Box.from_dsize((asset['width'], asset['height'])).to_polygon()
                    asset_corners_crs84 = kwimage.Polygon.coerce(asset['geos_corners'])

                    warp_wld_from_asset = kwimage.Affine.coerce(asset['warp_to_wld'])
                    warp_img_from_asset = kwimage.Affine.coerce(asset['warp_aux_to_img'])

                    # Create a copy of the existing image graph for this asset
                    graph_v3 = graph_v2.copy()

                    # Create a node with asset properties
                    graph_v3.add_node('asset')
                    graph_v3.nodes['asset']['box'] = asset_box_assetspace
                    graph_v3.nodes['asset']['wld_crs_info'] = asset['wld_crs_info']
                    graph_v3.nodes['asset']['corners_crs84'] = asset_corners_crs84

                    graph_v3.add_edge('asset', 'wld', warp=warp_wld_from_asset)
                    graph_v3.add_edge('asset', 'img', warp=warp_img_from_asset)
                    graph_v3.add_edge('wld', 'asset', warp=warp_wld_from_asset.inv())
                    graph_v3.add_edge('img', 'asset', warp=warp_img_from_asset.inv())

                    # Warp the asset box into world space
                    graph_v3.nodes['wld']['boxes']['asset'] = graph_v3.nodes['asset']['box'].warp(graph_v3.edges[('asset', 'wld')]['warp'])

                    ########
                    # Checks
                    ########
                    errors = check_space_graph_concistency(graph_v3)
                    asset_id = (gid, channels)
                    if errors:
                        print(f'asset_id={asset_id}')
                        print('errors = {}'.format(ub.urepr(errors, nl=True)))
                    seen_ids.add(asset_id)
                    if errors:
                        all_errors[asset_id] = errors
                        error_ids.add(asset_id)

                    # print(ub.urepr(dict(graph_v3.nodes)))
                    # for space1
    ok_ids = seen_ids - error_ids
    print(f'{len(ok_ids)} / {len(seen_ids)} passed')


def check_unique_channel_names(coco_dset, gids=None, verbose=0):
    """
    Check each image has unique channel names

    TODO:
        - [ ] move to kwcoco proper

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> # TODO: make a demo dataset with some sort of gsd metadata
        >>> coco_dset = kwcoco.CocoDataset.demo('vidshapes8-multispectral')
        >>> check_unique_channel_names(coco_dset)
        >>> # Make some duplicate channels to test
        >>> obj = coco_dset.images().objs[0]
        >>> obj['auxiliary'][0]['channels'] = 'B1|B1'
        >>> obj = coco_dset.images().objs[1]
        >>> obj['auxiliary'][0]['channels'] = 'B1|B1'
        >>> obj = coco_dset.images().objs[2]
        >>> obj['auxiliary'][1]['channels'] = 'B1'
        >>> import pytest
        >>> with pytest.raises(AssertionError):
        >>>     check_unique_channel_names(coco_dset)

    """
    images = coco_dset.images(gids=gids)
    errors = []
    for img in images.objs:
        coco_img = coco_dset.coco_image(img['id'])
        try:
            _check_unique_channel_names_in_image(coco_img)
        except AssertionError as ex:
            if verbose:
                print('ERROR: ex = {}'.format(ub.urepr(ex, nl=1)))
            errors.append(ex)

    if errors:
        error_summary = ub.dict_hist(map(str, errors))
        raise AssertionError(ub.urepr(error_summary))


def _check_unique_channel_names_in_image(coco_img):
    import kwcoco
    seen = set()
    for obj in coco_img.iter_asset_objs():
        chans = kwcoco.FusedChannelSpec.coerce(obj['channels'])
        chan_list : list = chans.normalize().parsed
        intra_aux_duplicate = ub.find_duplicates(chan_list)
        if intra_aux_duplicate:
            raise AssertionError(
                'Image has internal duplicate bands: {}'.format(
                    intra_aux_duplicate))

        inter_aux_duplicates = seen & set(chan_list)
        if inter_aux_duplicates:
            raise AssertionError(
                'Image has inter-auxiliary duplicate bands: {}'.format(
                    inter_aux_duplicates))


def geotiff_format_info(fpath):
    from osgeo import gdal
    gdal_ds = gdal.Open(fpath, gdal.GA_ReadOnly)
    filelist = gdal_ds.GetFileList()

    aff_wld_crs = gdal_ds.GetSpatialRef()
    has_geotransform = aff_wld_crs is not None

    filename = gdal_ds.GetDescription()
    main_band = gdal_ds.GetRasterBand(1)
    block_size = main_band.GetBlockSize()

    num_bands = gdal_ds.RasterCount
    width = gdal_ds.RasterXSize
    height = gdal_ds.RasterYSize

    ovr_count = main_band.GetOverviewCount()
    ifd_offset = main_band.GetMetadataItem('IFD_OFFSET', 'TIFF')
    if ifd_offset is not None:
        ifd_offset = int(ifd_offset)
    block_offset = main_band.GetMetadataItem('BLOCK_OFFSET_0_0', 'TIFF')
    structure = gdal_ds.GetMetadata("IMAGE_STRUCTURE")
    compress = structure.get("COMPRESSION", 'NONE')
    interleave = structure.get("INTERLEAVE", None)

    has_external_overview = (filename + '.ovr' in filelist)

    format_info = {
        'fpath': fpath,
        'filelist': filelist,
        'blocksize': block_size,
        'ovr_count': ovr_count,
        'ifd_offset': ifd_offset,
        'block_offset': block_offset,
        'compress': compress,
        'interleave': interleave,
        'has_external_overview': has_external_overview,
        'num_bands': num_bands,
        'has_geotransform': has_geotransform,
        'width': width,
        'height': height,
    }
    return format_info


def ensure_transfered_geo_data(coco_dset, gids=None):
    for gid in ub.ProgIter(coco_dset.images(gids), desc='transfer metadata'):
        transfer_geo_metadata(coco_dset, gid)


def transfer_geo_metadata(coco_dset, gid):
    """
    Transfer geo-metadata from source geotiffs to predicted feature images

    THIS FUNCITON MODIFIES THE IMAGE DATA ON DISK! BE CAREFUL!

    ASSUMES THAT EVERYTHING IS ALREADY ALIGNED

    Example:
        # xdoctest: +REQUIRES(env:DVC_DPATH)
        from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        from kwcoco_dataloader.utils.util_data import find_dvc_dpath
        import kwcoco
        dvc_dpath = find_dvc_dpath()
        coco_fpath = dvc_dpath / 'drop1-S2-L8-aligned/combo_data.kwcoco.json'
        coco_dset = kwcoco.CocoDataset(coco_fpath)
        gid = coco_dset.images().peek()['id']

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco
        >>> from kwcoco_dataloader.demo.smart_kwcoco_demodata import hack_seed_geometadata_in_dset
        >>> coco_dset = kwcoco.CocoDataset.demo('vidshapes8-multispectral')
        >>> hack_seed_geometadata_in_dset(coco_dset, force=True, rng=0)
        >>> gid = 2
        >>> transfer_geo_metadata(coco_dset, gid)
        >>> fpath = join(coco_dset.bundle_dpath, coco_dset.coco_image(gid).primary_asset()['file_name'])
        >>> _ = ub.cmd('gdalinfo ' + fpath, verbose=1)
    """
    from osgeo import gdal
    from kwgis.gis.geotiff import geotiff_metadata
    coco_img = coco_dset.coco_image(gid)

    assets_with_geo_info = {}
    assets_without_geo_info = {}

    asset_objs = list(coco_img.iter_asset_objs())
    for asset_idx, obj in enumerate(asset_objs):
        fname = obj.get('file_name', None)
        if fname is not None:
            fpath = join(coco_img.dset.bundle_dpath, fname)
            try:
                info = geotiff_metadata(fpath)
                if info.get('crs_error', None) is not None:
                    raise Exception
            except Exception:
                assets_without_geo_info[asset_idx] = obj
            else:
                assets_with_geo_info[asset_idx] = (obj, info)

    warp_vid_from_geoimg = kwimage.Affine.eye()

    if assets_without_geo_info:
        if not assets_with_geo_info:
            class Found(Exception):
                pass
            try:
                # If an asset in our local image has no data, we can
                # check to see if anyone in the vide has data.
                # Check if anything in the video has geo-data
                video_id = coco_img.img['video_id']
                for other_gid in coco_dset.images(video_id=video_id):
                    if other_gid != gid:
                        other_coco_img = coco_dset.coco_image(other_gid)
                        for obj in other_coco_img.iter_asset_objs():
                            fname = obj.get('file_name', None)
                            if fname is not None:
                                fpath = join(coco_img.dset.bundle_dpath, fname)
                                try:
                                    # Try until we find an image with real CRS info
                                    info = geotiff_metadata(fpath)
                                    if info.get('crs_error', None) is not None:
                                        raise Exception
                                except Exception:
                                    continue
                                else:
                                    raise Found
            except Found:
                assets_with_geo_info[-1] = (obj, info)
                warp_vid_from_geoimg = kwimage.Affine.coerce(other_coco_img.img['warp_img_to_vid'])
            else:
                raise exceptions.GeoMetadataNotFound(ub.paragraph(
                    '''
                    There are images without geo data, but no other data within
                    this image has transferable geo-data
                    '''))

        # Choose an object to register to (not sure if it matters which one)
        # choose arbitrary one for now.
        geo_asset_idx, (geo_obj, geo_info) = ub.peek(assets_with_geo_info.items())

        if geo_info['is_rpc']:
            raise NotImplementedError(
                'Not sure how to do this if the target has RPC information')

        warp_geoimg_from_geoaux = kwimage.Affine.coerce(
            geo_obj.get('warp_aux_to_img', None))
        warp_wld_from_geoaux = kwimage.Affine.coerce(geo_info['pxl_to_wld'])

        georef_crs_info = geo_info['wld_crs_info']
        georef_crs = georef_crs_info['type']

        img = coco_img.img
        warp_vid_from_img = kwimage.Affine.coerce(img['warp_img_to_vid'])

        # In case our reference is from another frame in the video
        warp_geoimg_from_vid = warp_vid_from_geoimg.inv()
        warp_geoaux_from_geoimg = warp_geoimg_from_geoaux.inv()
        warp_wld_from_img = (
            warp_wld_from_geoaux @
            warp_geoaux_from_geoimg @
            warp_geoimg_from_vid @
            warp_vid_from_img)

        for _asset_idx, obj in assets_without_geo_info.items():
            fname = obj.get('file_name', None)
            fpath = join(coco_img.dset.bundle_dpath, fname)

            warp_img_from_aux = kwimage.Affine.coerce(
                obj.get('warp_aux_to_img', None))

            warp_wld_from_aux = (
                warp_wld_from_img @ warp_img_from_aux)

            # Convert to gdal-style
            aff_geo_transform = warp_wld_from_aux.to_gdal()

            dst_ds = gdal.Open(fpath, gdal.GA_Update)
            if dst_ds is None:
                raise exceptions.GeoMetadataNotFound('error handling gdal')
            ret = dst_ds.SetGeoTransform(aff_geo_transform)
            if ret != 0:
                raise AssertionError(f'failed to set SetGeoTransform on {fpath}')
            ret = dst_ds.SetSpatialRef(georef_crs)
            if ret != 0:
                raise AssertionError(f'failed to set SetSpatialRef on {fpath}')
            dst_ds.FlushCache()
            dst_ds = None

        # Matt's transfer metadata code
        """
        geo_ds = gdal.Open(toafile)
        if geo_ds is None:
            log.error('Could not open image')
            sys.exit(1)
        transform = geo_ds.GetGeoTransform()
        proj = geo_ds.GetProjection()
        dst_ds = gdal.Open(boafile, gdal.GA_Update)
        dst_ds.SetGeoTransform(transform)
        dst_ds.SetProjection(proj)
        geo_ds, dst_ds = None, None
        """


def _execute_transfer_task(task):
    fpath = task['fpath']
    aff_geo_transform = task['aff_geo_transform']
    georef_crs = task['georef_crs']
    from osgeo import gdal
    dst_ds = gdal.Open(fpath, gdal.GA_Update)
    if dst_ds is None:
        raise Exception('error handling gdal')
    ret = dst_ds.SetGeoTransform(aff_geo_transform)
    assert ret == 0
    ret = dst_ds.SetSpatialRef(georef_crs)
    assert ret == 0
    dst_ds.FlushCache()
    dst_ds = None


def _sensor_channel_hueristic(sensor_coarse, num_bands):
    """
    Given a sensor and the number of bands in the image, return likely channel
    codes for the image

    Note these are "pseudo-harmonized" by common_name, but not harmonized
    that is, one sensor's 'red' is roughly similar to another's but not corrected to match.
    Bands without a common_name will have a sensor-unique prefix appended to prevent this behavior.
    """
    from kwcoco_dataloader.utils.util_bands import WORLDVIEW2_PAN, WORLDVIEW2_MS4, WORLDVIEW2_MS8, SENTINEL2, LANDSAT8, LANDSAT7  # NOQA

    def code(bands, prefix):
        names = []
        for band_dict in bands:
            if 'common_name' in band_dict:
                names.append(band_dict['common_name'])
            else:
                names.append(prefix + band_dict['name'])
        return '|'.join(names)

    err = 0
    if sensor_coarse == 'WV':
        if num_bands == 1:
            channels = 'panchromatic'
        elif num_bands == 3:
            channels = 'r|g|b'
        elif num_bands == 4:
            channels = code(WORLDVIEW2_MS4, 'w')
        elif num_bands == 8:
            channels = code(WORLDVIEW2_MS8, 'w')
            #channels = 'wv1|wv2|wv3|wv4|wv5|wv6|wv7|wv8'
            # channels = 'cb|b|g|y|r|wv6|wv7|wv8'
        else:
            err = 1
    elif sensor_coarse == 'S2':
        if num_bands == 1:
            channels = 'gray'
        elif num_bands == 3:
            channels = 'r|g|b'
        elif num_bands == 13:
            channels = code(SENTINEL2, 's')
            # channels = 's1|s2|s3|s4|s4|s6|s7|s8|s8a|s9|s10|s11|s12'
            # channels = 'cb|b|g|r|s4|s6|s7|s8|s8a|s9|s10|s11|s12'
        else:
            err = 1
    elif sensor_coarse in {'LC', 'L8', 'LS'}:
        if num_bands == 1:
            channels = 'panchromatic'
        elif num_bands == 3:
            channels = 'r|g|b'
        elif num_bands == 11:
            channels = code(LANDSAT8, 'l8')
            # channels = 'lc1|lc2|lc3|lc4|lc5|lc6|lc7|lc8|lc9|lc10|lc11'
            # channels = 'cb|b|g|r|lc5|lc6|lc7|pan|lc9|lc10|lc11'
        else:
            err = 1
    elif sensor_coarse in {'LE', 'L7'}:
        if num_bands == 1:
            channels = 'panchromatic'
        elif num_bands == 3:
            channels = 'r|g|b'
        elif num_bands == 8:
            channels = code(LANDSAT7, 'l7')
        else:
            err = 1
    else:
        err = 1
    if err:
        msg = f'sensor_coarse={sensor_coarse}, num_bands={num_bands}'
        print('ERROR: mgs = {!r}'.format(msg))
        raise NotImplementedError(msg)
    return channels


def _introspect_num_bands(fpath):
    from kwcoco_dataloader.utils import util_kwimage
    shape = util_kwimage.load_image_shape(fpath, backend=['gdal', 'pil'])
    if len(shape) == 1:
        return 1
    elif len(shape) == 3:
        return shape[2]
    else:
        raise Exception(f'unknown format, fpath={fpath}, shape={shape}')


def _num_band_hueristic(num_bands):
    if num_bands == 1:
        channels = 'gray'
    elif num_bands == 3:
        channels = 'r|g|b'
    elif num_bands == 4:
        channels = 'r|g|b|a'
    else:
        raise Exception(f'num_bands={num_bands}')
    return channels


def _recompute_auxiliary_transforms(img):
    """
    Uses geotiff info to repopulate metadata
    """
    import kwimage
    from kwcoco.coco_image import CocoImage
    coco_img = CocoImage(img)
    base = coco_img.primary_asset(requires=['warp_to_wld'])
    if base is None:
        import warnings
        warnings.warn(
            'Cannot recompute auxiliary/asset transforms if no asset has a '
            ' warp_to_wld attribute')
        return
    try:
        warp_wld_from_img = kwimage.Affine.coerce(base['warp_to_wld'])
    except Exception:
        print('img = {}'.format(ub.urepr(img, nl=2)))
        raise

    warp_img_from_wld = warp_wld_from_img.inv()
    img.update(ub.dict_isect(base, {
        'geos_corners',
        'wld_crs_info',
        'width', 'height',
        'wgs84_to_wld',
        'wld_to_pxl',
    }))
    if 'width' not in img and 'height' not in img:
        if 'width' in base and 'height' in base:
            img['width'] = base['width']
            img['height'] = base['height']

    for asset in coco_img.assets:
        if 'warp_to_wld' in asset:
            warp_wld_from_asset = kwimage.Affine.coerce(asset['warp_to_wld'])
            warp_img_from_asset = warp_img_from_wld @ warp_wld_from_asset
            asset['warp_aux_to_img'] = warp_img_from_asset.concise()
        else:
            import warnings
            warnings.warn(
                'An asset could not have its warp_aux_to_img transform updated '
                'because it does not have a warp_to_wld attribute')


def coco_channel_stats(coco_dset):
    """
    Return information about what channels are available in the dataset

    Example:
        >>> import kwcoco
        >>> import ubelt as ub
        >>> import kwcoco_dataloader
        >>> coco_dset = kwcoco_dataloader.coerce_kwcoco('vidshapes-kwcoco_dataloader')
        >>> from kwcoco_dataloader.utils import kwcoco_extensions
        >>> info = kwcoco_extensions.coco_channel_stats(coco_dset)
        >>> print(ub.urepr(info, nl=3))
    """
    import kwcoco
    from kwcoco.coco_image import CocoImage

    sensor_hist = ub.ddict(lambda: 0)
    chan_hist = ub.ddict(lambda: 0)
    single_chan_hist = ub.ddict(lambda: 0)
    sensorchan_hist = ub.ddict(lambda: ub.ddict(lambda: 0))
    sensorchan_hist2 = ub.ddict(lambda: 0)
    for _gid, img in coco_dset.index.imgs.items():
        coco_img: CocoImage = coco_dset.coco_image(_gid)
        channels = []
        for obj in coco_img.iter_asset_objs():
            # TODO: perhaps replace unknown-chan with a "*"?
            channels.append(obj.get('channels', 'unknown-chan'))
        channels = sorted(channels)
        chan = ','.join(channels)
        sensor = img.get('sensor_coarse', '*')
        chan_hist[chan] += 1
        sensor_hist[sensor] += 1
        sensorchan_hist[sensor][chan] += 1
        # TODO: replace other usages with sensorchan_hist2 then remove other
        # uses, and rename sensorchan_hist2 to sensorchan_hist
        sensorchan = f'{sensor}:({chan})'
        sensorchan_hist2[sensorchan] += 1

        for single_chan in kwcoco.ChannelSpec(chan).unique():
            single_chan_hist[single_chan] += 1

    CS = kwcoco.ChannelSpec
    FS = kwcoco.FusedChannelSpec
    osets = [CS.coerce(c).fuse().to_oset() for c in chan_hist]
    if len(osets) == 0:
        common_channels = FS.coerce([])
        all_channels = FS.coerce([])
        all_sensorchan = kwcoco.SensorChanSpec.coerce('')
    else:
        common_channels = FS.coerce(list(ub.oset.intersection(*osets))).concise()
        all_channels = FS.coerce(list(ub.oset.union(*osets))).concise()
        all_sensorchan = kwcoco.SensorChanSpec.late_fuse(*[
            kwcoco.SensorChanSpec.coerce(s)
            for s in sensorchan_hist2.keys()]).concise()

    info = {
        'single_chan_hist': single_chan_hist,
        'chan_hist': chan_hist,
        'sensor_hist': sensor_hist,
        'sensorchan_hist': sensorchan_hist,
        'sensorchan_hist2': sensorchan_hist2,
        'common_channels': common_channels,
        'all_channels': all_channels,
        'all_sensorchan': all_sensorchan,
    }
    return info


def coco_img_wld_info(coco_img):
    """
    TODO: candidate for kwcoco.CocoImage method
    """
    from kwgis.utils import util_gis
    asset = coco_img.primary_asset(requires=['geos_corners'])
    if asset is None:
        raise KeyError(f'Geo-referenced asset not found for {coco_img}')
    if 'wld_to_pxl' in asset:
        warp_aux_from_wld = kwimage.Affine.coerce(asset['wld_to_pxl'])
    elif 'warp_to_wld' in asset:
        warp_aux_from_wld = kwimage.Affine.coerce(asset['warp_to_wld']).inv()
    else:
        print('asset = {}'.format(ub.urepr(asset, nl=1)))
        raise KeyError('Asset has no known transform to world coordinates')

    if 'wld_crs_info' in asset:
        wld_crs_info = asset['wld_crs_info']
    elif 'wld_crs_info' in coco_img.img:
        wld_crs_info = coco_img.img['wld_crs_info']
    else:
        print('asset = {}'.format(ub.urepr(asset, nl=1)))
        raise KeyError('Asset / image has no registered world CRS info')
    # TODO: traditional / authority check? Or assume traditional?
    # img['wld_crs_info']['axis_mapping'] == 'OAMS_TRADITIONAL_GIS_ORDER'
    wld_crs = util_gis.coerce_crs(wld_crs_info)

    warp_img_from_aux = kwimage.Affine.coerce(asset.get('warp_aux_to_img', None))
    warp_img_from_wld = warp_img_from_aux @ warp_aux_from_wld
    return warp_img_from_wld, wld_crs


def warp_annot_segmentations_to_geos(coco_dset):
    """

    Example:
        >>> from kwcoco_dataloader.utils.kwcoco_extensions import *  # NOQA
        >>> import kwcoco_dataloader
        >>> orig_dset = kwcoco_dataloader.coerce_kwcoco('kwcoco_dataloader-msi', geodata=True)
        >>> coco_dset = orig_dset.copy()
        >>> for ann in coco_dset.annots().objs:
        ...     ann.pop('segmentation_geos', None)
        >>> warp_annot_segmentations_to_geos(coco_dset)
        >>> errors = []
        >>> for aid in ub.ProgIter(coco_dset.annots()):
        >>>     ann1 = orig_dset.index.anns[aid]
        >>>     ann2 = coco_dset.index.anns[aid]
        >>>     poly1 = kwimage.MultiPolygon.from_geojson(ann1['segmentation_geos'])
        >>>     poly2 = kwimage.MultiPolygon.from_geojson(ann2['segmentation_geos'])
        >>>     worked = (poly1.is_invalid() and poly2.is_invalid()) or poly1.iou(poly2) > 0.99
        >>>     errors.append(not worked)
        >>> if sum(errors) > 0:
        >>>     # FIXME: THERE SHOULD BE NO ERRORS HERE. PUNTING TO MAKE
        >>>     # THE DASHBOARDS GREEN, BUT THIS SHOULD BE REVISITED
        >>>     #raise AssertionError('transforms should have cyclic consistency')
        >>>     warnings.warn('Transforms should have cyclic consistency, but some dont. This should be an error, but we will allow it for now')
        >>>     assert (sum(errors) / len(errors)) < 0.5, 'more than half of the data does not have cyclic consistency'
    """
    import pandas as pd
    import geopandas as gpd
    from kwgis.utils import util_gis

    crs84 = util_gis.get_crs84()
    gdfs = []
    for gid in coco_dset.images().gids:
        aids = []
        for ann in coco_dset.annots(image_id=gid).objs:
            if 'segmentation' in ann:
                aids.append(ann['id'])
        annots = coco_dset.annots(aids)
        if len(annots) > 0:
            # TODO: check crs properties (probably always crs84)
            warp_img_from_wld, wld_crs = coco_img_wld_info(coco_dset.coco_image(gid))
            ssegs = annots.detections.data['segmentations']
            warp_wld_from_img = warp_img_from_wld.inv()

            gdf = gpd.GeoDataFrame(
                dict(
                    geometry=[p.to_shapely() for p in ssegs],
                    aid=annots.aids,
                ),
                crs=None,
            )
            gdf = gdf.join(
                pd.DataFrame(dict(
                    gid=gid,
                    wld_crs=wld_crs,
                    warp_wld_from_img=[warp_wld_from_img.to_shapely()]
                )),
                how='cross'
            )
            gdfs.append(gdf)
    if len(gdfs) > 0:
        gdf = pd.concat(gdfs, axis=0, ignore_index=True)

        crs84_info = {
            'axis_mapping': 'OAMS_TRADITIONAL_GIS_ORDER',
            'auth': ('EPSG', '4326')
        }
        # Convert to string so we can crs as a group key
        gdf['wld_crs_str'] = gdf['wld_crs'].apply(lambda crs: crs.to_string())
        crs_groups = gdf.groupby('wld_crs_str')[
            ['geometry', 'wld_crs', 'warp_wld_from_img', 'aid']]

        gdf.loc[:, 'crs84_geoms'] = None
        for wld_crs_str, grp in crs_groups:
            wld_crs = grp['wld_crs'].iloc[0]
            for wld_from_img, subgrp in grp.groupby('warp_wld_from_img'):
                wld_geoms = subgrp.affine_transform(wld_from_img)
                wld_geoms = wld_geoms.set_crs(wld_crs)
                crs84_geoms = wld_geoms.to_crs(crs84)
                # this geojson rep also contains bboxes, but don't need to use them
                geojsons = crs84_geoms.__geo_interface__['features']
                for aid, geoj in zip(subgrp['aid'], geojsons):
                    # To be compatible with other kwcoco files (might need to
                    # allow for an entire feature to live here)
                    sseg_geos = geoj['geometry']
                    sseg_geos.setdefault('properties', {})
                    sseg_geos['properties']['crs_info'] = crs84_info
                    ann = coco_dset.anns[aid]
                    ann['segmentation_geos'] = sseg_geos
