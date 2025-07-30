import kwutil
import kwarray
import ubelt as ub
import numpy as np
from delayed_image.channel_spec import FusedChannelSpec
# from delayed_image.channel_spec import ChannelSpec
from delayed_image.sensorchan_spec import SensorChanSpec
from kwcoco_dataloader.utils import util_kwarray
# from delayed_image.sensorchan_spec import FusedSensorChanSpec
# from delayed_image.sensorchan_spec import SensorSpec


class RobustNormalizer:
    """
    Abstracts the peritem and perframe normalization

    Note:
        Different normalization items should not have any overlap.
        Behavior might do weird things in this case.
        TODO: add a check to ensure the user doesnt do this.

    Attributes:
        _normalizer_items List[Dict]:
            the list of robust normalization parameters that should be
            associated with a sensor/channel pattern that will be normalized
            jointly. Contains params to be passed to
            :func:`kwarray.find_robust_normalizers`, the most common are high,
            mid, low, and mode which can be linear or sigmoid.
    """

    def __init__(self, normalizer_items):
        self._normalizer_items = normalizer_items

    @classmethod
    def coerce(cls, data, default_sensorchan=None, default_normalizer_params=None):
        """
        Args:
            data (Any):
                coercable representation

            default_sensorchan (SensorChanSpec):
                the default set of channels to use if known.

        Example:
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
            >>> default_sensorchan = 'red|green,blue|nir'
            >>> data = True
            >>> self = RobustNormalizer.coerce(data, default_sensorchan)
            >>> print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')

        Example:
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
            >>> default_sensorchan = 'red|green|blue|nir'
            >>> # From an explicit sensorchan config
            >>> data = 'red|green|blue'
            >>> self = RobustNormalizer.coerce(data, default_sensorchan)
            >>> print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
            >>> # From an explicit list of _normalizer_items
            >>> data = [
            >>>     {
            >>>         'sensorchan': 'red|green',
            >>>         'high': 0.95,
            >>>         'mode': 'linear',
            >>>     },
            >>>     {
            >>>         'sensorchan': 'blue,nir',
            >>>         'high': 1.0,
            >>>         'mode': 'sigmoid',
            >>>     },
            >>>     {
            >>>         'sensorchan': '(sensor1,sensor2):feature.0:3',
            >>>         'high': 1.0,
            >>>         'mode': 'sigmoid',
            >>>     },
            >>> ]
            >>> self = RobustNormalizer.coerce(data, default_sensorchan)
            >>> print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
        """
        if default_normalizer_params is None:
            default_normalizer_params = {
                'high': 1.00,
                # 'mid': 0.5,
                'mid': 0.5,
                'low': 0.00,
                # 'mode': 'sigmoid',
                'mode': 'linear',
            }
        else:
            default_normalizer_params = default_normalizer_params.copy()

        data = kwutil.Yaml.coerce(data, backend='pyyaml')
        if data is True:
            input_normalizers = [{
                'sensorchan': True,
            }]
        elif isinstance(data, str):
            input_normalizers = [{
                'sensorchan': data,
            }]
        elif isinstance(data, list):
            input_normalizers = data
        elif isinstance(data, dict):
            # Dict input can specify global defaults
            data = data.copy()
            defaults = data.pop('defaults', None)
            groups = data.pop('groups', None)
            sensorchan = data.pop('channels', None)
            sensorchan = data.pop('sensorchan', sensorchan)
            if defaults is None:
                defaults = data
            if sensorchan is not None:
                assert groups is None
                groups = [{'sensorchan': sensorchan}]
            default_normalizer_params.update(defaults)
            input_normalizers = groups
            if input_normalizers is None:
                # Apply to everything
                input_normalizers = [{
                    'sensorchan': '*',
                }]

        _normalizer_items = []
        for base_normalizer in input_normalizers:
            norm_item = base_normalizer.copy()
            sensorchan = norm_item.pop('channels', True)  # alias for sensorchan
            sensorchan = norm_item.pop('sensorchan', sensorchan)
            if sensorchan is True:
                sensorchan = default_sensorchan
            sensorchan = SensorChanSpec.coerce(sensorchan)

            separate_sensors = norm_item.get('separate_sensors', default_normalizer_params.get('separate_sensors', False))
            separate_channels = norm_item.get('separate_channels', default_normalizer_params.get('separate_channels', False))
            separate_time = norm_item.get('separate_time', default_normalizer_params.get('separate_time', False))

            norm_item['sensorchan'] = sensorchan.concise()
            norm_item['separate_sensors'] = separate_sensors
            norm_item['separate_time'] = separate_time
            norm_item['separate_channels'] = separate_channels
            norm_params = ub.udict.difference(default_normalizer_params, norm_item)
            norm_item.update(norm_params)
            if 1:
                norm_item = ub.udict(norm_item)
                x = (norm_item & default_normalizer_params)
                y = (norm_item - default_normalizer_params)
                norm_item = y | x
            _normalizer_items.append(norm_item)

        self = cls(_normalizer_items)
        return self

    def normalize(self, frame_items, _debug=False):
        """
        CommandLine:
            xdoctest -m kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer RobustNormalizer.normalize

        Example:
            >>> # From an explicit list of _normalizer_items
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
            >>> import kwutil
            >>> import kwarray.distributions
            >>> from delayed_image.channel_spec import FusedChannelSpec
            >>> data = kwutil.Yaml.coerce(ub.codeblock(
            ...     '''
            ...     defaults:
            ...         separate_channels: False
            ...         separate_sensors: False
            ...         separate_time: False
            ...         high: 1.0
            ...         low: 0.0
            ...         mode: linear
            ...     groups:
            ...       - sensorchan: r|g
            ...       - sensorchan: sensor1:b
            ...       - sensorchan: (sensor1,sensor2):c|m
            ...       - sensorchan: sensor2:y
            ...       - sensorchan: sensor1:k
            ...       - sensorchan: sensor2:k
            ...     '''))
            >>> self = RobustNormalizer.coerce(data)
            >>> print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
            >>> rng = kwarray.ensure_rng(43210231)
            >>> dist = kwarray.distributions.TruncNormal(mean=0.5, low=0, high=1, rng=rng)
            >>> num_frames = 3
            >>> sensors = ['sensor1', 'sensor2']
            >>> h = w = 1
            >>> modes = ['r|g|b', 'c|m|y|k']
            >>> mode_dropout = 0
            >>> sensor_dropout = 0
            >>> def build_mode_data(sensor_idx, time_idx):
            >>>     mode_data = {}
            >>>     idx = sensor_idx + (time_idx * len(sensors))
            >>>     total = num_frames + len(sensors)
            >>>     for mode in modes:
            >>>         c = mode.count('|') + 1
            >>>         if rng.rand() >= mode_dropout:
            >>>             #noise = dist.sample(c, h, w)
            >>>             #noise = dist.sample(c, h, w) * 0
            >>>             base = np.linspace(0, 1, c)[:, None, None]
            >>>             noise = np.tile(base, (1, h, w)) * dist.sample(c, h, w)
            >>>             mode_data[mode] = ((noise + idx) / (total + 1)).round(2)
            >>>     return mode_data
            >>> input_frame_items = [
            >>>     {
            >>>         'sensor': sensors[sensor_idx],
            >>>         'time_index': time_idx,
            >>>         'modes': build_mode_data(sensor_idx, time_idx)
            >>>     }
            >>>     for time_idx in range(num_frames)
            >>>     for sensor_idx in range(len(sensors))
            >>>     if rng.rand() >= sensor_dropout
            >>> ]
            >>> input_frame_items = [f for f in input_frame_items if f['modes']]
            >>> import copy
            >>> frame_items = copy.deepcopy(input_frame_items)
            >>> self.normalize(frame_items, _debug=True)
            >>> text1 = (f'input_frame_items = {ub.urepr(input_frame_items, nl=4)}')
            >>> text2 = (f'frame_items = {ub.urepr(frame_items, nl=4)}')
            >>> print(ub.hzcat([text1, text2]))
            >>> # xdoctest: +REQUIRES(module:kwplot)
            >>> # xdoctest: +REQUIRES(--show)
            >>> import kwplot
            >>> kwplot.autompl()
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.network_io import HeterogeneousBatchItem
            >>> # use networkio code to draw data
            >>> batch_item = HeterogeneousBatchItem({'frames': input_frame_items})
            >>> norm_batch_item = HeterogeneousBatchItem({'frames': frame_items})
            >>> kwplot.figure(fnum=1).clf()
            >>> default_combinable_channels = None
            >>> default_combinable_channels = 'auto'
            >>> norm_over_time = 0
            >>> # TODO: can we get the visualization intuitively show the normaliation?
            >>> canvas1 = batch_item.draw(default_combinable_channels=default_combinable_channels, max_channels=9, norm_over_time=norm_over_time)
            >>> canvas2 = norm_batch_item.draw(default_combinable_channels=default_combinable_channels, max_channels=9, norm_over_time=norm_over_time)
            >>> kwplot.imshow(canvas1, fnum=1, pnum=(1, 2, 1))
            >>> kwplot.imshow(canvas2, fnum=1, pnum=(1, 2, 2))

        Example:
            >>> # Test what happens when input frame has a constant value
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
            >>> import kwutil
            >>> data = kwutil.Yaml.coerce(ub.codeblock(
            ...     '''
            ...     - sensorchan: r
            ...       high: 1.0
            ...       mode: linear
            ...     '''))
            >>> self = RobustNormalizer.coerce(data)
            >>> print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
            >>> r = np.zeros((1, 1, 1)) + 10
            >>> input_frame_items = [
            >>>     {'sensor': 'sensor1', 'time_index': 0, 'modes': {'r': r}},
            >>> ]
            >>> import copy
            >>> frame_items = copy.deepcopy(input_frame_items)
            >>> self.normalize(frame_items)
            >>> text1 = (f'input_frame_items = {ub.urepr(input_frame_items, nl=4)}')
            >>> text2 = (f'frame_items = {ub.urepr(frame_items, nl=4)}')
            >>> print(ub.hzcat([text1, text2]))
            >>> assert np.all(frame_items[0]['modes']['r'] == 0), 'constant values normalize to zero'
        """
        # For each normalizer, gather the frame information with matching
        # channels that will need normalization.
        tasks = []
        if _debug:
            print('--- ROBUST NORMALIZE ---')
        for norm_item in self._normalizer_items:
            norm_sensorchan = norm_item['sensorchan']

            separate_sensors = norm_item.get('separate_sensors', False)
            separate_channels = norm_item.get('separate_channels', False)
            separate_time = norm_item.get('separate_time', False)

            # If the task separates different items, we construct keys to distinguish tehm.
            independent_groups = ub.ddict(list)
            tasks.append({
                'norm_item': norm_item,
                'independent_groups': independent_groups,
                'norm_sensorchan': norm_sensorchan,
            })
            if _debug:
                print(f'--- ATTEMPT MATCH: {norm_sensorchan} ---')

            for frame_item in frame_items:
                sensor = frame_item['sensor']
                time_index = frame_item.get('time_index', None)
                frame_modes = frame_item['modes']
                for mode_key, mode_data in frame_modes.items():
                    mode_chan = FusedChannelSpec.coerce(mode_key)

                    if norm_sensorchan.spec == '*:*':
                        # hack for full matching
                        matched_chans = mode_chan
                    else:
                        matched = norm_sensorchan.matching_sensor(sensor).chans
                        # Is this right? Do we use intersection, does it matter if
                        # matched is not a proper subset of mode_chan? I think it
                        # is ok if data is missing, but lets document it clearly
                        matched_chans = mode_chan.intersection(matched.fuse())

                    if _debug:
                        print(f' * test vs: {mode_chan}, found {matched_chans}')

                    if matched_chans.numel():
                        chan_to_slice = mode_chan.component_indices(axis=0)
                        _matched_slices = ub.udict(chan_to_slice).subdict(matched_chans.code_list())

                        if separate_channels:
                            slice_groups = [{k: v} for k, v in _matched_slices.items()]
                        else:
                            slice_groups = [_matched_slices]

                        for matched_slices in slice_groups:
                            # TODO: do we want to allow different sensors to be
                            # part of the same normalization group?
                            norm_group_key = {}
                            if separate_sensors:
                                norm_group_key['sensor'] = sensor
                            if separate_time:
                                norm_group_key['time_index'] = time_index
                            if separate_channels:
                                norm_group_key['channels'] = '|'.join(matched_slices.keys())
                            norm_group_key = tuple(norm_group_key.items())
                            if _debug:
                                print(f' * append to group: {norm_group_key}')
                            independent_groups[norm_group_key].append({
                                'time_index': time_index,
                                'sensor': sensor,
                                'mode_key': mode_key,
                                'mode_data': mode_data,
                                'matched_slices': matched_slices,
                            })

        for task in tasks:
            independent_groups = task['independent_groups']
            norm_item = task['norm_item']
            normalizer_params = ub.udict(norm_item) - {
                'sensorchan', 'separate_sensors',
                'separate_time', 'separate_channels'}

            if _debug:
                print('--- TASK ---')
                task_meta = ub.udict(task) - {'independent_groups'}
                print(f'task_meta = {ub.urepr(task_meta, nl=2)}')
                independent_parts = {}
                for norm_key, norm_items in independent_groups.items():
                    group_info = [ub.udict(v) - {'mode_data'} for v in norm_items]
                    independent_parts[norm_key] = group_info
                print(f'independent_parts = {ub.urepr(independent_parts, nl=2)}')

            for norm_key, norm_items in independent_groups.items():
                tocat = []
                for norm_item in norm_items:
                    mode_data = norm_item['mode_data']
                    for sl in norm_item['matched_slices'].values():
                        flat_subdata = mode_data[sl].ravel()
                        tocat.append(flat_subdata)

                raw_datas = np.concatenate(tocat, axis=0)
                raw_datas.shape
                valid_mask = np.isfinite(raw_datas)
                valid_raw_datas = raw_datas[valid_mask]
                # Compute robust normalizers over the entire temporal range per-sensor
                normalizer = kwarray.find_robust_normalizers(valid_raw_datas,
                                                             params=normalizer_params)
                # print(f'normalizer = {ub.urepr(normalizer, nl=1)}')

                # We don't actually need to do this because this was never
                # respected in older versions of the code.
                # if legacy:
                #     # Postprocess / regularize the normalizer
                #     # FIXME: This postprocess step unintuitive and not easy to
                #     # explain, we should mark this as legacy behavior and introduce
                #     # a new more reasonable default for peritem normalization.
                #     prior_min = min(0, normalizer['min_val'])
                #     alpha = 0.5
                #     normalizer['min_val'] * alpha + (1 - alpha) * prior_min

                if _debug:
                    group_info = [ub.udict(v) - {'mode_data'} for v in norm_items]
                    print(f'norm_key = {ub.urepr(norm_key, nl=1)}')
                    print(f'group_info = {ub.urepr(group_info, nl=1)}')
                    print(f'normalizer = {ub.urepr(normalizer, nl=1)}')
                    print(f'valid_raw_datas={valid_raw_datas}')

                # Apply the normalize to all parts of the original data inplace
                for norm_item in norm_items:
                    mode_data = norm_item['mode_data']
                    for sl in norm_item['matched_slices'].values():
                        chan_data = mode_data[sl]
                        valid_mask = np.isfinite(chan_data)
                        valid_data = chan_data[valid_mask]

                        # Apply normalizer (todo: update kwarray API and use
                        # kwarray variant)
                        imdata_normalized = util_kwarray.apply_robust_normalizer(
                            normalizer, chan_data, valid_data, valid_mask,
                            dtype=np.float32, copy=True)

                        imdata_normalized = np.clip(
                            imdata_normalized, 0.0, 1.0,
                            out=imdata_normalized)

                        # minval = imdata_normalized.min()
                        # maxval = imdata_normalized.max()
                        # assert maxval <= 1
                        # assert minval >= 0

                        # Overwrite original data with new normalized variants
                        mode_data[sl] = imdata_normalized
        return frame_items


def demo_doctests():
    """
    Placeholder for complex doctests that will likely become unit tests.

    CommandLine:
        xdoctest -m kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer demo_doctests

    Example:
        >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
        >>> demo_doctests()
    """
    # From an explicit list of _normalizer_items
    import kwutil
    data = kwutil.Yaml.coerce(ub.codeblock(
         '''
         - sensorchan: r|g
           high: 0.95
           mode: linear
           separate_sensors: True
           separate_channels: True
         - sensorchan: sensor1:b
           high: 1.0
           low: 0.0001
           mid: 0.5
           mode: sigmoid
         # Using "," or "|" does not impact the sensorchan pattern, as it is partially matched
         - sensorchan: c,m
           high: 1.0
           mode: linear
           separate_sensors: True
           separate_channels: True
         - sensorchan: y|k
           high: 1.0
           mode: linear
           separate_sensors: True
           separate_channels: False
         '''))
    print(f'data = {ub.urepr(data, nl=1)}')
    self = RobustNormalizer.coerce(data)
    print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
    zeros = np.zeros((1, 1))
    # import kwarray
    # rng = kwarray.ensure_rng(0)
    rgb1 = np.stack([zeros, zeros + 1, zeros + 2], axis=0)
    cmyk1 = np.stack([zeros, zeros + 1, zeros + 2, zeros + 3], axis=0)
    cmyk2 = cmyk1 + 4
    rgb2 = rgb1 + 3
    rgb3 = rgb1 + 6
    rgb4 = rgb1 + 9
    # rgb5 = rgb1 + 12
    # rgb6 = rgb1 + 15
    input_frame_items = [
        {'sensor': 'sensor1', 'time_index': 0, 'modes': {'r|g|b': rgb1, 'c|m|y|k': cmyk1}},
        {'sensor': 'sensor1', 'time_index': 1, 'modes': {'r|g|b': rgb2}},
        {'sensor': 'sensor2', 'time_index': 1, 'modes': {'c|m|y|k': cmyk2}},
        {'sensor': 'sensor1', 'time_index': 2, 'modes': {'r|g|b': rgb3}},
        {'sensor': 'sensor2', 'time_index': 2, 'modes': {'r|g|b': rgb4}},
    ]
    import copy
    frame_items = copy.deepcopy(input_frame_items)
    self.normalize(frame_items, _debug=True)

    text1 = (f'input_frame_items = {ub.urepr(input_frame_items, nl=4)}')
    text2 = (f'frame_items = {ub.urepr(frame_items, nl=4)}')
    print(ub.hzcat([text1, text2]))

    # Group and stack the results
    flat_results = [
        {'sensor': frame['sensor'], 'mode': k, 'data': v}
        for frame in frame_items for k, v in frame['modes'].items()
    ]
    groups = ub.group_items(flat_results, key=lambda d: (d['sensor'], d['mode']))
    stacked_groups = ub.udict(groups).map_values(lambda vs: np.stack([v['data'] for v in vs], axis=0))
    sensor1_rg = stacked_groups[('sensor1', 'r|g|b')][:, 0:2]
    # sensor2_rg = stacked_groups[('sensor2', 'r|g|b')][:, 0:2].ravel()
    sensor1_b = stacked_groups[('sensor1', 'r|g|b')][:, 2].ravel()
    sensor2_b = stacked_groups[('sensor2', 'r|g|b')][:, 2].ravel()
    # sensor1_yk = stacked_groups[('sensor1', 'c|m|y|k')][:, 2:4].ravel()
    sensor2_yk = stacked_groups[('sensor2', 'c|m|y|k')][:, 2:4].ravel()
    sensor1_cm = stacked_groups[('sensor1', 'c|m|y|k')][:, 0:2]
    sensor2_cm = stacked_groups[('sensor2', 'c|m|y|k')][:, 0:2]

    assert np.isclose(sensor2_b.max(), 11), 'sensor2 b is not normalized'
    assert 0.4 < sensor1_b.mean() < 0.5, 'sensor1 b is normalized independently'

    assert np.allclose(sensor1_cm, 0), 'c and m are normalized independently'
    assert np.allclose(sensor2_cm, 0), 'c and m are normalized independently'

    assert np.all(sensor1_rg[:, 0] == sensor1_rg[:, 1]), 'r and g are normalized independently'
    assert 0.49 < sensor1_rg.mean() < 0.51, 'r and g are normalized linearly'
    assert 0.49 < sensor2_yk.mean() < 0.51, 'y and k are normalized jointly across channels, and separately across sensors'


def doctest_perframe():
    """
    Check that perframe normalization, will normalize everything to zero for
    constant frames.

    TODO: move to a unit test

    Example:
        >>> from kwcoco_dataloader.tasks.fusion.datamodules.robust_normalizer import *  # NOQA
        >>> doctest_perframe()
    """
    import kwutil
    import kwarray.distributions
    data = kwutil.Yaml.coerce(ub.codeblock(
         '''
         defaults:
             separate_channels: True
             separate_sensors: True
             separate_time: True
             high: 1.0
             low: 0.0
             mode: linear
         groups:
           - sensorchan: r|g|b
         '''))
    self = RobustNormalizer.coerce(data)
    print(f'self._normalizer_items = {ub.urepr(self._normalizer_items, nl=1)}')
    rng = kwarray.ensure_rng(43210231)
    num_frames = 3
    sensors = ['sensor1', 'sensor2']
    h = w = 2
    modes = ['r|g|b']
    mode_dropout = 0
    sensor_dropout = 0
    def build_mode_data(sensor_idx, time_idx):
        mode_data = {}
        idx = sensor_idx + (time_idx * len(sensors))
        total = num_frames + len(sensors)
        for mode in modes:
            c = mode.count('|') + 1
            if rng.rand() >= mode_dropout:
                base = np.linspace(0, 1, c)[:, None, None]
                noise = np.tile(base, (1, h, w))
                mode_data[mode] = ((noise + idx) / (total + 1)).round(2)
        return mode_data
    input_frame_items = [
        {
            'sensor': sensors[sensor_idx],
            'time_index': time_idx,
            'modes': build_mode_data(sensor_idx, time_idx)
        }
        for time_idx in range(num_frames)
        for sensor_idx in range(len(sensors))
        if rng.rand() >= sensor_dropout
    ]
    input_frame_items = [f for f in input_frame_items if f['modes']]
    import copy
    frame_items = copy.deepcopy(input_frame_items)
    self.normalize(frame_items, _debug=True)
    text1 = (f'input_frame_items = {ub.urepr(input_frame_items, nl=4)}')
    text2 = (f'frame_items = {ub.urepr(frame_items, nl=4)}')
    print(ub.hzcat([text1, text2]))

    for frame in frame_items:
        for k, mode_data in frame['modes'].items():
            assert np.allclose(mode_data, 0, rtol=1e-5, atol=1e-5)
