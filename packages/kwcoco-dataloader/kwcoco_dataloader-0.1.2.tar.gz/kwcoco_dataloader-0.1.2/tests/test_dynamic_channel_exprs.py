
def test_dynamic_channel_exprs():
    """
    Test different allowed expressions in dynamic channels
    """
    # Test normalization with dynamic channels
    from kwcoco_dataloader.tasks.fusion.datamodules.kwcoco_dataset import KWCocoVideoDataset
    import kwutil
    import kwcoco_dataloader

    dynamic_channels = kwutil.Yaml.coerce(
        '''
        - name: r1
          expr: '-g'
        - name: r2
          expr: 'exp(b / 255) ** 3 + 1'
        - name: r3
          expr: maximum(minimum(r, 0.9), 0.1)
        ''')
    channels = '|'.join([c['name'] for c in dynamic_channels])

    coco_dset = kwcoco_dataloader.coerce_kwcoco('vidshapes2')
    self = KWCocoVideoDataset(
        coco_dset, time_dims=5,
        window_dims=(128, 128),
        channels=channels,
        dynamic_channels=dynamic_channels
    )
    index = 0
    index = self.sample_grid['targets'][self.sample_grid['positives_indexes'][4]]
    item = self[index]

    if 1:
        # For developement
        canvas = self.draw_item(item)
        import kwplot
        kwplot.autompl()
        kwplot.imshow(canvas)
        kwplot.show_if_requested()
