# Introduction

MiniHack is a sandbox framework for easily designing environments for Reinforcement Learning.
MiniHack is based on the [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle)
and provides a standard [Gym](https://gym.openai.com/docs/) interface for customly created tesbeds.

MiniHack not only provides a diverse suite of challenging tasks but is primarily built for easily
designing new ones.The motivation behind MiniHack is to be able to perform RL experiments in a
controlled setting while being able to increasingly scale the difficulty and complexity of the
tasks by removing simplifying assumptions.To this end, MiniHack leverages the description file
(des-file) format of the game of NetHack, thereby enabling the creation of many challenging and
diverse environments.
