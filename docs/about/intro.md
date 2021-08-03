# Introduction

MiniHack is a sandbox framework for easily designing rich and diverse environments for Reinforcement Learning (RL) research.
Based on the game of [NetHack](./nethack), arguably the hardest grid-based game in the world, MiniHack uses the [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle) to provide a convenient [Gym interface](https://github.com/openai/gym) for for customly created RL tesbeds.

MiniHack already comes with a large list of challenging tasks. However, it is primarily built for easily designing new ones. The motivation behind MiniHack is to be able to perform RL experiments in a controlled setting while being able to increasingly scale the difficulty and complexity of the tasks by removing simplifying assumptions.