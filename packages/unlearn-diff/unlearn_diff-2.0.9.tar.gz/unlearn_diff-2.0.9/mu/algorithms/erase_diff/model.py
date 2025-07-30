# mu/algorithms/erase_diff/model.py

import logging 
import torch

from pathlib import Path
from typing import Any

from mu.core import BaseModel
from mu.helpers import load_model_from_config

class EraseDiffModel(BaseModel):
    """
    EraseDiffModel handles loading, saving, and interacting with the Stable Diffusion model.

    Wu, J., Le, T., Hayat, M., & Harandi, M. (2024).

    EraseDiff: Erasing Data Influence in Diffusion Models

    https://arxiv.org/abs/2401.05779
    """

    def __init__(self, model_config_path: str, ckpt_path: str, device: str):
        """
        Initialize the EraseDiffModel.

        Args:
            model_config_path (str): Path to the model configuration file.
            ckpt_path (str): Path to the model checkpoint.
            device (str): Device to load the model on (e.g., 'cuda:0').
        """
        super().__init__()
        self.device = device
        self.model_config_path = model_config_path
        self.ckpt_path = ckpt_path
        self.model = self.load_model(model_config_path, ckpt_path, device)
        self.logger = logging.getLogger(__name__)

    def load_model(self, model_config_path: str, ckpt_path: str, device: str):
        """
        Load the Stable Diffusion model from config and checkpoint.

        Args:
            model_config_path (str): Path to the model configuration file.
            ckpt_path (str): Path to the model checkpoint.
            device (str): Device to load the model on.

        Returns:
            torch.nn.Module: Loaded Stable Diffusion model.
        """
        return load_model_from_config(model_config_path, ckpt_path, device)

    def save_model(self,model, output_path: str):
        """
        Save the trained model's state dictionary.

        Args:
            output_path (str): Path to save the model checkpoint.
        """
        torch.save({"state_dict": model.state_dict()}, output_path)


    def get_learned_conditioning(self, prompts: list) -> Any:
        """
        Obtain learned conditioning for given prompts.

        Args:
            prompts (list): List of prompt strings.

        Returns:
            Any: Learned conditioning tensors.
        """
        return self.model.get_learned_conditioning(prompts)

    def apply_model(self, z: torch.Tensor, t: torch.Tensor, c: Any) -> torch.Tensor:
        """
        Apply the model to generate outputs.

        Args:
            z (torch.Tensor): Noisy latent vectors.
            t (torch.Tensor): Timesteps.
            c (Any): Conditioning tensors.

        Returns:
            torch.Tensor: Model outputs.
        """
        return self.model.apply_model(z, t, c)
