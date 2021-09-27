# RLlib

MiniHack additionally provides support for agents using the [RLlib](https://docs.ray.io/en/latest/rllib.html) library. RLlib is an open-source library for reinforcement learning that offers  high scalability and a unified API for a variety of applications. RLlib natively supports TensorFlow, TensorFlow Eager, and PyTorch. RLlib includes implementations of many popular algorithms, including IMPALA, PPO, Rainbow DQN, A3C, and many more. The full list of algorithms is available [here](https://docs.ray.io/en/latest/rllib-toc.html#algorithms).

For further details, checkout out RLlib [paper](https://arxiv.org/abs/1712.09381) and [blog post](https://docs.ray.io/en/latest/rllib-examples.html#blog-posts).

## Installation

To install and train an RLlib agent use the following commands:
```bash
pip install -e ".[rllib]"
# Test DQN run
python3 -m minihack.agent.rllib.train algo=dqn env=MiniHack-Room-5x5-v0 total_steps=1000000 lr=0.000001
```

## Running Experiments

We use the [hydra](https://github.com/facebookresearch/hydra) framework for configuring our experiments. All environment and training parameters can be specified using command line arguments (or edited directly in `config.yaml`). See `config.yaml` file in  `minihack.agent.rllib` for more information. Be sure to set up appropriate parameters for logging with [wandb](https://wandb.ai/site) (disabled by default).

```bash
# Single A2C run
python3 -m minihack.agent.rllib.train algo=a2c env=MiniHack-Room-15x15-v0 total_steps=1000000 a2c.entropy_coeff=0.001 lr=0.00001

# Single PPO run
python3 -m minihack.agent.rllib.train algo=ppo env=MiniHack-Room-15x15-v0 total_steps=1000000 ppo.entropy_coeff=0.0001 lr=0.00001

# Single DQN run
python3 -m minihack.agent.rllib.train algo=dqn env=MiniHack-Room-15x15-v0 total_steps=1000000 dqn.buffer_size=100000 lr=0.000001

# To perform a sweep on the cluster: add another --multirun command and comma-separate values
python3 -m minihack.agent.rllib.train --multirun algo=a2c env=MiniHack-Room-15x15-v0 lr=0.00001 seed=0,1,2,3,4 total_steps=5000000
```