# mu/algorithms/concept_ablation/concept_ablation_dataset.py

from torch.utils.data import Dataset

class WrappedDataset(Dataset):
    """Wraps an arbitrary object with __len__ and __getitem__ into a pytorch dataset
    
    Kumari, N., Zhang, B., Wang, S.-Y., Shechtman, E., Zhang, R., & Zhu, J.-Y. (2023).

    Ablating Concepts in Text-to-Image Diffusion Models

    Presented at the 2023 IEEE International Conference on Computer Vision
    
    """

    def __init__(self, dataset):
        self.data = dataset

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class ConcatDataset(Dataset):
    """Concatenates multiple datasets into one"""
    def __init__(self, *datasets):
        self.datasets = datasets

    def __getitem__(self, idx):
        return tuple(d[idx] for d in self.datasets)

    def __len__(self):
        return min(len(d) for d in self.datasets)
