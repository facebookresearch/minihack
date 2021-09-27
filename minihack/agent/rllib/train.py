# Copyright (c) Facebook, Inc. and its affiliates.

import os
from collections.abc import Iterable
from numbers import Number

import hydra
import minihack.agent.rllib.models  # noqa: F401
from minihack.agent.common.envs import tasks
from minihack.agent import is_env_registered, get_env_shortcut
import numpy as np
import ray
import ray.tune.integration.wandb
from minihack.agent.rllib.envs import RLLibNLEEnv  # noqa: F401
from omegaconf import DictConfig, OmegaConf
from ray import tune
from ray.rllib.models.catalog import MODEL_DEFAULTS
from ray.rllib.agents import a3c, dqn, impala, ppo
from ray.tune.integration.wandb import (
    _VALID_ITERABLE_TYPES,
    _VALID_TYPES,
    WandbLoggerCallback,
)
from ray.tune.registry import register_env
from ray.tune.utils import merge_dicts


def get_full_config(cfg: DictConfig) -> DictConfig:
    env_flags = OmegaConf.to_container(cfg)
    env_flags["seedspath"] = ""
    return OmegaConf.create(env_flags)


NAME_TO_TRAINER: dict = {
    "impala": (impala.DEFAULT_CONFIG.copy(), impala.ImpalaTrainer),
    "a2c": (a3c.a2c.A2C_DEFAULT_CONFIG.copy(), a3c.A2CTrainer),
    "dqn": (dqn.DEFAULT_CONFIG.copy(), dqn.DQNTrainer),
    "ppo": (ppo.DEFAULT_CONFIG.copy(), ppo.PPOTrainer),
}


@hydra.main(config_path=".", config_name="config")
def train(cfg: DictConfig) -> None:
    ray.init(num_gpus=cfg.num_gpus, num_cpus=cfg.num_cpus + 1)
    cfg = get_full_config(cfg)
    register_env("RLlibNLE-v0", RLLibNLEEnv)

    try:
        config, trainer = NAME_TO_TRAINER[cfg.algo]
    except KeyError as error:
        raise ValueError(
            "The algorithm you specified isn't currently supported: %s",
            cfg.algo,
        ) from error

    args_config = OmegaConf.to_container(cfg)

    # Algo-specific config. Requires hydra config keys to match rllib exactly
    algo_config = args_config.pop(cfg.algo)

    # Remove unnecessary config keys
    for algo in NAME_TO_TRAINER.keys():
        if algo != cfg.algo:
            args_config.pop(algo, None)

    # Merge config from hydra (will have some rogue keys but that's ok)
    config = merge_dicts(config, args_config)

    # check the name of the environment
    if cfg.env not in tasks.ENVS:
        if is_env_registered(cfg.env):
            cfg.env = get_env_shortcut(cfg.env)
        else:
            raise KeyError(
                f"Could not find an environement with a name: {cfg.env}."
            )

    # Update configuration with parsed arguments in specific ways
    config = merge_dicts(
        config,
        {
            "framework": "torch",
            "num_gpus": cfg.num_gpus,
            "seed": cfg.seed,
            "env": "RLlibNLE-v0",
            "env_config": {
                "flags": cfg,
                "observation_keys": cfg.obs_keys.split(","),
                "name": cfg.env,
            },
            "train_batch_size": cfg.train_batch_size,
            "model": merge_dicts(
                MODEL_DEFAULTS,
                {
                    "custom_model": "rllib_nle_model",
                    "custom_model_config": {"flags": cfg, "algo": cfg.algo},
                    "use_lstm": cfg.use_lstm,
                    "lstm_use_prev_reward": True,
                    "lstm_use_prev_action": True,
                    "lstm_cell_size": cfg.hidden_dim,
                },
            ),
            "num_workers": cfg.num_cpus,
            "num_envs_per_worker": int(cfg.num_actors / cfg.num_cpus),
            "evaluation_interval": 100,
            "evaluation_num_episodes": 50,
            "evaluation_config": {"explore": False},
            "rollout_fragment_length": cfg.unroll_length,
        },
    )

    # Merge algo-specific config at top level
    config = merge_dicts(config, algo_config)

    # Ensure we can use the config we've specified above
    trainer_class = trainer.with_updates(default_config=config)

    callbacks = []
    if cfg.wandb:
        callbacks.append(
            WandbLoggerCallback(
                project=cfg.project,
                api_key_file="~/.wandb_api_key",
                entity=cfg.entity,
                group=cfg.group,
                tags=cfg.tags.split(","),
            )
        )
        os.environ[
            "TUNE_DISABLE_AUTO_CALLBACK_LOGGERS"
        ] = "1"  # Only log to wandb

    # Hacky monkey-patching to allow for OmegaConf config
    def _is_allowed_type(obj):
        """Return True if type is allowed for logging to wandb"""
        if isinstance(obj, DictConfig):
            return True
        if isinstance(obj, np.ndarray) and obj.size == 1:
            return isinstance(obj.item(), Number)
        if isinstance(obj, Iterable) and len(obj) > 0:
            return isinstance(obj[0], _VALID_ITERABLE_TYPES)
        return isinstance(obj, _VALID_TYPES)

    ray.tune.integration.wandb._is_allowed_type = _is_allowed_type

    tune.run(
        trainer_class,
        stop={"timesteps_total": cfg.total_steps},
        config=config,
        name=cfg.name,
        callbacks=callbacks,
    )


if __name__ == "__main__":
    train()
