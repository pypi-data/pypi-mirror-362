The kwcoco_dataloader Module
============================



|Pypi| |PypiDownloads| |ReadTheDocs| |GitlabCIPipeline| |GitlabCICoverage|


A windowed torch dataloader for kwcoco files with support for image sequences,
heterogeneous image sensors, arbitrary bands, efficient subimage loading via
COGs, pixelwise weighting, balanced sampling, and more.

An independent component ported from the `geowatch <https://gitlab.kitware.com/computer-vision/geowatch>`_ project.

As of version 0.1.0 it is a port of all features from geowatch needed to make
all doctest tests pass without issue.  This means that the dependency footprint
is slightly larger than it should be, and it will likely shrink over time or
have parts (particularly for GIS components) become options.

See Slides 77-86 in the `GeoWATCH slide deck <https://docs.google.com/presentation/d/125kMWZIwfS85lm7bvvCwGAlYZ2BevCfBLot7A72cDk8/edit#slide=id.g27d26def66f_0_61>`_.

The `geowatch tutorials <https://gitlab.kitware.com/computer-vision/geowatch/-/tree/main/docs/source/manual/tutorial>`_ also make heavy use of this dataloader and is a good referene while this repo is constructed.


+-----------------+---------------------------------------------------------------+
| Read the Docs   | http://kwcoco-dataloader.readthedocs.io/en/latest/            |
+-----------------+---------------------------------------------------------------+
| Gitlab (main)   | https://gitlab.kitware.com/computer-vision/kwcoco_dataloader  |
+-----------------+---------------------------------------------------------------+
| Github (mirror) | https://github.com/Kitware/kwcoco_dataloader                  |
+-----------------+---------------------------------------------------------------+
| Pypi            | https://pypi.org/project/kwcoco_dataloader                    |
+-----------------+---------------------------------------------------------------+



.. |Pypi| image:: https://img.shields.io/pypi/v/kwcoco_dataloader.svg
    :target: https://pypi.python.org/pypi/kwcoco_dataloader

.. |PypiDownloads| image:: https://img.shields.io/pypi/dm/kwcoco_dataloader.svg
    :target: https://pypistats.org/packages/kwcoco_dataloader

.. |ReadTheDocs| image:: https://readthedocs.org/projects/kwcoco-dataloader/badge/?version=latest
    :target: http://kwcoco-dataloader.readthedocs.io/en/latest/

.. |GitlabCIPipeline| image:: https://gitlab.kitware.com/computer-vision/kwcoco_dataloader/badges/main/pipeline.svg
    :target: https://gitlab.kitware.com/computer-vision/kwcoco_dataloader/-/jobs

.. |GitlabCICoverage| image:: https://gitlab.kitware.com/computer-vision/kwcoco_dataloader/badges/main/coverage.svg
    :target: https://gitlab.kitware.com/computer-vision/kwcoco_dataloader/commits/main
