# TorchBeast

To get started with MiniHack environments, we provide baseline agents using the [TorchBeast](#torchbeast) framework.

[TorchBeast](https://github.com/facebookresearch/torchbeast) provides a [PyTorch](https://pytorch.org/) implementation of [IMPALA: Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures](https://arxiv.org/abs/1802.01561).

TorchBeast comes in two variants: MonoBeast and PolyBeast. PolyBeast is the more powerful version of the framework and allows training agents across multiple machines. For further details, see the [TorchBeast paper](https://arxiv.org/abs/1910.03552).

For MiniHack, we use the PolyBeast implementation of TorchBeast and additionally provide an implementation of the following exploration methods:
- [RND: Exploration by Random Network Distillation](https://arxiv.org/abs/1810.12894)
- [RIDE: Rewarding Impact-Driven Exploration for Procedurally-Generated Environments](https://arxiv.org/abs/2002.12292)

## Installation

To install and train a polybeast agent in MiniHack, first install polybeast by following the instructions [here](https://github.com/facebookresearch/torchbeast#installing-polybeast), then use the following commands:

```bash
pip install ".[polybeast]"
# Test IMPALA run
python3 -m minihack.agent.polybeast.polyhydra env=small_room total_steps=100000
```

## Running Experiments

We use the [hydra](https://github.com/facebookresearch/hydra) framework for configuring our experiments. All environment and training parameters can be specified using command line arguments (or edited directly in `config.yaml`). See `config.yaml` file in the polybeast directory for more information. Be sure to set up appropriate parameters for logging with [wandb](https://wandb.ai/site) (disabled by default).


```bash
# Single IMPALA run
python3 -m minihack.agent.polybeast.polyhydra model=baseline env=small_room total_steps=1000000

# Single RND run
python3 -m minihack.agent.polybeast.polyhydra model=rnd env=small_room total_steps=1000000

# Single RND run
python3 -m minihack.agent.polybeast.polyhydra model=ride state_counter=coordinates env=small_room total_steps=1000000

# To perform a sweep on the cluster: add another --multirun command and comma-separate values
python3 -m minihack.agent.polybeast.polyhydra --multirun model=baseline,rnd env=big_room_random,big_room_monster total_steps=10000000
```

The full list of environment name shortcuts can be looked up [here](./env_names.yaml).

## Replicating the Results of the Paper

To replicate results of the paper performed using polybeast, simply run a sweep of 5 runs with IMPALA, RND or RIDE agents on the desired environments as follows:

```bash
python3 -m minihack.agent.polybeast.polyhydra --multirun model=baseline name=1,2,3,4,5 env=big_room_random,big_room_monster total_steps=10000000
```

For navigation tasks, the default parameters are already set. For skill acquisition tasks, additionally set `learning_rate=0.00005 msg.model=lt_cnn`.