
import multiprocessing
import cv2
import numpy as np
from torchvision.models import inception_v3
from scipy import linalg
import tqdm
import os
import torch
import warnings
from tqdm import tqdm
from torch import nn
from torchvision.models import inception_v3


def to_cuda(elements):
    """Transfers elements to CUDA if GPU is available."""
    if torch.cuda.is_available():
        return elements.to("cuda")
    return elements


class PartialInceptionNetwork(nn.Module):
    """
    A modified InceptionV3 network used for feature extraction.
    Captures activations from the Mixed_7c layer and outputs shape (N, 2048).
    """

    def __init__(self, transform_input=True):
        super().__init__()
        self.inception_network = inception_v3(pretrained=True)
        # Register a forward hook to capture activations from Mixed_7c
        self.inception_network.Mixed_7c.register_forward_hook(self.output_hook)
        self.transform_input = transform_input

    def output_hook(self, module, input, output):
        self.mixed_7c_output = output  # shape (N, 2048, 8, 8)

    def forward(self, x):
        """
        x: (N, 3, 299, 299) float32 in [0,1]
        Returns: (N, 2048) float32
        """
        assert x.shape[1:] == (3, 299, 299), f"Expected (N,3,299,299), got {x.shape}"
        # Shift to [-1, 1]
        x = x * 2 - 1
        # Trigger output hook
        _ = self.inception_network(x)
        # Collect the activations
        activations = self.mixed_7c_output  # (N, 2048, 8, 8)
        activations = torch.nn.functional.adaptive_avg_pool2d(activations, (1, 1))
        activations = activations.view(x.shape[0], 2048)
        return activations

def get_activations(images, batch_size=64):
    """
    Calculates activations for the last pool layer for all images using PartialInceptionNetwork.
    images: shape (N, 3, 299, 299), float32 in [0,1]
    Returns: np.array shape (N, 2048)
    """
    assert images.shape[1:] == (3, 299, 299)
    num_images = images.shape[0]
    inception_net = PartialInceptionNetwork().eval()
    inception_net = to_cuda(inception_net)

    n_batches = int(np.ceil(num_images / batch_size))
    inception_activations = np.zeros((num_images, 2048), dtype=np.float32)

    idx = 0
    for _ in range(n_batches):
        start = idx
        end = min(start + batch_size, num_images)
        ims = images[start:end]
        ims = to_cuda(ims)
        with torch.no_grad():
            batch_activations = inception_net(ims)
        inception_activations[start:end, :] = batch_activations.cpu().numpy()
        idx = end
    return inception_activations


def calculate_activation_statistics(images, batch_size=64):
    """
    Calculates the mean (mu) and covariance matrix (sigma) for Inception activations.
    images: shape (N, 3, 299, 299)
    Returns: (mu, sigma)
    """
    act = get_activations(images, batch_size=batch_size)
    mu = np.mean(act, axis=0)
    sigma = np.cov(act, rowvar=False)
    return mu, sigma


def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):
    """
    Computes the Frechet Distance between two multivariate Gaussians described by
    (mu1, sigma1) and (mu2, sigma2).
    """
    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)
    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    diff = mu1 - mu2

    # Product might be almost singular
    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    if not np.isfinite(covmean).all():
        warnings.warn(
            "FID calculation produced singular product; adding offset to covariances."
        )
        offset = np.eye(sigma1.shape[0]) * eps
        covmean, _ = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset), disp=False)

    if np.iscomplexobj(covmean):
        if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
            m = np.max(np.abs(covmean.imag))
            raise ValueError(f"Imaginary component in sqrtm: {m}")
        covmean = covmean.real

    return diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * np.trace(covmean)


def preprocess_image(im):
    """
    Resizes to 299x299, changes dtype to float32 [0,1], and rearranges shape to (3,299,299).
    """
    # If im is uint8, scale to float32
    if im.dtype == np.uint8:
        im = im.astype(np.float32) / 255.0
    im = cv2.resize(im, (299, 299))
    im = np.rollaxis(im, 2, 0)  # (H, W, 3) -> (3, H, W)
    im = torch.from_numpy(im)  # shape (3, 299, 299)
    return im


def preprocess_images(images, use_multiprocessing=False):
    """
    Applies `preprocess_image` to a batch of images.
    images: (N, H, W, 3)
    Returns: torch.Tensor shape (N, 3, 299, 299)
    """
    if use_multiprocessing:
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            jobs = [pool.apply_async(preprocess_image, (im,)) for im in images]
            final_images = torch.zeros(len(images), 3, 299, 299, dtype=torch.float32)
            for idx, job in enumerate(jobs):
                final_images[idx] = job.get()
    else:
        final_images = torch.stack([preprocess_image(im) for im in images], dim=0)

    return final_images


def calculate_fid(images1, images2, use_multiprocessing=False, batch_size=64):
    """
    Calculate FID between two sets of images.
    images1, images2: np.array shape (N, H, W, 3)
    Returns: FID (float)
    """
    # Preprocess to shape (N,3,299,299), float32 in [0,1]
    images1 = preprocess_images(images1, use_multiprocessing)
    images2 = preprocess_images(images2, use_multiprocessing)

    # Compute mu, sigma
    mu1, sigma1 = calculate_activation_statistics(images1, batch_size=batch_size)
    mu2, sigma2 = calculate_activation_statistics(images2, batch_size=batch_size)

    # Compute Frechet distance
    fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
    return fid


def load_style_generated_images(
    path, theme_available,class_available,exclude="Abstractionism", seed=[188, 288, 588, 688, 888]
):
    """Loads all .png or .jpg images from a given path
    Warnings: Expects all images to be of same dtype and shape.
    Args:
        path: relative path to directory
    Returns:
        final_images: np.array of image dtype and shape.
    """
    image_paths = []

    # if use_sample:
    #     class_available = ["Architectures"]

    if exclude is not None:
        if exclude in theme_available:
            theme_tested = [x for x in theme_available]
            theme_tested.remove(exclude)
            class_tested = class_available
        else:  # exclude is a class
            theme_tested = theme_available
            class_tested = [x for x in class_available]
            class_tested.remove(exclude)
    else:
        theme_tested = theme_available
        class_tested = class_available
    for theme in theme_tested:
        for object_class in class_tested:
            for individual in seed:
                image_paths.append(
                    os.path.join(
                        path, theme, f"{theme}_{object_class}_seed_{individual}.jpg"
                    )
                )
    if not os.path.isfile(image_paths[0]):
        raise FileNotFoundError(f"Could not find {image_paths[0]}")

    first_image = cv2.imread(image_paths[0])
    W, H = 512, 512
    image_paths.sort()
    image_paths = image_paths
    final_images = np.zeros((len(image_paths), H, W, 3), dtype=first_image.dtype)
    for idx, impath in tqdm(enumerate(image_paths)):
        im = cv2.imread(impath)
        im = cv2.resize(im, (W, H))  # Resize image to 512x512
        im = im[:, :, ::-1]  # Convert from BGR to RGB
        assert im.dtype == final_images.dtype
        final_images[idx] = im
    return final_images


def load_style_ref_images(path,theme_available,class_available,use_sample, exclude="Seed_Images"):
    """Loads all .png or .jpg images from a given path
    Warnings: Expects all images to be of same dtype and shape.
    Args:
        path: relative path to directory
    Returns:
        final_images: np.array of image dtype and shape.
    """
    image_paths = []


    if use_sample:
        class_available = ["Architectures"]
    if exclude is not None:
        # assert exclude in theme_available, f"{exclude} not in {theme_available}"
        if exclude in theme_available:
            theme_tested = [x for x in theme_available]
            theme_tested.remove(exclude)
            class_tested = class_available
        else:  # exclude is a class
            theme_tested = theme_available
            class_tested = [x for x in class_available]
            class_tested.remove(exclude)
    else:
        theme_tested = theme_available
        class_tested = class_available

    for theme in theme_tested:
        for object_class in class_tested:
            for idx in range(1, 6):
                image_paths.append(
                    os.path.join(path, theme, object_class, str(idx) + ".jpg")
                )

    first_image = cv2.imread(image_paths[0])
    W, H = 512, 512
    image_paths.sort()
    image_paths = image_paths
    final_images = np.zeros((len(image_paths), H, W, 3), dtype=first_image.dtype)
    for idx, impath in tqdm(enumerate(image_paths)):
        im = cv2.imread(impath)
        im = cv2.resize(im, (W, H))  # Resize image to 512x512
        im = im[:, :, ::-1]  # Convert from BGR to RGB
        assert im.dtype == final_images.dtype
        final_images[idx] = im
    return final_images


def tensor_to_float(obj):
    if isinstance(obj, dict):
        return {k: tensor_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [tensor_to_float(v) for v in obj]
    elif hasattr(obj, "item"):  # For PyTorch tensors
        return obj.item()
    else:
        return obj
