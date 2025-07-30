# mu/algorithms/selective_amnesia/trainer.py

import sys
import os
import signal
import pudb
import argparse
import logging

from pathlib import Path
from typing import Dict
from torch.nn import MSELoss
from torch.optim import Adam
from tqdm import tqdm
from pytorch_lightning import seed_everything
from packaging import version
import pytorch_lightning as pl
from omegaconf import OmegaConf
from pytorch_lightning.trainer import Trainer

from models import stable_diffusion
sys.modules['stable_diffusion'] = stable_diffusion

from stable_diffusion.ldm.util import instantiate_from_config
from mu.algorithms.selective_amnesia.utils import convert_paths
from mu.algorithms.selective_amnesia.data_handler import SelectiveAmnesiaDataHandler
from mu.core.base_trainer import BaseTrainer


class SelectiveAmnesiaTrainer(BaseTrainer):
    """
    Trainer for the Selective Amnesia algorithm.
    Incorporates EWC loss and other SA-specific training logic.

    Heng, A., & Soh, H. (2023).

    Selective Amnesia: A Continual Learning Approach to Forgetting in Deep Generative Models

    https://arxiv.org/abs/2305.10120
    """

    def __init__(self, model, config: Dict, device: str, config_path: str, **kwargs):
        """
        Initialize the SelectiveAmnesiaTrainer.

        Args:
            model: Instance of SelectiveAmnesiaModel or a similar model class.
            config (dict): Configuration dictionary with training parameters.
            device (str): Device to perform training on (e.g. 'cuda:0').
            data_handler: An instance of ConceptAblationDataHandler or a similar data handler.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(model, config, **kwargs)
        self.device = device
        self.model = model.model
        self.model_config_path = model.model_config_path
        self.config_path = config_path
        self.opt_config = config
        self.logger = logging.getLogger(__name__)
        self.setup_optimizer()

    def setup_optimizer(self, *args, **kwargs):
        """
        Setup the optimizer based on the training configuration.
        Adjust parameter groups or other attributes as per concept ablation needs.
        """
        pass

        
    def train(self):
        """
        Execute the training loop.
        """
        # configs = [
        #     OmegaConf.load(cfg) for cfg in [self.config_path, self.model_config_path]
        # ]
        # config = OmegaConf.merge(*configs)
        clean_config = convert_paths(self.config_path) #fix the posixpath
        dict_config = OmegaConf.create(clean_config)
        file_config = OmegaConf.load(self.model_config_path)
        config = OmegaConf.merge(dict_config, file_config)

        lightning_config = config.pop("lightning", OmegaConf.create())

        trainer_config = lightning_config.get("trainer", OmegaConf.create())

        trainer_config["accelerator"] = "gpu"

        trainer_config["devices"] = self.opt_config.get("devices")
        trainer_config["strategy"] = "ddp"
        cpu = False

        trainer_opt = argparse.Namespace(**trainer_config)

        lightning_config.trainer = trainer_config

        trainer_kwargs = dict()

        seed = self.opt_config.get("seed", 42)
        wandb_entity = self.opt_config.get("wandb_entity", "")
        output_dir = self.opt_config.get("output_dir", "")

        os.makedirs(output_dir, exist_ok=True)

        ckptdir = os.path.join(output_dir, "checkpoints")
        cfgdir = os.path.join(output_dir, "configs")

        self.logger.info("Starting training...")
        seed_everything(seed)

        # default logger configs
        default_logger_cfgs = {
            "wandb": {
                "target": "pytorch_lightning.loggers.WandbLogger",
                "params": {
                    "project": "quick-canvas-machine-unlearning",
                    "name": f"selective_amnesia_{self.opt_config.get('template_name')}",
                    "save_dir": output_dir,
                    "dir": output_dir,
                    "id": f"selective_amnesia_{self.opt_config.get('template_name')}",
                    "resume": "allow",
                    "entity": "selective-amnesia",
                },
            },
            "tensorboard": {
                "target": "pytorch_lightning.loggers.TensorBoardLogger",
                "params": {
                    "name": "tensorboard",
                    "save_dir": output_dir,
                },
            },
        }

        if wandb_entity is not None:
            default_logger_cfg = default_logger_cfgs["wandb"]
        else:
            default_logger_cfg = default_logger_cfgs["tensorboard"]

        if "logger" in lightning_config:
            logger_cfg = lightning_config.logger
        else:
            logger_cfg = OmegaConf.create()
        logger_cfg = OmegaConf.merge(default_logger_cfg, logger_cfg)
        trainer_kwargs["logger"] = instantiate_from_config(logger_cfg)

        # modelcheckpoint - use TrainResult/EvalResult(checkpoint_on=metric) to
        # specify which metric is used to determine best models
        default_modelckpt_cfg = {
            "target": "pytorch_lightning.callbacks.ModelCheckpoint",
            "params": {
                "dirpath": ckptdir,
                "filename": "{epoch:06}",
                "verbose": True,
                "save_last": True,
            },
        }
        if hasattr(self.model, "monitor"):
            self.logger.info(f"Monitoring {self.model.monitor} as checkpoint metric.")
            default_modelckpt_cfg["params"]["monitor"] = self.model.monitor
            default_modelckpt_cfg["params"]["save_top_k"] = -1

        if "modelcheckpoint" in lightning_config:
            modelckpt_cfg = lightning_config.modelcheckpoint
        else:
            modelckpt_cfg = OmegaConf.create()
        modelckpt_cfg = OmegaConf.merge(default_modelckpt_cfg, modelckpt_cfg)
        self.logger.info(f"Merged modelckpt-cfg: \n{modelckpt_cfg}")

        if version.parse(pl.__version__) < version.parse("1.4.0"):
            trainer_kwargs["checkpoint_callback"] = instantiate_from_config(
                modelckpt_cfg
            )

        # add callback which sets up log directory
        default_callbacks_cfg = {
            "setup_callback": {
                "target": "mu.algorithms.selective_amnesia.callbacks.SetupCallback",
                "params": {
                    "resume": "",
                    "now": f"selective_amnesia_{self.opt_config.get('template_name')}",
                    "logdir": output_dir,
                    "ckptdir": ckptdir,
                    "cfgdir": cfgdir,
                    "config": config,
                    "lightning_config": lightning_config,
                },
            },
            "image_logger": {
                "target": "mu.algorithms.selective_amnesia.callbacks.ImageLogger",
                "params": {"batch_frequency": 750, "max_images": 4, "clamp": True},
            },
            "learning_rate_logger": {
                "target": "mu.algorithms.selective_amnesia.callbacks.LearningRateMonitor",
                "params": {
                    "logging_interval": "step",
                    # "log_momentum": True
                },
            },
            "cuda_callback": {
                "target": "mu.algorithms.selective_amnesia.callbacks.CUDACallback"
            },
        }

        if version.parse(pl.__version__) >= version.parse("1.4.0"):
            default_callbacks_cfg.update({"checkpoint_callback": modelckpt_cfg})

        if "callbacks" in lightning_config:
            callbacks_cfg = lightning_config.callbacks
        else:
            callbacks_cfg = OmegaConf.create()

        callbacks_cfg = OmegaConf.merge(default_callbacks_cfg, callbacks_cfg)
        if ("ignore_keys_callback" in callbacks_cfg) and self.opt_config.get(
            "ckpt_path"
        ):
            callbacks_cfg.ignore_keys_callback.params["ckpt_path"] = (
                self.opt_config.get("ckpt_path")
            )
        elif "ignore_keys_callback" in callbacks_cfg:
            del callbacks_cfg["ignore_keys_callback"]

        trainer_kwargs["callbacks"] = [
            instantiate_from_config(callbacks_cfg[k]) for k in callbacks_cfg
        ]

        trainer = Trainer.from_argparse_args(trainer_opt, **trainer_kwargs)

        trainer.logdir = output_dir

        config.data.params.raw_dataset_dir = self.opt_config.get("raw_dataset_dir")
        config.data.params.processed_dataset_dir = self.opt_config.get(
            "processed_dataset_dir"
        )
        config.data.params.dataset_type = self.opt_config.get("dataset_type")
        config.data.params.template = self.opt_config.get("template")
        config.data.params.template_name = self.opt_config.get("template_name")
        config.data.params.use_sample = self.opt_config.get("use_sample")

        config = SelectiveAmnesiaDataHandler.update_config_based_on_template(
            self.opt_config.get("raw_dataset_dir"),
            self.opt_config.get("processed_dataset_dir"),
            config,
            self.opt_config.get("template"),
            self.opt_config.get("template_name"),
            self.opt_config.get("dataset_type"),
            self.opt_config.get("use_sample"),
        )
        data = instantiate_from_config(config.data)
        data.prepare_data()
        data.setup()

        self.logger.info("#### Data #####")
        for k in data.datasets:
            self.logger.info(
                f"{k}, {data.datasets[k].__class__.__name__}, {len(data.datasets[k])}"
            )

        # configure learning rate
        bs, base_lr = (
            config.data.params.train_batch_size,
            config.model.base_learning_rate,
        )
        if not cpu:
            ngpu = len(lightning_config.trainer.devices.strip(",").split(","))
        else:
            ngpu = 1
        if "accumulate_grad_batches" in lightning_config.trainer:
            accumulate_grad_batches = lightning_config.trainer.accumulate_grad_batches
        else:
            accumulate_grad_batches = 1
        self.logger.info(f"accumulate_grad_batches = {accumulate_grad_batches}")
        lightning_config.trainer.accumulate_grad_batches = accumulate_grad_batches
        if config.get("scale_lr"):
            self.model.learning_rate = accumulate_grad_batches * ngpu * bs * base_lr
            self.logger.info(
                "Setting learning rate to {:.2e} = {} (accumulate_grad_batches) * {} (num_gpus) * {} (batchsize) * {:.2e} (base_lr)".format(
                    self.model.learning_rate, accumulate_grad_batches, ngpu, bs, base_lr
                )
            )
        else:
            self.model.learning_rate = base_lr
            self.logger.info("++++ NOT USING LR SCALING ++++")
            self.logger.info(f"Setting learning rate to {self.model.learning_rate:.2e}")

        # allow checkpointing via USR1

        def melk(*args, **kwargs):
            # run all checkpoint hooks
            if trainer.global_rank == 0:
                self.logger.info("Summoning checkpoint.")
                ckpt_path = os.path.join(ckptdir, "last.ckpt")
                trainer.save_checkpoint(ckpt_path)

        def divein(*args, **kwargs):
            if trainer.global_rank == 0:
                pudb.set_trace()

        signal.signal(signal.SIGUSR1, melk)
        signal.signal(signal.SIGUSR2, divein)

        # run
        try:
            self.model.load_ewc_params()
            trainer.fit(self.model, data)
        except Exception:
            melk()
            raise
