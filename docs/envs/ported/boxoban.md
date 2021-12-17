# Boxoban

This family of environments is ported to MiniHack from [Boxoban](https://github.com/deepmind/boxoban-levels), a box-pushing puzzle game inspired by Sokoban. The goal is to push four boxes (or boulder's in MiniHack's version) to four goal locations (fountains).

The procedurally generated levels are divided into three difficulties - Ulfiltered (`MiniHack-Boxoban-Unfiltered-v0`), Medium (`MiniHack-Boxoban-Medium-v0`), and Hard (`MiniHack-Boxoban-Hard-v0`).

An example of Boxoban level ported into MiniHack.

![](./imgs/boxoban.png)

## Reward

The agent receives a reward of +1 for pushing all boulders to different goal positions. The agent additional receives a shaped reward of +0.1 for each pushing each boulder to a goal position and -0.1 penalty for moving it out of there.

## Source

[Source](https://github.com/facebookresearch/minihack/tree/main/minihack/envs/boxohack.py)

## All Environments

| Name                             | Capability |
| -------------------------------- | ---------- |
| `MiniHack-Boxoban-Unfiltered-v0` | Planning   |
| `MiniHack-Boxoban-Medium-v0`     | Planning   |
| `MiniHack-Boxoban-Hard-v0`       | Planning   |