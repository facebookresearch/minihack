# MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research

![MiniHack Environments](/docs/imgs/minihack_envs.png)

[![Documentation Status](https://readthedocs.org/projects/minihack/badge/?version=latest)](https://minihack.readthedocs.io/en/latest/?badge=latest)

MiniHack is a sandbox framework for easily designing environments for
Reinforcement Learning. MiniHack is based on the [The NetHack Learning
Environment (NLE)](https://github.com/facebookresearch/nle) and provides a
standard RL interface for customly created tesbeds.

It not only provides a diverse suite of challenging tasks but is primarily built for easily designing new ones.
The motivation behind MiniHack is to be able to perform RL experiments in a controlled setting while being able to increasingly scale the difficulty and complexity of the tasks by removing simplifying assumptions.
To this end, MiniHack leverages the description file (des-file) format of the game of NetHack, thereby enabling the creation of many challenging and diverse environments.

For the full list of existing tasks, see [here](./TASKS.md).

## Des-file format

The des-file format is a domain-specific language created by the developers of NetHack for describing the levels of the game. des-files are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc. 

Levels defined via des-file can be fairly rich, as the underlying programming language has support for variables, loops, conditional statements, as well as probability distributions.
Crucially, it supports underspecified statements, such as generating a random monster or an object at a random location on the map.
Furthermore, it features commands that procedurally generate diverse grid layouts in a single line.

For more information, check out our [interactive tutorial](./notebooks/des_file_tutorial.ipynb) or the [documentation](https://nethackwiki.com/wiki/Des-file_format) on NetHack Wiki..

## NetHack

NetHack is one of the oldest and arguably most impactful videogames in history,
as well as being one of the hardest roguelikes currently being played by humans.
It is procedurally generated, rich in entities and dynamics, and overall an
extremely challenging environment for current state-of-the-art RL agents, while
being much cheaper to run compared to other challenging testbeds.

MiniHack, NLE and NetHack use [NETHACK GENERAL PUBLIC LICENSE](https://github.com/facebookresearch/nle/blob/master/LICENSE).


<!-- # Papers using the MiniHack The Planet
- Samvelyan et al. [MiniHack The Planet](https://arxiv.org/abs/20XX.YYYY) (FAIR, UCL, Oxford)

Open a [pull request](https://github.com/MiniHackPlanet/MiniHack/edit/master/README.md) to add papers -->

# Getting started

Starting with MiniHack environments is extremely simple, provided one is familiar
with other gym / RL environments.

## Installation

We advise using a conda environment for this:

``` bash
conda create -n minihack python=3.8
conda activate minihack
```

Then, install the MiniHack package. 

``` bash
git clone https://github.com/ucl-dark/minihack 
cd minihack
pip install -e ".[dev]"
pre-commit install
```

## Trying it out

After installation, one can try out any of the provided tasks as follows:

```python
>>> import gym
>>> import minihack
>>> env = gym.make("MiniHack-River-v0")
>>> env.reset()  # each reset generates a new dungeon
>>> env.step(1)  # move agent '@' north
>>> env.render()
```

MiniHack also comes with a few scripts that allow to get some environment rollouts,
and play with the action space:

```bash
# Play the MiniHack in the Terminal as a human
$ python -m minihack.scripts.play --env MiniHack-River-v0

# Use a random agent
$ python -m minihack.scripts.play --env MiniHack-River-v0  --mode random

# See all the options
$ python -m minihack.scripts.play --help

# Play the MiniHack with graphical user interface (gui)
$ python -m minihack.scripts.play_gui --env MiniHack-River-v0
```

## Baseline Agents

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
document](./nle/agent/README.md).
We also provide baseline learning curves of the MiniHack paper in Weights&Biases format for all of our experiments. They can be accessed [here](https://wandb.ai/minihack).

# Contributions and Maintenance

We welcome contributions to MiniHack. If you are interested in contributing please see [this document](./CONTRIBUTING.md). MiniHack's maintenance plan can be found [here](./MAINTENANCE.md).

# Citation
 
If you use MiniHack in any of your work, please cite:

```
@misc{samvelyan2021MiniHack,
  author = {Mikayel Samvelyan and
            Robert Kirk and
            Vitaly Kurin and
            Jack Parker-Holder and
            Minqi Jiang and
            Eric Hambro and
            Fabio Petroni and
            Heinrich K\"{u}ttler and
            Edward Grefenstette and
            Tim Rockt{\"{a}}schel},
  title     = {{MiniHack the Planet: A Sandbox for NetHack Learning Environment}},
  howpublished= {https://github.com/MiniHackPlanet/MiniHack},
  year      = {2021},
}
```

If you use MiniHack's interface on environments ported from other benchmarks, please cite the original paper as well:

- [MiniGrid](https://github.com/maximecb/gym-minigrid/) (see [LICENSE](https://github.com/maximecb/gym-minigrid/blob/master/LICENSE))

```
@misc{gym_minigrid,
  author = {Chevalier-Boisvert, Maxime and Willems, Lucas and Pal, Suman},
  title = {Minimalistic Gridworld Environment for OpenAI Gym},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/maximecb/gym-minigrid}},
}
```

- [Boxoban](https://github.com/deepmind/boxoban-levels/) (see [LICENSE](https://github.com/deepmind/boxoban-levels/blob/master/LICENSE))

```
@misc{boxobanlevels,
  author = {Arthur Guez, Mehdi Mirza, Karol Gregor, Rishabh Kabra, Sebastien Racaniere, Theophane Weber, David Raposo, Adam Santoro, Laurent Orseau, Tom Eccles, Greg Wayne, David Silver, Timothy Lillicrap, Victor Valdes},
  title = {An investigation of Model-free planning: boxoban levels},
  howpublished= {https://github.com/deepmind/boxoban-levels/},
  year = "2018",
}
```
