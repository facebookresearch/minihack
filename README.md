<p align="center">
 <img width="70%" src="docs/imgs/minihack.png" />
</p>

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
 <a href="https://pepy.tech/project/minihack">
    <img src="https://static.pepy.tech/personalized-badge/minihack?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads" />
  </a>
 </p>
 
-------------------------------------------------------------------------------------------------------------------------------------------------------

MiniHack is a sandbox framework for easily designing rich and diverse environments for Reinforcement Learning (RL).
Based on the game of [NetHack](https://en.wikipedia.org/wiki/NetHack), MiniHack uses the [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle) to communicate with the game and to provide a convenient interface for customly created RL training and test environments of varying complexity.
Check out our [NeurIPS 2021 paper](https://arxiv.org/abs/2109.13202) and recent [blogpost](https://ai.facebook.com/blog/minihack-a-new-sandbox-for-open-ended-reinforcement-learning).

MiniHack comes with a large list of challenging [environments](https://minihack.readthedocs.io/en/latest/envs/index.html). However, it is primarily built for easily designing new ones.
The motivation behind MiniHack is to be able to perform RL experiments in a controlled setting while being able to increasingly scale the complexity of the tasks.

<p align="center">
 <img width="90%" src="/docs/imgs/minihack_gameplay_collage.gif" />
</p>

To do this, MiniHack leverages the so-called [description files](https://nethackwiki.com/wiki/Des-file_format) written using a human-readable probabilistic-programming-like domain-specific language. With just a few lines of code, people can generate a large variety of [Gym](https://github.com/openai/gym) environments, controlling every little detail, from the location and types of monsters, to the traps, objects, and terrain of the level, all while introducing randomness that challenges generalization capabilities of RL agents. For further details, we refer users to our [brief overview](https://minihack.readthedocs.io/en/latest/getting-started/des_files.html), [detailed tutorial](https://minihack.readthedocs.io/en/latest/tutorials/des_file_tutorial.html), or [interactive notebook](./docs/tutorials/des_file_tutorial.ipynb).

[Our documentation](https://minihack.readthedocs.io/) will walk you through everything you need to know about MiniHack, step-by-step, including information on how to get started, configure environments or design new ones, train baseline agents, and much more.

![MiniHack Environments](/docs/imgs/des_file.gif)

### MiniHack Level Editor

The [MiniHack Level Editor](https://minihack-editor.github.io) allows to easily define MiniHack environments inside a browser using a convenient drag-and-drop functionality. Check it out at [minihack-editor.github.io](https://minihack-editor.github.io).

<p align="center">
 <img width="90%" src="/docs/imgs/level_editor.png" />
</p>

### Language Wrapper

We thank [ngoodger](https://github.com/ngoodger) for implementing the [NLE Language Wrapper](https://github.com/ngoodger/nle-language-wrapper) that translates the non-language observations from Net/MiniHack tasks into similar language representations. Actions can also be optionally provided in text form which are converted to the Discrete actions of the NLE.

# Installation

The simplest way to install MiniHack is through [pypi](https://pypi.org/project/minihack/):
```bash
pip install minihack
```

See the [full installation guide](./docs/getting-started/installation.md) for further information on installing and extending MiniHack on different platforms, as well as pre-installed Dockerfiles.


# Submitting New Environments

For submitting your own MiniHack-based environment to our [zoo of public environments](https://minihack.readthedocs.io/en/latest/envs/index.html), please follow the instructions [here](./docs/envs/contributing.md).

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
pip install -e ".[polybeast]"
python -m minihack.agent.polybeast.polyhydra env=MiniHack-Room-5x5-v0 total_steps=100000
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
pip install -e ".[rllib]"
python -m minihack.agent.rllib.train algo=dqn env=MiniHack-Room-5x5-v0 total_steps=1000000
```

More information on running RLlib agents can be found [here](./docs/agents/rllib.md).

### Unsupervised Environment Design

MiniHack also enables research in *Unsupervised Environment Design*, whereby an adaptive task distribution is learned during training by dynamically adjusting free parameters of the task MDP.
Check out the [`ucl-dark/paired`](https://github.com/ucl-dark/paired) repository for replicating the examples from the paper using the [PAIRED](https://arxiv.org/abs/2012.02096).

# Papers using MiniHack

- Walker et al. [Unsupervised representational learning with recognition-parametrised probabilistic models](https://arxiv.org/abs/2209.05661) (UCL, Sept 2022)
- Mu et al. [Improving Intrinsic Exploration with Language Abstractions](https://arxiv.org/abs/2202.08938) (Stanford, UW, Meta AI, UCL, NeurIPS 2022)
- Matthews et al. [Hierarchical Kickstarting for Skill Transfer in Reinforcement Learning](https://arxiv.org/abs/2110.02439) (UCL, Meta AI, Oxford, CoLLAs 2022)
- Powers et al. [CORA: Benchmarks, Baselines, and a Platform for Continual Reinforcement Learning Agents](https://arxiv.org/abs/2110.10067) (CMU, Georgia Tech, AI2, CoLLAs 2022)
- Nottingham et al. [Learning to Query Internet Text for Informing Reinforcement Learning Agents](https://arxiv.org/abs/2205.13079) (UC Irvine, May 2022)
- Matthews et al. [SkillHack: A Benchmark for Skill Transfer in Open-Ended Reinforcement Learning](https://openreview.net/forum?id=rHSVHmDWI-9) (UCL, Meta AI, Oxford, April 2022)
- Parker-Holder et al. [Evolving Curricula with Regret-Based Environment Design](https://arxiv.org/abs/2203.01302) (Oxford, Meta AI, UCL, Berkeley, ICML 2022)
- Jiang et al. [Grounding Aleatoric Uncertainty in Unsupervised Environment Design](https://openreview.net/forum?id=o8_QHMYOfu) (FAIR, UCL, Berkeley, Oxford, December 2021)
- Parker-Holder et al. [That Escalated Quickly: Compounding Complexity by Editing Levels at the Frontier of Agent Capabilities](https://openreview.net/forum?id=3qGInPFqR0p) (Oxford, FAIR, UCL, Berkeley, December 2021)
- Samvelyan et al. [MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research
](https://arxiv.org/abs/2109.13202) (FAIR, UCL, Oxford, NeurIPS 2021)

Open a [pull request](https://github.com/facebookresearch/minihack/edit/main/README.md) to add papers.

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
