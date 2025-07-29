# mu/algorithms/erase_diff/erase_diff_dataset.py

import os
from typing import Any, Tuple, Dict, List
from torch.utils.data import DataLoader

from mu.datasets import UnlearnCanvasDataset, I2PDataset, BaseDataset, GenericDataset
from mu.datasets.utils import INTERPOLATIONS, get_transform

class EraseDiffDataset(BaseDataset):
    """
    Dataset class for the EraseDiff algorithm.
    Extends BaseDataset to handle specific requirements.
    Manages both 'forget' and 'remain' datasets.

    @article{wu2024erasediff,
    title={EraseDiff: Erasing Data Influence in Diffusion Models},
    author={Wu, Jing and Le, Trung and Hayat, Munawar and Harandi, Mehrtash},
    journal={arXiv preprint arXiv:2401.05779},
    year={2024}
    }
    """

    def __init__(
        self,
        forget_data_dir: str,
        remain_data_dir: str,
        template: str,
        template_name: str,
        use_sample: bool = False,
        image_size: int = 512,
        interpolation: str = 'bicubic',
        batch_size: int = 4,
        num_workers: int = 4,
        pin_memory: bool = True,
        dataset_type: str = 'unlearncanvas',
        categories: List[str] = None
    ):
        """
        Initialize the EraseDiffDataset.

        Args:
            forget_data_dir (str): Directory containing forget dataset.
            remain_data_dir (str): Directory containing remain dataset.
            template (str): Template type ('style', 'object', or 'i2p').
            template_name (str): Name of the template to use (e.g., 'self-harm', 'Abstractionism').
            use_sample (bool, optional): Whether to use sample constants. Defaults to False.
            image_size (int, optional): Size to resize images. Defaults to 512.
            interpolation (str, optional): Interpolation mode for resizing. Defaults to 'bicubic'.
            batch_size (int, optional): Batch size for data loaders. Defaults to 4.
            num_workers (int, optional): Number of worker threads for data loading. Defaults to 4.
            pin_memory (bool, optional): Whether to pin memory in DataLoader. Defaults to True.
        """
        # Initialize transformations
        if interpolation not in INTERPOLATIONS:
            raise ValueError(f"Unsupported interpolation mode: {interpolation}. Supported modes: {list(INTERPOLATIONS.keys())}")

        interpolation_mode = INTERPOLATIONS[interpolation]
        transform = get_transform(interpolation=interpolation_mode, size=image_size)

        if dataset_type == 'i2p':
            self.forget_dataset = I2PDataset(
                data_dir=forget_data_dir,
                template_name=template_name,
                use_sample=use_sample,
                transform=transform
            )

            self.remain_dataset = I2PDataset(
                data_dir=remain_data_dir,
                template_name=template_name,
                use_sample=use_sample,
                transform=transform
            )
        elif dataset_type == 'unlearncanvas':
            # Initialize forget dataset
            self.forget_dataset = UnlearnCanvasDataset(
                data_dir=forget_data_dir,
                template=template,
                template_name=template_name,
                use_sample=use_sample,
                transform=transform
            )

            # Initialize remain dataset
            self.remain_dataset = UnlearnCanvasDataset(
                data_dir=remain_data_dir,
                template=template,
                template_name=template_name,
                use_sample=use_sample,
                transform=transform
            )
        elif dataset_type == 'generic':
            # Initialize forget dataset
            self.forget_dataset = GenericDataset(
                data_dir=forget_data_dir,
                template_name=template_name,
                categories = categories,
                transform=transform
            )

            # Initialize remain dataset
            self.remain_dataset = GenericDataset(
                data_dir=remain_data_dir,
                template_name=template_name,
                categories = categories,
                transform=transform
            )

        # Initialize DataLoaders
        self.forget_loader = DataLoader(
            self.forget_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=pin_memory
        )

        self.remain_loader = DataLoader(
            self.remain_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=pin_memory
        )

    def get_data_loaders(self) -> Dict[str, DataLoader]:
        """
        Retrieve the forget and remain data loaders.

        Returns:
            Dict[str, DataLoader]: Dictionary containing 'forget' and 'remain' DataLoaders.
        """
        return {
            'forget': self.forget_loader,
            'remain': self.remain_loader
        }

    def __len__(self) -> int:
        """
        Returns the length based on the forget dataset.

        Returns:
            int: Number of samples in the forget dataset.
        """
        return len(self.forget_dataset)

    def __getitem__(self, idx: int) -> Tuple[Any, str]:
        """
        Retrieve a sample from the forget dataset.

        Args:
            idx (int): Index of the sample.

        Returns:
            Tuple[Any, str]: A tuple containing the data sample and its corresponding prompt.
        """
        return self.forget_dataset[idx]