# NetHack

NetHack is one of the oldest and arguably most impactful videogames in history,
as well as being one of the hardest roguelikes currently being played by humans.
It is procedurally generated, rich in entities and dynamics, and overall an extremely
challenging environment for current state-of-the-art RL agents, while being much
cheaper to run compared to other challenging testbeds.

For more information about NetHack, check out its [original
README](./README.nh), at [nethack.org](https://nethack.org/), and on the
[NetHack wiki](https://nethackwiki.com).

## NetHack Learning Environment

[The NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle)
is a Reinforcement Learning environment presented at NeurIPS 2020. NLE is based on
NetHack 3.6.6 and designed to provide a standard RL interface to the game, and comes
with tasks that function as a first step to evaluate agents on this new environment.

You can read more about NLE in the [NeurIPS 2020 paper](https://arxiv.org/abs/2006.13760).

![Example of an agent running on NLE](https://github.com/facebookresearch/nle/raw/master/dat/nle/example_run.gif)
