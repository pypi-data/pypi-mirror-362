# mu/algorithms/erase_diff/data_handler.py

import os
import random
import glob
import logging

import pandas as pd
from typing import Any, Dict
from torch.utils.data import DataLoader

from mu.datasets.constants import *
from mu.core import BaseDataHandler
from mu.helpers import read_text_lines
from mu.algorithms.erase_diff.datasets.erase_diff_dataset import EraseDiffDataset

class EraseDiffDataHandler(BaseDataHandler):
    """
    Concrete data handler for the EraseDiff algorithm.
    Manages forget and remain datasets through EraseDiffDataset.

    Wu, J., Le, T., Hayat, M., & Harandi, M. (2024).

    EraseDiff: Erasing Data Influence in Diffusion Models

    https://arxiv.org/abs/2401.05779
    """
    
    def __init__(
        self,
        raw_dataset_dir: str,
        processed_dataset_dir: str,
        template: str,
        template_name: str,
        batch_size: int = 4,
        image_size: int = 512,
        interpolation: str = 'bicubic',
        use_sample: bool = False,
        num_workers: int = 4,
        pin_memory: bool = True,
        dataset_type: str = 'unlearncanvas',
    ):
        """
        Initialize the EraseDiffDataHandler.

        Args:
            raw_dataset_dir (str): Directory containing the original dataset organized by themes and classes
            processed_dataset_dir (str): Directory where the processed datasets will be saved
            template (str): Template type ('style' or 'object')
            template_name (str): Name of the template to use
            batch_size (int, optional): Batch size for data loaders. Defaults to 4.
            image_size (int, optional): Size to resize images. Defaults to 512.
            interpolation (str, optional): Interpolation mode. Defaults to 'bicubic'.
            use_sample (bool, optional): Whether to use sample datasets. Defaults to False.
            num_workers (int, optional): Number of worker threads for data loading. Defaults to 4.
            pin_memory (bool, optional): Whether to pin memory in DataLoader. Defaults to True.
            dataset_type (str, optional): Type of dataset to use. Defaults to 'unlearncanvas'.
        """
        self.raw_dataset_dir = raw_dataset_dir
        self.processed_dataset_dir = processed_dataset_dir
        self.template = template
        self.template_name = template_name
        self.batch_size = batch_size
        self.image_size = image_size
        self.interpolation = interpolation
        self.use_sample = use_sample
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.dataset_type = dataset_type
        self.categories = None

        # Initialize logger
        self.logger = logging.getLogger(__name__)

        # Generate the dataset based on type
        self.generate_dataset()

        # Initialize DataLoaders
        self.data_loaders = self.get_data_loaders()

    def generate_dataset(self):
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




    def load_data(self, data_path: str) -> Any:
        """
        Load data from the specified path.
        For EraseDiff, this involves loading image paths and prompts.

        Args:
            data_path (str): Path to the data.

        Returns:
            Any: Loaded data (e.g., dictionary containing image paths and prompts).
        """
        images_txt = os.path.join(data_path, 'images.txt')
        prompts_txt = os.path.join(data_path, 'prompts.txt')
        if not os.path.isfile(images_txt) or not os.path.isfile(prompts_txt):
            self.logger.error(f"Missing images.txt or prompts.txt in {data_path}")
            raise FileNotFoundError(f"Missing images.txt or prompts.txt in {data_path}")
        image_paths = read_text_lines(images_txt)
        prompts = read_text_lines(prompts_txt)
        if len(image_paths) != len(prompts):
            self.logger.error(f"Mismatch between images and prompts in {data_path}")
            raise ValueError(f"Mismatch between images and prompts in {data_path}")
        return {'image_paths': image_paths, 'prompts': prompts}

    def preprocess_data(self, data: Any) -> Any:
        """
        Preprocess the data.
        For EraseDiff, this is handled by the Dataset class via transformations.

        Args:
            data (Any): Raw data to preprocess.

        Returns:
            Any: Preprocessed data.
        """
        # No additional preprocessing required as transformations are applied within the Dataset
        return data

    def get_data_loaders(self, batch_size: int = None) -> Dict[str, DataLoader]:
        """
        Get data loaders for forget and remain datasets.

        Args:
            batch_size (int, optional): Batch size for data loaders. If None, uses self.batch_size.

        Returns:
            Dict[str, DataLoader]: Dictionary containing 'forget' and 'remain' data loaders.
        """
        if batch_size is None:
            batch_size = self.batch_size

        # Determine dataset directories based on dataset type and template name
        if self.dataset_type == 'unlearncanvas':
            forget_data_dir = os.path.join(self.processed_dataset_dir, self.template_name)
            remain_data_dir = os.path.join(self.processed_dataset_dir, "Seed_Images")
        elif self.dataset_type == 'i2p':
            forget_data_dir = os.path.join(self.processed_dataset_dir, self.template_name)
            remain_data_dir = os.path.join(self.processed_dataset_dir, "Seed_Images")
        elif self.dataset_type == 'generic':
            forget_data_dir = os.path.join(self.processed_dataset_dir, self.template_name)
            remain_data_dir = os.path.join(self.processed_dataset_dir, "Seed_Images")
        else:
            raise ValueError(f"Unsupported dataset type: {self.dataset_type}")

        # Initialize EraseDiffDataset
        erase_diff_dataset = EraseDiffDataset(
            forget_data_dir=forget_data_dir,
            remain_data_dir=remain_data_dir,
            template=self.template,
            template_name=self.template_name,
            use_sample=self.use_sample,
            image_size=self.image_size,
            interpolation=self.interpolation,
            dataset_type=self.dataset_type,
            categories = self.categories
        )

        # Retrieve DataLoaders
        data_loaders = erase_diff_dataset.get_data_loaders()

        return data_loaders