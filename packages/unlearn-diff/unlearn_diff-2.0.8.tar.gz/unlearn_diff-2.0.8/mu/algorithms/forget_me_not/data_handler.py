# mu/algorithms/forget_me_not/data_handler.py

import os
import random
import glob
import logging
import torch

import pandas as pd
from typing import Any, Dict, Optional
from torch.utils.data import DataLoader

from mu.datasets.constants import *
from mu.core import BaseDataHandler
from mu.helpers import read_text_lines
from mu.algorithms.forget_me_not.datasets.forget_me_not_ti_dataset import ForgetMeNotTIDataset

class ForgetMeNotDataHandler(BaseDataHandler):
    """
    Data Handler for the Forget Me Not algorithm.
    Extends the BaseDataHandler to manage data loading, preprocessing, and data loader creation.

    Zhang, E., Wang, K., Xu, X., Wang, Z., & Shi, H. (2023).

    Forget-Me-Not: Learning to Forget in Text-to-Image Diffusion Models

    https://arxiv.org/abs/2211.08332
    """

    def __init__(self, config: Dict, tokenizer):
        super().__init__()
        self.config = config
        self.raw_dataset_dir = config.get('raw_dataset_dir')
        self.processed_dataset_dir = config.get('processed_dataset_dir')
        self.template = config.get('template')
        self.template_name = config.get('template_name')
        self.dataset_type = config.get('dataset_type', 'unlearncanvas')
        self.use_sample = config.get('use_sample', False)

        # Initialize logger
        self.logger = logging.getLogger(__name__)

        # Generate the dataset based on type
        self.generate_dataset()

    def generate_dataset(self, *args, **kwargs):
        """
        Generate dataset based on the dataset type
        """
        if self.dataset_type == 'unlearncanvas':
            self._generate_dataset_uc()
        elif self.dataset_type == 'i2p':
            self._generate_dataset_i2p()
        elif self.dataset_type == 'generic':
            self._generate_dataset_generic()
        else:
            raise ValueError(f"Unsupported dataset type: {self.dataset_type}")
        
    def _generate_dataset_uc(self):
        """
        Generate datasets by organizing images into themes and classes.
        Handles sample datasets if use_sample is enabled.
        """
        self.logger.info("Starting dataset generation (UC)...")

        themes = uc_sample_theme_available if self.use_sample else uc_theme_available
        classes = uc_sample_class_available if self.use_sample else uc_class_available

        classes_range = 3 if self.use_sample else 10

        for theme in themes:
            theme_dir = os.path.join(self.processed_dataset_dir, theme)
            os.makedirs(theme_dir, exist_ok=True)
            prompt_list = []
            path_list = []

            for class_ in classes:
                for idx in range(1, 4):
                    prompt = f"A {class_} image in {theme.replace('_', ' ')} style."
                    image_path = os.path.join(self.raw_dataset_dir, theme, class_, f"{idx}.jpg")
                    if os.path.exists(image_path):
                        prompt_list.append(prompt)
                        path_list.append(image_path)
                    else:
                        self.logger.warning(f"Image not found: {image_path}")

            prompts_txt_path = os.path.join(theme_dir, 'prompts.txt')
            images_txt_path = os.path.join(theme_dir, 'images.txt')

            with open(prompts_txt_path, 'w') as f:
                f.write('\n'.join(prompt_list))
            with open(images_txt_path, 'w') as f:
                f.write('\n'.join(path_list))

            self.logger.info(f"Generated dataset for theme '{theme}' with {len(path_list)} samples.")

            # For Seed Images
            seed_theme = "Seed_Images"
            seed_dir = os.path.join(self.processed_dataset_dir, seed_theme)
            os.makedirs(seed_dir, exist_ok=True)
            prompt_list = []
            path_list = []

            for class_ in classes:
                for idx in range(1, 4):
                    prompt = f"A {class_} image in Photo style."
                    image_path = os.path.join(self.raw_dataset_dir, seed_theme, class_, f"{idx}.jpg")
                    if os.path.exists(image_path):
                        prompt_list.append(prompt)
                        path_list.append(image_path)
                    else:
                        self.logger.warning(f"Image not found: {image_path}")

            prompts_txt_path = os.path.join(seed_dir, 'prompts.txt')
            images_txt_path = os.path.join(seed_dir, 'images.txt')

            with open(prompts_txt_path, 'w') as f:
                f.write('\n'.join(prompt_list))
            with open(images_txt_path, 'w') as f:
                f.write('\n'.join(path_list))

            self.logger.info(f"Generated Seed Images dataset with {len(path_list)} samples.")

            # For Class-based Organization
            for object_class in classes:
                class_dir = os.path.join(self.processed_dataset_dir, object_class)
                os.makedirs(class_dir, exist_ok=True)
                prompt_list = []
                path_list = []

                for theme in themes:
                    for idx in range(1, 4):
                        prompt = f"A {object_class} image in {theme.replace('_', ' ')} style."
                        image_path = os.path.join(self.raw_dataset_dir, theme, object_class, f"{idx}.jpg")
                        if os.path.exists(image_path):
                            prompt_list.append(prompt)
                            path_list.append(image_path)
                        else:
                            self.logger.warning(f"Image not found: {image_path}")

                prompts_txt_path = os.path.join(class_dir, 'prompts.txt')
                images_txt_path = os.path.join(class_dir, 'images.txt')

                with open(prompts_txt_path, 'w') as f:
                    f.write('\n'.join(prompt_list))
                with open(images_txt_path, 'w') as f:
                    f.write('\n'.join(path_list))

                self.logger.info(f"Generated dataset for class '{object_class}' with {len(path_list)} samples.")
        self.logger.info("Dataset generation (UC) completed.")

    def _generate_dataset_i2p(self):
        """
        Generate datasets for i2p by organizing images and prompts based on categories.
        """
        self.logger.info("Starting dataset generation (I2P)...")

        # Paths for images and prompts
        images_dir = os.path.join(self.raw_dataset_dir, 'images')
        prompts_file = os.path.join(self.raw_dataset_dir, 'prompts', 'i2p.csv')

        if not os.path.exists(prompts_file):
            self.logger.error("Prompts file not found: {prompts_file}")
            raise FileNotFoundError(f"Prompts file not found: {prompts_file}")

        # Read the CSV file
        data = pd.read_csv(prompts_file)

        categories = data['categories'].unique()

        for category in categories:
            category_dir = os.path.join(self.processed_dataset_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            prompt_list = []
            path_list = []

            category_data = data[data['categories'] == category]

            for _, row in category_data.iterrows():
                prompt = row['prompt']
                image_path = os.path.join(images_dir, category, f"{row['Unnamed: 0']}.jpg")

                if os.path.exists(image_path):
                    prompt_list.append(prompt)
                    path_list.append(image_path)
                else:
                    self.logger.warning(f"Image not found: {image_path}")

            prompts_txt_path = os.path.join(category_dir, 'prompts.txt')
            images_txt_path = os.path.join(category_dir, 'images.txt')

            with open(prompts_txt_path, 'w') as f:
                f.write('\n'.join(prompt_list))
            with open(images_txt_path, 'w') as f:
                f.write('\n'.join(path_list))

            self.logger.info(f"Generated dataset for category '{category}' with {len(path_list)} samples.")

            # Also need to generate Seed Images
            seed_category = "Seed_Images"
            seed_dir = os.path.join(self.processed_dataset_dir, seed_category)
            os.makedirs(seed_dir, exist_ok=True)
            prompt_list = []
            path_list = []

            for _, row in category_data.iterrows():
                prompt = row['prompt']
                image_path = os.path.join(images_dir, seed_category, f"{row['Unnamed: 0']}.jpg")

                if os.path.exists(image_path):
                    prompt_list.append(prompt)
                    path_list.append(image_path)
                else:
                    self.logger.warning(f"Image not found: {image_path}")

            prompts_txt_path = os.path.join(seed_dir, 'prompts.txt')
            images_txt_path = os.path.join(seed_dir, 'images.txt')
   
            with open(prompts_txt_path, 'w') as f:
                f.write('\n'.join(prompt_list))
            with open(images_txt_path, 'w') as f:
                f.write('\n'.join(path_list))

        self.logger.info("Dataset generation (I2P) completed.")


    def _generate_dataset_generic(self):
        """
        Generate dataset for the generic dataset type by organizing images and prompts
        into folders based on unique categories. Comma-separated category values in the CSV
        are split into individual categories. Image filenames are generated using an incremental
        counter (0,1,2,...) for each category.
        """
        self.logger.info("Starting dataset generation (Generic)...")

        # Define paths for raw images and the prompts CSV file.
        images_dir = os.path.join(self.raw_dataset_dir, 'images')
        prompts_folder = os.path.join(self.raw_dataset_dir, 'prompts')
        prompts_file = glob.glob(os.path.join(prompts_folder, '*.csv'))[0]
        # prompts_file = os.path.join(self.raw_dataset_dir, 'prompts', 'generic.csv')  

        if not os.path.exists(prompts_file):
            self.logger.error(f"Prompts file not found: {prompts_file}")
            raise FileNotFoundError(f"Prompts file not found: {prompts_file}")

        data = pd.read_csv(prompts_file)

        # Build a unique set of categories by splitting comma-separated entries.
        unique_categories = set()
        for cats in data['categories']:
            # Ensure cats is a string and split by comma.
            if isinstance(cats, str):
                for cat in cats.split(','):
                    unique_categories.add(cat.strip())
        self.categories = sorted(list(unique_categories))

        # Initialize a counter and storage for prompts and image paths for each category.
        counters = {category: 0 for category in self.categories}
        dataset_data = {category: {"prompts": [], "paths": []} for category in self.categories}

        # Process each row in the CSV.
        for _, row in data.iterrows():
            prompt = row['prompt']
            # Split the categories in this row.
            row_categories = []
            if isinstance(row['categories'], str):
                row_categories = [cat.strip() for cat in row['categories'].split(',')]
            else:
                self.logger.warning("Skipping row with non-string categories.")
                continue

            for category in row_categories:
                # Generate filename using the current counter.
                filename = f"{counters[category]}.jpg"
                counters[category] += 1
                # Construct the expected image path.
                image_path = os.path.join(images_dir, category, filename)

                if os.path.exists(image_path):
                    dataset_data[category]["prompts"].append(prompt)
                    dataset_data[category]["paths"].append(image_path)
                else:
                    self.logger.warning(f"Image not found: {image_path}")

        # Write out the prompts and image paths for each category.
        for category in self.categories:
            category_dir = os.path.join(self.processed_dataset_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            prompts_txt_path = os.path.join(category_dir, 'prompts.txt')
            images_txt_path = os.path.join(category_dir, 'images.txt')

            with open(prompts_txt_path, 'w') as f:
                f.write('\n'.join(dataset_data[category]["prompts"]))
            with open(images_txt_path, 'w') as f:
                f.write('\n'.join(dataset_data[category]["paths"]))

            self.logger.info(f"Generated dataset for category '{category}' with {len(dataset_data[category]['paths'])} samples.")

        seed_category = "Seed_Images"
        seed_dir = os.path.join(self.processed_dataset_dir, seed_category)
        os.makedirs(seed_dir, exist_ok=True)
        
        # Select a random category from the available categories.
        random_category = random.choice(self.categories)
        seed_prompt_list = dataset_data[random_category]["prompts"]
        seed_path_list = dataset_data[random_category]["paths"]

        # Save the seed prompts and image paths.
        seed_prompts_txt_path = os.path.join(seed_dir, 'prompts.txt')
        seed_images_txt_path = os.path.join(seed_dir, 'images.txt')
        with open(seed_prompts_txt_path, 'w') as f:
            f.write('\n'.join(seed_prompt_list))
        with open(seed_images_txt_path, 'w') as f:
            f.write('\n'.join(seed_path_list))

        self.logger.info(f"Seed images generated using category '{random_category}' with {len(seed_path_list)} samples.")
        self.logger.info("Dataset generation (Generic) completed.")



    def _text2img_dataloader(self,train_dataset, train_batch_size, tokenizer):
        def collate_fn(examples):
            input_ids = [example["instance_prompt_ids"] for example in examples]
            uncond_ids = [example["uncond_prompt_ids"] for example in examples]
            pixel_values = [example["instance_images"] for example in examples]

            # Concat class and instance examples for prior preservation.
            # We do this to avoid doing two forward passes.
            if examples[0].get("class_prompt_ids", None) is not None:
                input_ids += [example["class_prompt_ids"] for example in examples]
                pixel_values += [example["class_images"] for example in examples]

            pixel_values = torch.stack(pixel_values)
            pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()

            input_ids = tokenizer.pad(
                {"input_ids": input_ids},
                padding="max_length",
                max_length=tokenizer.model_max_length,
                return_tensors="pt",
            ).input_ids

            uncond_ids = tokenizer.pad(
                {"input_ids": uncond_ids},
                padding="max_length",
                max_length=tokenizer.model_max_length,
                return_tensors="pt",
            ).input_ids

            batch = {
                "input_ids": input_ids,
                "uncond_ids":uncond_ids,
                "pixel_values": pixel_values,
            }

            if examples[0].get("mask", None) is not None:
                batch["mask"] = torch.stack([example["mask"] for example in examples])

            return batch
        
        train_dataloader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=train_batch_size,
            shuffle=True,
            collate_fn=collate_fn,
        )

        return train_dataloader

    def load_data(self,         
                tokenizer,
                token_map: Optional[dict] = None,
                class_data_root=None,
                class_prompt=None,
                size=512,
                h_flip=True,
                color_jitter=False,
                resize=True,
                use_face_segmentation_condition=False,
                blur_amount: int = 70,
                train_batch_size: int = 1,
                *args, 
                **kwargs
            ) -> Dict[str, DataLoader]:
        """
        Create and return data loaders for training (and optionally validation/test sets).
        
        Args:
            batch_size (int): Batch size for data loaders.
        
        Returns:
            Dict[str, DataLoader]: A dictionary of data loaders.
        """        
        dataset = ForgetMeNotTIDataset(
            processed_dataset_dir=self.processed_dataset_dir,
            dataset_type=self.dataset_type,
            template_name=self.template_name,
            template = self.template, 
            sample=self.use_sample,
            tokenizer=tokenizer,  # Ensure tokenizer is passed in config
            token_map=token_map,
            class_data_root=class_data_root,
            class_prompt=class_prompt,
            size=size,
            h_flip=h_flip,
            color_jitter=color_jitter,
            resize=resize,
            use_face_segmentation_condition=use_face_segmentation_condition,
            blur_amount=blur_amount
        )


        train_dataloader = self._text2img_dataloader(
            dataset, train_batch_size, tokenizer
        )

        return train_dataloader


    def preprocess_data(self, *args, **kwargs):
        pass