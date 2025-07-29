# Semi Permeable Membrane Algorithm for Machine Unlearning

This repository provides an implementation of the semipermeable membrane algorithm for machine unlearning in Stable Diffusion models. The semipermeable membrane algorithm allows you to remove specific concepts or styles from a pre-trained model without retraining it from scratch.


## Installation

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
## Usage

To train the Semi Permeable Membrane algorithm to unlearn a specific concept or style from the Stable Diffusion model, use the `train.py` script located in the `scripts` directory.

## Run Train
Create a file, eg, `my_trainer.py` and use examples and modify your configs to run the file.  

**Example Code**

**Using quick canvas dataset**


```python

from mu.algorithms.semipermeable_membrane.algorithm import (
    SemipermeableMembraneAlgorithm,
)
from mu.algorithms.semipermeable_membrane.configs import (
    semipermiable_membrane_train_mu,
    SemipermeableMembraneConfig,
)

algorithm = SemipermeableMembraneAlgorithm(
    semipermiable_membrane_train_mu,
    output_dir="/opt/dlami/nvme/outputs",
    train={"iterations": 2},
    use_sample = True # to run on sample dataset
    
)
algorithm.run()
```

**Using quick canvas dataset**


```python

from mu.algorithms.semipermeable_membrane.algorithm import (
    SemipermeableMembraneAlgorithm,
)
from mu.algorithms.semipermeable_membrane.configs import (
    semipermiable_membrane_train_i2p,
    SemipermeableMembraneConfig,
)

algorithm = SemipermeableMembraneAlgorithm(
    semipermiable_membrane_train_i2p,
    output_dir="/opt/dlami/nvme/outputs",
    train={"iterations": 2},
    use_sample = True # to run on sample dataset
    dataset_type = "i2p",
    template_name = "self-harm",
    
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

- `algorithm.py`: Implementation of the Semi Permeable MembraneAlgorithm class.
- `configs/`: Contains configuration files for training and generation.
- `model.py`: Implementation of the Semi Permeable MembraneModel class.
- `scripts/train.py`: Script to train the Semi Permeable Membrane algorithm.
- `trainer.py`: Implementation of the Semi Permeable MembraneTrainer class.
- `utils.py`: Utility functions used in the project.
- `data_handler.py` : Implementation of DataHandler class

---
### Description of Arguments in train_config.yaml

**pretrained_model**

* ckpt_path: File path to the pretrained model's checkpoint file.

* v2: Boolean indicating whether the pretrained model is version 2 or not.

* v_pred: Boolean to enable/disable "v-prediction" mode for diffusion models.

* clip_skip: Number of CLIP layers to skip during inference.

**network**

* rank: Rank of the low-rank adaptation network.

* alpha: Scaling factor for the network during training.


**train**

* precision: Numerical precision to use during training (e.g., float32 or float16).

* noise_scheduler: Type of noise scheduler to use in the training loop (e.g., ddim).

* iterations: Number of training iterations.

* batch_size: Batch size for training.

* lr: Learning rate for the training optimizer.

* unet_lr: Learning rate for the U-Net model.

* text_encoder_lr: Learning rate for the text encoder.

* optimizer_type: Optimizer to use for training (e.g., AdamW8bit).

* lr_scheduler: Learning rate scheduler to apply during training.

* lr_warmup_steps: Number of steps for linear warmup of the learning rate.

* lr_scheduler_num_cycles: Number of cycles for a cosine-with-restarts scheduler.

* max_denoising_steps: Maximum denoising steps to use during training.

**save**

* per_steps: Frequency of saving the model (in steps).

* precision: Numerical precision for saved model weights


**other**

* use_xformers: Boolean to enable xformers memory-efficient attention.

* wandb_project and wandb_run

* Configuration for tracking the training progress using Weights & Biases.

* wandb_project: Project name in W&B.

* wandb_run: Specific run name in the W&B dashboard.

**use_sample**

* Boolean to indicate whether to use the sample dataset for training.

**dataset_type**

* Type of dataset to use, options are unlearncanvas or i2p.

**template**
* Specifies the template type, choices are:
    * object: Focus on specific objects.
    * style: Focus on artistic styles.
    * i2p: Intermediate style processing.

**template_name**

* Name of the template, choices are:
    * self-harm
    * Abstractionism

**prompt**

* target: Target template or concept to guide training (references template_name).

* positive: Positive prompt based on the template.

* unconditional: Unconditional prompt text.

* neutral: Neutral prompt text.

* action: Specifies the action applied to the prompt (e.g., erase_with_la).

* guidance_scale: Guidance scale for classifier-free guidance.

* resolution: Image resolution for training.

* batch_size: Batch size for generating prompts.

* dynamic_resolution: Boolean to allow dynamic resolution.

* la_strength: Strength of local adaptation.

* sampling_batch_size: Batch size for sampling images.

**devices**

* CUDA devices to use for training (specified as a comma-separated list, e.g., "0,1").

**output_dir**

* Directory to save the fine-tuned model and other outputs.

**verbose**

* Boolean flag for verbose logging during training.



#### Semipermeable membrane Evaluation Framework

This section provides instructions for running the **evaluation framework** for the Semipermeable membrane algorithm on Stable Diffusion models. The evaluation framework is used to assess the performance of models after applying machine unlearning.


#### **Running the Evaluation Framework**

You can run the evaluation framework using the `evaluate.py` script located in the `mu/algorithms/semipermeable_membrane/scripts/` directory. Work within the same environment used to perform unlearning for evaluation as well.


### **Basic Command to Run Evaluation:**

**Before running evaluation, download the classifier ckpt from here:**

https://drive.google.com/drive/folders/1AoazlvDgWgc3bAyHDpqlafqltmn4vm61 

Add the following code to `evaluate.py`

```python
from mu.algorithms.semipermeable_membrane import SemipermeableMembraneEvaluator
from mu.algorithms.semipermeable_membrane.configs import (
    semipermeable_membrane_eval_config
)
from evaluation.metrics.accuracy import accuracy_score
from evaluation.metrics.fid import fid_score


evaluator = SemipermeableMembraneEvaluator(
    semipermeable_membrane_eval_config,
    spm_path = ["outputs/semipermiable/semipermeable_membrane_Abstractionism_last.safetensors"],
)
generated_images_path = evaluator.generate_images()

reference_image_dir = "/home/ubuntu/Projects/Palistha/testing/data/quick-canvas-dataset/sample"

accuracy = accuracy_score(gen_image_dir=generated_images_path,
                          dataset_type = "unlearncanvas",
                          classifier_ckpt_path = "/home/ubuntu/Projects/models/classifier_ckpt_path/style50_cls.pth",
                          reference_dir=reference_image_dir,
                          forget_theme="Bricks",
                          seed_list = ["188"] )
print(accuracy['acc'])
print(accuracy['loss'])

fid, _ = fid_score(generated_image_dir=generated_images_path,
                reference_image_dir=reference_image_dir )

print(fid)
```

**Run the script**

```bash
python evaluate.py
```


#### **Description of parameters in evaluation_config.yaml**

The `evaluation_config.yaml` file contains the necessary parameters for running the Semipermeable membrane evaluation framework. Below is a detailed description of each parameter along with examples.

---

### **Model Configuration Parameters:**
- spm_path: paths to finetuned model checkpoint.
   - *Type:* `list`
   - *Example:* `outputs/semipermeable_membrane/finetuned_models/semipermeable_membrane_Abstractionism_last.safetensors`


- precision : Specifies the numerical precision for model computation.  
   - *Type:* `str`  
   - *Options:* `"fp32"`, `"fp16"`, `"bf16"`  
   - *Example:* `"fp32"`  

- spm_multiplier:  Specifies the multiplier for Semipermeable Membrane (SPM) model.  
   - *Type:* `float`  
   - *Example:* `1.0`  

- v2 : Specifies whether to use version 2.x of the model.  
   - *Type:* `bool`  
   - *Example:* `false`  

- matching_metric : Metric used for evaluating the similarity between generated prompts and erased concepts.  
   - *Type:* `str`  
   - *Options:* `"clipcos"`, `"clipcos_tokenuni"`, `"tokenuni"`  
   - *Example:* `"clipcos_tokenuni"`  

- model_config : Path to the model configuration YAML file.  
   - *Type:* `str`  
   - *Example:* `"mu/algorithms/semipermeable_membrane/config"`  

- model_ckpt_path: Path to pretrained Stable Diffusion model.
   - *Type*: `str`
   - *Example*: `models/diffuser/style50`

---

### **Sampling Parameters:**

- seed : Random seed for reproducibility of the evaluation process.  
   - *Type:* `int`  
   - *Example:* `188`  

- devices : Specifies the CUDA devices for running the model.  
   - *Type:* `str` (Comma-separated for multiple devices)  
   - *Example:* `"0"`  

- task : Specifies the task type for the evaluation process.  
   - *Type:* `str`  
   - *Options:* `"class"`, `"style"`  
   - *Example:* `"class"`  

---

### **Output Parameters:**
- sampler_output_dir : Directory where generated images will be saved during the sampling process.  
   - *Type:* `str`  
   - *Example:* `"outputs/eval_results/mu_results/semipermeable_membrane/"`  

---

### **Dataset and Classification Parameters:**
- reference_dir : Path to the reference dataset used for evaluation and comparison.  
   - *Type:* `str`  
   - *Example:* `"msu_unlearningalgorithm/data/quick-canvas-dataset/sample/"`  

- classification_model : Specifies the classification model used for the evaluation.  
   - *Type:* `str`  
   - *Example:* `"vit_large_patch16_224"`  

- forget_theme : Specifies the theme to be forgotten during the unlearning process.  
   - *Type:* `str`  
   - *Example:* `"Bricks"`  

---

### **Performance Parameters:**

- seed_list :  List of random seeds for multiple evaluation trials.  
   - *Type:* `list`  
   - *Example:* `["188"]`  

- use_sample: If you want to just run on sample dataset then set it as True. By default it is True.
   - *Type:* `bool`  
   - *Example:* `True`
