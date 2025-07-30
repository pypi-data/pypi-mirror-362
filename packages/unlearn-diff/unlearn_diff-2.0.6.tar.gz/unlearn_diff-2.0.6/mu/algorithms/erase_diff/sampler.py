# mu/algorithms/erase_diff/sampler.py

import sys
import os
import logging

import torch
import numpy as np
from PIL import Image
from torch import autocast
from pytorch_lightning import seed_everything

from mu.core.base_sampler import BaseSampler  
from mu.datasets.constants import *
from mu.core import BaseSampler
from mu.helpers import load_config
from mu.helpers.utils import load_ckpt_from_config
from mu.helpers.utils import load_categories

from models import stable_diffusion
sys.modules['stable_diffusion'] = stable_diffusion

from stable_diffusion.ldm.models.diffusion.ddim import DDIMSampler
from mu.datasets.constants.i2p_const import i2p_categories


class EraseDiffSampler(BaseSampler):
    """
    EraseDiff Image Generator class extending a hypothetical BaseImageGenerator.
    
    Wu, J., Le, T., Hayat, M., & Harandi, M. (2024).

    EraseDiff: Erasing Data Influence in Diffusion Models

    https://arxiv.org/abs/2401.05779
    """

    def __init__(self, config: dict, **kwargs):
        """
        Initialize the EraseDiffSampler with a YAML config (or dict).
        
        Args:
            config (Dict[str, Any]): Dictionary of hyperparams / settings.
            **kwargs: Additional keyword arguments that can override config entries.
        """
        super().__init__()

        self.config = config
        self.device = config.get("device", "cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.sampler = None
        self.use_sample = self.config.get('use_sample')
        self.dataset_type = self.config.get("dataset_type", "default")
        self.categories = i2p_categories
        
        # For the default case, we use themes and classes.
        self.theme_available = uc_sample_theme_available_eval if self.use_sample else uc_theme_available
        self.class_available = uc_sample_class_available_eval if self.use_sample else uc_class_available
        
        
        self.logger = logging.getLogger(__name__)

    def load_model(self) -> None:
        """
        Load the model using `config` and initialize the sampler.
        """
        self.logger.info("Loading model...")
        model_ckpt_path = self.config["ckpt_path"]
        model_config = load_config(self.config["model_config_path"])
        self.model = load_ckpt_from_config(model_config, model_ckpt_path, verbose=True)
        self.model.to(self.device)
        self.model.eval()
        self.sampler = DDIMSampler(self.model)
        self.logger.info("Model loaded and sampler initialized successfully.")

    def sample(self) -> None:
        """
        Sample (generate) images using the loaded model and sampler, based on the config.
        """
        steps = self.config["ddim_steps"]        
        cfg_text = self.config["cfg_text"]    
        seed = self.config["seed"]
        H = self.config["image_height"]
        W = self.config["image_width"]
        ddim_eta = self.config["ddim_eta"]
        output_dir = self.config["sampler_output_dir"]

        # Create output directories.
        if self.dataset_type == "i2p":
            self.categories = i2p_categories
        elif self.dataset_type == "generic":
            self.categories = load_categories(self.config["reference_dir"])
        else:
            # Default: generate directories for each theme.
            for test_theme in self.theme_available:
                theme_path = os.path.join(output_dir, test_theme)
                os.makedirs(theme_path, exist_ok=True)
        
        self.logger.info(f"Generating images and saving to {output_dir}")

        # Set random seed for reproducibility.
        seed_everything(seed)
    
        if self.dataset_type == "i2p" or self.dataset_type == "generic":

            # For i2p and generic, iterate over categories only.
            for category in self.categories:
                category_path = os.path.join(output_dir, category)
                os.makedirs(category_path, exist_ok=True)

                prompt = f"A {category} image."
                self.logger.info(f"Sampling prompt: {prompt}")
                with torch.no_grad():
                    with autocast(self.device):
                        with self.model.ema_scope():
                            # Prepare conditioning.
                            uc = self.model.get_learned_conditioning([""])  
                            c  = self.model.get_learned_conditioning(prompt)
                            shape = [4, H // 8, W // 8]

                            # Generate samples using the sampler.
                            samples_ddim, _ = self.sampler.sample(
                                S=steps,
                                conditioning=c,
                                batch_size=1,
                                shape=shape,
                                verbose=False,
                                unconditional_guidance_scale=cfg_text,
                                unconditional_conditioning=uc,
                                eta=ddim_eta,
                                x_T=None
                            )

                            # Convert generated samples to image.
                            x_samples_ddim = self.model.decode_first_stage(samples_ddim)
                            x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)
                            x_samples_ddim = x_samples_ddim.cpu().permute(0, 2, 3, 1).numpy()
                            assert len(x_samples_ddim) == 1

                            # Convert to uint8 format.
                            x_sample = x_samples_ddim[0]
                            if isinstance(x_sample, torch.Tensor):
                                x_sample = (255. * x_sample.cpu().detach().numpy()).round()
                            else:
                                x_sample = (255. * x_sample).round()
                            x_sample = x_sample.astype(np.uint8)
                            img = Image.fromarray(x_sample)

                            # Save the generated image in the category's directory.
                            filename = f"{category}_seed_{seed}.jpg"
                            outpath = os.path.join(output_dir, category, filename)
                            img.save(outpath)
                            self.logger.info(f"Image saved: {outpath}")
        else:
            # Default behavior: iterate over themes and object classes.
            for test_theme in self.theme_available:
                for object_class in self.class_available:
                    prompt = f"A {object_class} image in {test_theme.replace('_',' ')} style."
                    self.logger.info(f"Sampling prompt: {prompt}")
                    with torch.no_grad():
                        with autocast(self.device):
                            with self.model.ema_scope():
                                # Prepare conditioning.
                                uc = self.model.get_learned_conditioning([""])  
                                c  = self.model.get_learned_conditioning(prompt)
                                shape = [4, H // 8, W // 8]

                                # Generate samples using the sampler.
                                samples_ddim, _ = self.sampler.sample(
                                    S=steps,
                                    conditioning=c,
                                    batch_size=1,
                                    shape=shape,
                                    verbose=False,
                                    unconditional_guidance_scale=cfg_text,
                                    unconditional_conditioning=uc,
                                    eta=ddim_eta,
                                    x_T=None
                                )

                                # Convert generated samples to image.
                                x_samples_ddim = self.model.decode_first_stage(samples_ddim)
                                x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)
                                x_samples_ddim = x_samples_ddim.cpu().permute(0, 2, 3, 1).numpy()
                                assert len(x_samples_ddim) == 1

                                # Convert to uint8 format.
                                x_sample = x_samples_ddim[0]
                                if isinstance(x_sample, torch.Tensor):
                                    x_sample = (255. * x_sample.cpu().detach().numpy()).round()
                                else:
                                    x_sample = (255. * x_sample).round()
                                x_sample = x_sample.astype(np.uint8)
                                img = Image.fromarray(x_sample)

                                # Save the generated image in the theme's directory.
                                filename = f"{test_theme}_{object_class}_seed_{seed}.jpg"
                                outpath = os.path.join(output_dir, test_theme, filename)
                                img.save(outpath)
                                self.logger.info(f"Image saved: {outpath}")

        self.logger.info("Image generation completed successfully.")
        return output_dir

    def save_image(self, image: Image.Image, file_path: str) -> None:
        """
        Save an image to the specified path.
        """
        image.save(file_path)
        self.logger.info(f"Image saved at: {file_path}")
