# Boxoban

This family of environments is ported to MiniHack from [Boxoban](https://github.com/deepmind/boxoban-levels), a box-pushing puzzle game inspired by Sokoban. The goal is to push four boxes (or boulder's in MiniHack's version) to four goal locations. The procedurally generated levels are divided into three difficulties - Ulfiltered, Medium, and Hard.

An example of Boxoban level ported into MiniHack.

![](./imgs/boxoban.png)

## Source

[Source](https://github.com/facebookresearch/minihack/tree/main/minihack/envs/boxohack.py)

## All Environments

| Name                             | Capability |
| -------------------------------- | ---------- |
| `MiniHack-Boxoban-Unfiltered-v0` | Planning   |
| `MiniHack-Boxoban-Medium-v0`     | Planning   |
| `MiniHack-Boxoban-Hard-v0`       | Planning   |