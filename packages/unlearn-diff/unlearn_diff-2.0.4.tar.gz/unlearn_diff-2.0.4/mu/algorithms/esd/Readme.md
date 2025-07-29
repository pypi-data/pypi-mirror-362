# ESD Algorithm for Machine Unlearning

This repository provides an implementation of the ESD algorithm for machine unlearning in Stable Diffusion models. The ESD algorithm allows you to remove specific concepts or styles from a pre-trained model without retraining it from scratch.

### Installation

### Prerequisities
Ensure `conda` is installed on your system. You can install Miniconda or Anaconda:

- **Miniconda** (recommended): [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- **Anaconda**: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

After installing `conda`, ensure it is available in your PATH by running. You may require to restart the terminal session:

```bash
conda --version
```

**Step-by-Step Setup:**

Step 1. Create a Conda Environment Create a new Conda environment named myenv with Python 3.8.5:

```bash
conda create -n myenv python=3.8.5
```

Step 2. Activate the Environment Activate the environment to work within it:

```bash
conda activate myenv
```

Step 3. Install Core Dependencies Install PyTorch, torchvision, CUDA Toolkit, and ONNX Runtime with specific versions:

```bash
conda install pytorch==1.11.0 torchvision==0.12.0 cudatoolkit=11.3 onnxruntime==1.16.3 -c pytorch -c conda-forge
```

Step 4. Install our unlearn_diff Package using pip:

```bash
pip install unlearn_diff
```

Step 5. Install Additional Git Dependencies:

 After installing unlearn_diff, install the following Git-based dependencies in the same Conda environment to ensure full functionality:

```bash
pip install git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers
```

```bash
pip install git+https://github.com/openai/CLIP.git@main#egg=clip
```

```bash
pip install git+https://github.com/crowsonkb/k-diffusion.git
```

```bash
pip install git+https://github.com/cocodataset/panopticapi.git
```

```bash
pip install git+https://github.com/Phoveran/fastargs.git@main#egg=fastargs
```

```bash
pip install git+https://github.com/boomb0om/text2image-benchmark
```


### Downloading data and models.
After you install the package, you can use the following commands to download.

1. **Dataset**:
  - **i2p**:
    - **Sample**:
     ```
     download_data sample i2p
     ```
    - **Full**:
     ```
     download_data full i2p
     ```
  - **quick_canvas**:
    - **Sample**:
     ```
     download_data sample quick_canvas
     ```
    - **Full**:
     ```
     download_data full quick_canvas
     ```

2. **Model**:
  - **compvis**:
    ```
    download_model compvis
    ```
  - **diffuser**:
    ```
    download_model diffuser
    ```

3. **Download best.onnx model**

    ```
    download_best_onnx
    ```
**Verify the Downloaded Files**

After downloading, verify that the datasets have been correctly extracted:
```bash
ls -lh ./data/i2p-dataset/sample/
ls -lh ./data/quick-canvas-dataset/sample/
```
---


## Run Train using quick canvas dataset

Create a file, eg, `my_trainer.py` and use examples and modify your configs to run the file.  

**Example Code**
```python
from mu.algorithms.esd.algorithm import ESDAlgorithm
from mu.algorithms.esd.configs import (
    esd_train_mu,
)

algorithm = ESDAlgorithm(
    esd_train_mu,
    ckpt_path="machine_unlearning/models/compvis/style50/compvis.ckpt",
    raw_dataset_dir=(
        "data/quick-canvas-dataset/sample"
    ),
    template_name = "Abstractionism", #concept to erase
    dataset_type = "unlearncanvas" ,
    use_sample = True, #train on sample dataset
    output_dir = "outputs/esd/finetuned_models" #output dir to save finetuned models
    
)
algorithm.run()
```

## Run Train using i2p dataset

Create a file, eg, `my_trainer.py` and use examples and modify your configs to run the file.  

**Example Code**
```python
from mu.algorithms.esd.algorithm import ESDAlgorithm
from mu.algorithms.esd.configs import (
    esd_train_i2p,
)

algorithm = ESDAlgorithm(
    esd_train_i2p,
    ckpt_path="models/compvis/style50/compvis.ckpt",
    raw_dataset_dir = "data/i2p-dataset/sample",
    template_name = "self-harm", #concept to erase
    dataset_type = "i2p" ,
    use_sample = True, #train on sample dataset
    output_dir = "outputs/esd/finetuned_models" #output dir to save finetuned models
    
)
algorithm.run()
```

**Running the Training Script in Offline Mode**

```bash
WANDB_MODE=offline python my_trainer.py
```

**How It Works** 
* Default Values: The script first loads default values from the train config file as in configs section.

* Parameter Overrides: Any parameters passed directly to the algorithm, overrides these configs.

* Final Configuration: The script merges the configs and convert them into dictionary to proceed with the training. 

## Directory Structure

- `algorithm.py`: Implementation of the ESDAlgorithm class.
- `configs/`: Contains configuration files for training and generation.
- `constants/const.py`: Constants used throughout the project.
- `model.py`: Implementation of the ESDModel class.
- `scripts/train.py`: Script to train the ESD algorithm.
- `trainer.py`: Implementation of the ESDTrainer class.
- `utils.py`: Utility functions used in the project.
---

### Description of arguments being used in train_config class

These are the configuration used for training a Stable Diffusion model using the ESD (Erase Stable Diffusion) method. It defines various parameters related to training, model setup, dataset handling, and output configuration. Below is a detailed description of each section and parameter:

**Training Parameters**

These parameters control the fine-tuning process, including the method of training, guidance scales, learning rate, and iteration settings.

* train_method: Specifies the method of training to decide which parts of the model to update.

    * Type: str
    * Choices: noxattn, selfattn, xattn, full, notime, xlayer, selflayer
    * Example: xattn

* start_guidance: Guidance scale for generating initial images during training. Affects the diversity of the training set.

    * Type: float
    * Example: 0.1

* negative_guidance: Guidance scale for erasing the target concept during training.

    * Type: float
    * Example: 0.0

* iterations: Number of training iterations (similar to epochs).

    * Type: int
    * Example: 1

* lr: Learning rate used by the optimizer for fine-tuning.

    * Type: float
    * Example: 5e-5

* image_size: Size of images used during training and sampling (in pixels).

    * Type: int
    * Example: 512

* ddim_steps: Number of diffusion steps used in the DDIM sampling process.

    * Type: int
    * Example: 50


**Model Configuration**

These parameters specify the Stable Diffusion model checkpoint and configuration file.

* model_config_path: Path to the YAML file defining the model architecture and parameters.

    * Type: str
    * Example: mu/algorithms/esd/configs/model_config.yaml

* ckpt_path: Path to the finetuned Stable Diffusion model checkpoint.

    * Type: str
    * Example: '../models/compvis/style50/compvis.ckpt'


**Dataset Configuration**

These parameters define the dataset type and template for training, specifying whether to focus on objects, styles, or inappropriate content.

* dataset_type: Type of dataset used for training.

    * Type: str
    * Choices: unlearncanvas, i2p
    * Example: unlearncanvas

* template: Type of concept or style to erase during training.

    * Type: str
    * Choices: object, style, i2p
    * Example: style

* template_name: Specific name of the object or style to erase (e.g., "Abstractionism").

    * Type: str
    * Example Choices: Abstractionism, self-harm
    * Example: Abstractionism


**Output Configuration**

These parameters control where the outputs of the training process, such as fine-tuned models, are stored.

* output_dir: Directory where the fine-tuned model and training results will be saved.

    * Type: str
    * Example: outputs/esd/finetuned_models

* separator: Separator character used to handle multiple prompts during training. If set to null, no special handling occurs.

    * Type: str or null
    * Example: null

**Device Configuration**

These parameters define the compute resources for training.

* devices: Specifies the CUDA devices used for training. Provide a comma-separated list of device IDs.

    * Type: str
    * Example: 0,1

* use_sample: Boolean flag indicating whether to use a sample dataset for testing or debugging.

    * Type: bool
    * Example: True


#### ESD Evaluation Framework

This section provides instructions for running the **evaluation framework** for the ESD algorithm on Stable Diffusion models. The evaluation framework is used to assess the performance of models after applying machine unlearning.


#### **Running the Evaluation Framework**

You can run the evaluation framework using the `evaluate.py` script located in the `mu/algorithms/esd/scripts/` directory. Work within the same environment used to perform unlearning for evaluation as well.


### **Basic Command to Run Evaluation:**

**Before running evaluation, download the classifier ckpt from here:**

https://drive.google.com/drive/folders/1AoazlvDgWgc3bAyHDpqlafqltmn4vm61 

Add the following code to `evaluate.py`.

```python
from mu.algorithms.esd import ESDAlgorithm
from mu.algorithms.esd.configs import (
    esd_evaluation_config
)
from evaluation.metrics.accuracy import accuracy_score
from evaluation.metrics.fid import fid_score


evaluator = ESDAlgorithm(
    esd_evaluation_config,
    ckpt_path="outputs/esd/finetuned_models/esd_Bricks_model.pth",
)
generated_images_path = evaluator.generate_images()

accuracy = accuracy_score(gen_image_dir=generated_images_path,
                          dataset_type = "unlearncanvas",
                        classifier_ckpt_path = "/home/ubuntu/Projects/models/classifier_ckpt_path/style50_cls.pth",
                          forget_theme="Bricks",
                          seed_list = ["188"] )
print(accuracy['acc'])
print(accuracy['loss'])

reference_image_dir = "data/quick-canvas-dataset/sample"
fid, _ = fid_score(generated_image_dir=generated_images_path,
                reference_image_dir=reference_image_dir )

print(fid)
```

**Run the script**

```bash
python evaluate.py
```




#### **Description of parameters in evaluation_config.yaml**

The `evaluation_config.yaml` file contains the necessary parameters for running the ESD evaluation framework. Below is a detailed description of each parameter along with examples.

---

### **Model Configuration:**
- ckpt_path : Path to the finetuned Stable Diffusion checkpoint file to be evaluated.  
   - *Type:* `str`  
   - *Example:* `"outputs/esd/finetuned_models/esd_Abstractionism_model.pth"`

- classification_model : Specifies the classification model used for evaluating the generated outputs.  
   - *Type:* `str`  
   - *Example:* `"vit_large_patch16_224"`

---

### **Training and Sampling Parameters:**
- devices : CUDA device IDs to be used for the evaluation process.  
   - *Type:* `str`  
   - *Example:* `"0"`  

- cfg_text : Classifier-free guidance scale value for image generation. Higher values increase the strength of the conditioning prompt.  
   - *Type:* `float`  
   - *Example:* `9.0`  

- seed : Random seed for reproducibility of results.  
   - *Type:* `int`  
   - *Example:* `188`

- ddim_steps : Number of steps for the DDIM (Denoising Diffusion Implicit Models) sampling process.  
   - *Type:* `int`  
   - *Example:* `100`

- ddim_eta : DDIM eta value for controlling the amount of randomness during sampling. Set to `0` for deterministic sampling.  
   - *Type:* `float`  
   - *Example:* `0.0`

- image_height : Height of the generated images in pixels.  
   - *Type:* `int`  
   - *Example:* `512`

- image_width : Width of the generated images in pixels.  
   - *Type:* `int`  
   - *Example:* `512`

---

### **Output and Logging Parameters:**
- sampler_output_dir : Directory where generated images will be saved during evaluation.  
   - *Type:* `str`  
   - *Example:* `"outputs/eval_results/mu_results/esd/"`
---


### **Optimization Parameters:**
- forget_theme : Concept or style intended for removal in the evaluation process.  
   - *Type:* `str`  
   - *Example:* `"Bricks"`

- use_sample: If you want to just run on sample dataset then set it as True. By default it is True.
   - *Type:* `bool`  
   - *Example:* `True`



