"""
python -m kwcoco_dataloader.tasks.fusion


mkinit ~/code/kwcoco_dataloader/kwcoco_dataloader/tasks/fusion/datamodules/__init__.py --nomods -w
"""

__submodules__ = {
    'kwcoco_datamodule': ['KWCocoVideoDataModule'],
    'kwcoco_dataset': ['KWCocoVideoDataset'],
}
from kwcoco_dataloader.tasks.fusion.datamodules.kwcoco_datamodule import (
    KWCocoVideoDataModule,)
from kwcoco_dataloader.tasks.fusion.datamodules.kwcoco_dataset import (
    KWCocoVideoDataset,)

__all__ = ['KWCocoVideoDataModule', 'KWCocoVideoDataset']
