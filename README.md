# MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research

<!-- <p align="center">
 <img width="70%" src="docs/img/minihack.png" />
</p> -->

<p align="center">
  <a href="https://pypi.python.org/pypi/minihack/">
    <img src="https://img.shields.io/pypi/v/minihack.svg" />
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" />
  </a>
  <a href="https://minihack.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/minihack/badge/?version=latest" />
  </a>
   <a href="https://github.com/facebookresearch/minihack/actions/workflows/test_and_deploy.yml">
    <img src="https://github.com/facebookresearch/minihack/actions/workflows/test_and_deploy.yml/badge.svg?branch=main" />
  </a>
 </p>
 
 ![MiniHack Environments](/docs/imgs/minihack_envs.png)

MiniHack is a sandbox framework for easily designing rich and diverse environments for Reinforcement Learning (RL).
Based on the game of [NetHack](https://en.wikipedia.org/wiki/NetHack), arguably the hardest grid-based game in the world, MiniHack uses the [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle) to communicate with the game and provide a convenient interface for customly created RL tesbeds. Please refer to the accompanying [paper](https://openreview.net/pdf?id=skFwlyefkWJ) for the outline of our motivation for MiniHack.

MiniHack already comes with a large list of challenging [tasks](./docs/envs/tasks.md). However, it is primarily built for easily designing new ones.
The motivation behind MiniHack is to be able to perform RL experiments in a controlled setting while being able to increasingly scale the complexity of the tasks.

To this end, MiniHack leverages the [description files of NetHack](https://nethackwiki.com/wiki/Des-file_format). The description files (or des-files) are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc.  The des-files can be compiled into binary using the NetHack level compiler, and MiniHack maps them to [Gym environments](https://github.com/openai/gym). We refer users to our [brief overview](https://minihack.readthedocs.io/en/latest/getting-started/des_files.html), [detailed tutorial](https://minihack.readthedocs.io/en/latest/tutorials/des_file_tutorial.html), or [interactive notebook](./docs/tutorials/des_file_tutorial.ipynb) for further information on des-files.

[Our documentation](https://minihack.readthedocs.io/) will walk you through everything you need to know about MiniHack, step-by-step, including information on how to get started, configure environments or design new ones, train baseline agents, and much more.

# Installation

MiniHack is available on [pypi](https://pypi.org/project/minihack/) and can be installed as follows:
```bash
pip install minihack
```

We advise using a conda environment for this:

```bash
conda create -n minihack python=3.8
conda activate minihack
pip install minihack
```

**NOTE:** NLE requires `cmake>=3.15` to be installed when building the package. Checkout out [here](https://github.com/facebookresearch/nle#installation) how to install it in __MacOS__ and __Ubuntu 18.04__. __Windows__ users should use [Docker](#docker).

**NOTE:** Baseline agents have separate installation instructions. See [here](#baseline-agents) for more details.

### Extending MiniHack

If you wish to extend MiniHack, please install the package as follows:

```bash
git clone https://github.com/facebookresearch/minihack
cd minihack
pip install -e ".[dev]"
pre-commit install
```

### Docker

We have provided several Dockerfiles for building images with pre-installed MiniHack. Please follow the instructions described [here](./docker/README.md).

# Trying out MiniHack

MiniHack uses the popular [Gym interface](https://github.com/openai/gym) for the interactions between the agent and the environment.
A pre-registered MiniHack environment can be used as follows:

```python
import gym
import minihack
env = gym.make("MiniHack-River-v0")
env.reset() # each reset generates a new environment instance
env.step(1)  # move agent '@' north
env.render()
```

To see the list of all [MiniHack environments](./docs/envs/tasks.md), run:

```bash
python -m minihack.scripts.env_list
```

The following scripts allow to play MiniHack environments with a keyboard:

```bash
# Play the MiniHack in the Terminal as a human
python -m minihack.scripts.play --env MiniHack-River-v0

# Use a random agent
python -m minihack.scripts.play --env MiniHack-River-v0  --mode random

# Play the MiniHack with graphical user interface (gui)
python -m minihack.scripts.play_gui --env MiniHack-River-v0
```

**NOTE:** If the package has been properly installed one could run the scripts above with `mh-envs`, `mh-play`, and `mh-guiplay` commands.

# Baseline Agents

In order to get started with MiniHack environments, we provide a variety of baselines agent integrations.

### TorchBeast
A [TorchBeast](https://github.com/facebookresearch/torchbeast) agent is
bundled in `minihack.agent.polybeast` together with a simple model to provide
a starting point for experiments. To install and train this agent, first
install torchbeast by following the instructions [here](https://github.com/facebookresearch/torchbeast#installing-polybeast),
then use the following commands:
``` bash
pip install ".[polybeast]"
python3 -m minihack.agent.polybeast.polyhydra env=small_room_random learning_rate=0.0001 use_lstm=true total_steps=1000000
```

More information on running our TorchBeast agents, and instructions on how to reproduce
the results of the paper, can be found [here](./docs/agents/torchbeast.md).
The learning curves for all of our polybeast experiments can be accessed in our [Weights&Biases repository](https://wandb.ai/minihack).

### RLlib

An [RLlib](https://github.com/ray-project/ray#rllib-quick-start) agent is
provided in `minihack.agent.rllib`, with a similar model to the torchbeast agent.
This can be used to try out a variety of different RL algorithms. To install and train an RLlib agent, use the following
commands:
```bash
pip install ".[rllib]"
python -m minihack.agent.rllib.train algo=dqn
```

More information on running RLlib agents can be found [here](./docs/agents/rllib.md).

### Unsupervised Environment Design

MiniHack also enables research in *Unsupervised Environment Design*, whereby an adaptive task distribution is learned during training by dynamically adjusting free parameters of the task MDP. 
Check out the [`ucl-dark/paired`](https://github.com/ucl-dark/paired) repository for replicating the examples from the paper using the [PAIRED](https://arxiv.org/abs/2012.02096).

# Citation

If you use MiniHack in your work, please cite:

```
@inproceedings{samvelyan2021minihack,
  title={MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research},
  author={Mikayel Samvelyan and Robert Kirk and Vitaly Kurin and Jack Parker-Holder and Minqi Jiang and Eric Hambro and Fabio Petroni and Heinrich Kuttler and Edward Grefenstette and Tim Rockt{\"a}schel},
  booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 1)},
  year={2021},
  url={https://openreview.net/forum?id=skFwlyefkWJ}
}
```

If you use our example ported environments, please cite the original papers: [MiniGrid](https://github.com/maximecb/gym-minigrid/) (see [license](https://github.com/maximecb/gym-minigrid/blob/master/LICENSE), [bib](https://github.com/maximecb/gym-minigrid/#minimalistic-gridworld-environment-minigrid)), [Boxoban](https://github.com/deepmind/boxoban-levels/) (see [license](https://github.com/deepmind/boxoban-levels/blob/master/LICENSE), [bib](https://github.com/deepmind/boxoban-levels/#bibtex)).

# Contributions and Maintenance

We welcome contributions to MiniHack. If you are interested in contributing, please see [this document](./CONTRIBUTING.md). Our maintenance plan can be found [here](./MAINTENANCE.md).

# Papers using the MiniHack

- Powers et al. [CORA: Benchmarks, Baselines, and a Platform for Continual Reinforcement Learning Agents](https://openreview.net/forum?id=Fr_KF_lMCMr) (CMU, Georgia Tech, AI2, August 2021)
- Samvelyan et al. [MiniHack The Planet](https://openreview.net/pdf?id=skFwlyefkWJ) (FAIR, UCL, Oxford, NeurIPS 2021)

Open a [pull request](https://github.com/facebookresearch/minihack/edit/main/README.md) to add papers.
