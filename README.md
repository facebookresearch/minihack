# MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research

[![Documentation Status](https://readthedocs.org/projects/minihack/badge/?version=latest)](https://minihack.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

![MiniHack Environments](/docs/imgs/minihack_envs.png)

MiniHack is a sandbox framework for easily designing rich and diverse environments for Reinforcement Learning (RL) research.
Based on the game of [NetHack](https://en.wikipedia.org/wiki/NetHack), arguably the hardest grid-based game in the world, MiniHack uses the [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle) to communicate with the game and provide a convenient interface for customly created RL tesbeds.

MiniHack already comes with a large list of challenging [tasks](./TASKS.md). However, it is primarily built for easily designing new ones.
The motivation behind MiniHack is to be able to perform RL experiments in a controlled setting while being able to increasingly scale the complexity of the tasks.

To this end, MiniHack leverages the description files of NetHack. The description files (or des-files) are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc. The developers of NetHack created a special domain-specific language for describing the levels of the game, called _des-file format_. The des-files can be compiled into binary using the NetHack level compiler, and MiniHack maps them to [Gym environments](https://github.com/openai/gym). For more information on des-files, we refer users to our [brief overview](https://minihack.readthedocs.io/en/latest/getting-started/des_files.html), [detailed visually-aided tutorial](https://minihack.readthedocs.io/en/latest/tutorials/des_file/index.html), or [interactive notebook](./notebooks/des_file_tutorial.ipynb).

[MiniHack documentation](https://minihack.readthedocs.io/) will walk you through everything you need to know, step-by-step, including information on how to get started with MiniHack, configure environments or design new ones, train baseline agents, use our APi, and much more.

# Installation

MiniHack is available on [pypi](https://pypi.org/project/gym-minigrid/) and can be installed as follows:
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

To see the list of all MiniHack environments, run:

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

Several baseline agents are included as part of MiniHack, which can be
installed and used as follows:

* a [TorchBeast](https://github.com/facebookresearch/torchbeast) agent is
  bundled in `minihack.agent.polybeast` together with a simple model to provide
  a starting point for experiments. To install and train this agent, first
  install torchbeast be following the instructions
  [here](https://github.com/facebookresearch/torchbeast#installing-polybeast),
  then use the following commands:
``` bash
$ pip install ".[polybeast]"
$ python3 -m minihack.agent.polybeast.polyhydra env=small_room_random learning_rate=0.0001 use_lstm=true total_steps=1000000
```

* An [RLlib](https://github.com/ray-project/ray#rllib-quick-start) agent is
  provided in `minihack.agent.rllib`, with a similar model to the torchbeast agent.
  This can be used to try out a variety of different RL algorithms - several
  examples are provided. To install and train this agent use the following
  commands:
```bash
$ pip install ".[rllib]"
$ python -m minihack.agent.rllib.train algo=dqn
```

More information on running these agents, and instructions on how to reproduce
the results of the MiniHack paper, can be found in [this
document](./minihack/agent/README.md).
We also provide baseline learning curves of the MiniHack paper in Weights&Biases format for all of our experiments. They can be accessed [here](https://wandb.ai/minihack).

# Contributions and Maintenance

We welcome contributions to MiniHack. If you are interested in contributing please see [this document](./CONTRIBUTING.md). MiniHack's maintenance plan can be found [here](./MAINTENANCE.md).

# Citation

If you use MiniHack in your work, please cite:

```
@misc{samvelyan2021minihack,
  title={MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research},
  author={Mikayel Samvelyan and Robert Kirk and Vitaly Kurin and Jack Parker-Holder and Minqi Jiang and Eric Hambro and Fabio Petroni and Heinrich Kuttler and Edward Grefenstette and Tim Rockt{\"a}schel},
  year={2021},
  url={https://openreview.net/forum?id=skFwlyefkWJ}
}
```

If you use MiniHack's interface on environments ported from other benchmarks, please cite the original paper as well: [MiniGrid](https://github.com/maximecb/gym-minigrid/) (see [license](https://github.com/maximecb/gym-minigrid/blob/master/LICENSE), [bibtex](https://github.com/maximecb/gym-minigrid/#minimalistic-gridworld-environment-minigrid)), [Boxoban](https://github.com/deepmind/boxoban-levels/) (see [license](https://github.com/deepmind/boxoban-levels/blob/master/LICENSE), [bibtex](https://github.com/deepmind/boxoban-levels/#bibtex)).

<!-- # Papers using the MiniHack
- Samvelyan et al. [MiniHack The Planet](https://arxiv.org/abs/20XX.YYYY) (FAIR, UCL, Oxford)

Open a [pull request](https://github.com/facebookresearch/minihack/edit/master/README.md) to add papers. -->
