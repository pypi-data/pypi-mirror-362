# mu/algorithms/semipermeable_membrane/algorithm.py

import torch
import wandb
import logging

from typing import Dict
from pathlib import Path

from mu.core import BaseAlgorithm
from mu.core.base_config import BaseConfig
from mu.algorithms.semipermeable_membrane.model import SemipermeableMembraneModel
from mu.algorithms.semipermeable_membrane.data_handler import (
    SemipermeableMembraneDataHandler,
)
from mu.algorithms.semipermeable_membrane.trainer import SemipermeableMembraneTrainer
from mu.algorithms.semipermeable_membrane.configs import SemipermeableMembraneConfig


class SemipermeableMembraneAlgorithm(BaseAlgorithm):
    """
    SemipermeableMembraneAlgorithm orchestrates the setup and training of the SPM method.

    Lyu, M., Yang, Y., Hong, H., Chen, H., Jin, X., He, Y., Xue, H., Han, J., & Ding, G. (2023).

    One-dimensional Adapter to Rule Them All: Concepts, Diffusion Models and Erasing Applications

    https://arxiv.org/abs/2312.16145
    """

    def __init__(self, config: SemipermeableMembraneConfig, **kwargs):
        """
        Initialize the SemipermeableMembraneAlgorithm.

        Args:
            config (Dict): Configuration dictionary.
        """

        for key, value in kwargs.items():
            if not hasattr(config, key):
                setattr(config, key, value)
                continue
            config_attr = getattr(config, key)
            if isinstance(config_attr, BaseConfig) and isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    setattr(config_attr, sub_key, sub_val)
            elif isinstance(config_attr, dict) and isinstance(value, dict):
                config_attr.update(value)
            else:
                setattr(config, key, value)
        self.config = config.to_dict()

        self._parse_config()
        config.validate_config()
        self.model = None
        self.trainer = None
        self.data_handler = None
        self.logger = logging.getLogger(__name__)
        self._setup_components()
        self.device = self.model.device

    def _parse_config(self):
        return super()._parse_config()

    def _setup_components(self):
        """
        Setup model, data handler, and trainer components.
        """
        self.logger.info("Setting up components...")

        # Initialize Data Handler
        self.data_handler = SemipermeableMembraneDataHandler(
            template=self.config.get("template", ""),
            template_name=self.config.get("template_name", ""),
            dataset_type=self.config.get("dataset_type", "unlearncanvas"),
            use_sample=self.config.get("use_sample", False),
        )

        # Initialize Model
        self.model = SemipermeableMembraneModel(self.config)

        # Initialize Trainer
        self.trainer = SemipermeableMembraneTrainer(
            model=self.model,
            config=self.config,
            device=str(self.model.device),
            data_handler=self.data_handler,
        )

    def run(self):
        """
        Execute the training process.
        """
        try:
            # Initialize WandB with configurable project/run names
            wandb_config = {
                "project": self.config.get(
                    "wandb_project", "quick-canvas-machine-unlearning"
                ),
                "name": self.config.get("wandb_run", "Semipermeable Membrane"),
                "config": self.config,
            }
            wandb.init(**wandb_config)
            self.logger.info("Initialized WandB for logging.")

            # Create output directory if it doesn't exist
            output_dir = Path(self.config.get("output_dir", "./outputs"))
            output_dir.mkdir(parents=True, exist_ok=True)

            try:
                # Start training
                self.trainer.train()

                output_name = output_dir / self.config.get(
                    "output_name",
                    f"semipermeable_membrane_{self.config.get('template_name')}_model.pth",
                )

                # Save to WandB
                wandb.save(str(output_name))

            except Exception as e:
                self.logger.error(f"Error during training: {str(e)}")
                raise

        except Exception as e:
            self.logger.error(f"Failed to initialize training: {str(e)}")
            raise

        finally:
            # Ensure WandB always finishes
            if wandb.run is not None:
                wandb.finish()
            self.logger.info("Training complete. WandB logging finished.")
