# Sokoban

This family of environments is ported to MiniHack from [NetHack](https://github.com/facebookresearch/nle), levels taken directly from Sokoban minigame inside NetHack, excluding monsters and items. The goal is to push boulder's to goal locations (pits or wholes).

Original dat file can be seen [here](https://github.com/facebookresearch/nle/blob/main/dat/sokoban.des).
and corresponding solution from [NetHack Wiki](https://nethackwiki.com/wiki/Sokoban).

An example of Sokoban level ported into MiniHack.

![](../imgs/sokoban3b.png)

## Reward

The agent receives a reward of +1 for reaching the stairs down and +0.1 for filling each pit.

## All Environments

| Name                    | Capability |
| ----------------------- | ---------- |
| `MiniHack-Sokoban1a-v0` | Planning   |
| `MiniHack-Sokoban1b-v0` | Planning   |
| `MiniHack-Sokoban2a-v0` | Planning   |
| `MiniHack-Sokoban2b-v0` | Planning   |
| `MiniHack-Sokoban3a-v0` | Planning   |
| `MiniHack-Sokoban3b-v0` | Planning   |
| `MiniHack-Sokoban4a-v0` | Planning   |
| `MiniHack-Sokoban4b-v0` | Planning   |
