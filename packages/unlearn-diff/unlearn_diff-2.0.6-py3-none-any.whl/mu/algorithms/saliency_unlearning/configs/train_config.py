# mu/algorithms/saliency_unlearning/configs/train_config.py

import os

from pathlib import Path

from mu.core.base_config import BaseConfig

current_dir = Path(__file__).parent


class SaliencyUnlearningConfig(BaseConfig):
    def __init__(self, **kwargs):
        # Model configuration
        self.alpha = 0.1  # Alpha value for training
        self.epochs = 1  # Number of epochs for training
        self.train_method = (
            "xattn"  # Attention method: ["noxattn", "selfattn", "xattn", "full"]
        )
        self.ckpt_path = "models/compvis/style50/compvis.ckpt"  # Path to the checkpoint
        self.model_config_path = current_dir / "model_config.yaml"

        # Dataset directories
        self.raw_dataset_dir = (
            "data/quick-canvas-dataset/sample"  # Path to the raw dataset
        )
        self.processed_dataset_dir = (
            "mu/algorithms/saliency_unlearning/data"  # Path to the processed dataset
        )
        self.dataset_type = "unlearncanvas"  # Type of the dataset
        self.template = "style"  # Template type for training
        self.template_name = "Abstractionism"  # Name of the template

        # Directory Configuration
        self.output_dir = "outputs/saliency_unlearning/finetuned_models"  # Directory for output models
        self.mask_path = (
            "outputs/saliency_unlearning/masks/0.5.pt"  # Path to the mask file
        )

        # Training configuration
        self.devices = "0"  # CUDA devices for training (comma-separated)
        self.use_sample = True  # Whether to use a sample dataset for training

        # Guidance and training parameters
        self.start_guidance = 0.5  # Start guidance for training
        self.negative_guidance = 0.5  # Negative guidance for training
        self.ddim_steps = 50  # Number of DDIM steps for sampling

        # Update properties based on provided kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def validate_config(self):
        """
        Perform basic validation on the config parameters.
        """
        # Check if directories exist
        if not os.path.exists(self.raw_dataset_dir):
            raise FileNotFoundError(f"Directory {self.raw_dataset_dir} does not exist.")
        if not os.path.exists(self.processed_dataset_dir):
            os.makedirs(self.processed_dataset_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.mask_path):
            raise FileNotFoundError(f"Mask file {self.mask_path} does not exist.")

        # Validate checkpoint path
        if not os.path.exists(self.ckpt_path):
            raise FileNotFoundError(f"Checkpoint file {self.ckpt_path} does not exist.")

        # Validate guidance values
        if not (0 <= self.start_guidance <= 1):
            raise ValueError("Start guidance should be between 0 and 1.")
        if not (0 <= self.negative_guidance <= 1):
            raise ValueError("Negative guidance should be between 0 and 1.")

        # Validate training method
        if self.train_method not in ["noxattn", "selfattn", "xattn", "full"]:
            raise ValueError(
                f"Invalid train_method: {self.train_method}. Must be one of ['noxattn', 'selfattn', 'xattn', 'full']."
            )

        # Validate DDIM steps
        if not isinstance(self.ddim_steps, int) or self.ddim_steps <= 0:
            raise ValueError("DDIM steps should be a positive integer.")

        # Validate model config path
        if not os.path.exists(self.model_config_path):
            raise FileNotFoundError(
                f"Model config file {self.model_config_path} does not exist."
            )


saliency_unlearning_train_mu = SaliencyUnlearningConfig()
saliency_unlearning_train_mu.dataset_type = "unlearncanvas"
saliency_unlearning_train_mu.raw_dataset_dir = "data/quick-canvas-dataset/sample"

saliency_unlearning_train_i2p = SaliencyUnlearningConfig()
saliency_unlearning_train_i2p.dataset_type = "i2p"
saliency_unlearning_train_i2p.raw_dataset_dir = "data/i2p-dataset/sample"
