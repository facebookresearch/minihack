# Using The Baselines

In this README we describe how to use the baselines implemented here to
reproduce the results of the MiniHack paper. This assumes you have installed `minihack`.

## Installing agent requirements

We provide integrations with two frameworks.

* a [TorchBeast](https://github.com/facebookresearch/torchbeast) agent is
  bundled in `minihack.agent.polybeast` together with a simple model to provide
  a starting point for experiments. To install and train this agent, first
  install torchbeast be following the instructions
  [here](https://github.com/facebookresearch/torchbeast#installing-polybeast),
  then use the following commands:
``` bash
$ pip install -e ".[polybeast_agent]"
$ python3 -m minihack.agent.polybeast.polyhydra env=small_room_random learning_rate=0.0001 use_lstm=true total_steps=1000000
```

* An [RLlib](https://github.com/ray-project/ray#rllib-quick-start) agent is
  provided in `minihack.agent.rllib`, with a similar model to the TorchBeast agent.
  This can be used to try out a variety of different RL algorithms - several
  examples are provided. To install and train this agent use the following
  commands:
```bash
$ pip install -e ".[rllib_agent]"
$ python3 -m minihack.agent.rllib.train algo=dqn total_steps=1000000
```

# TorchBeast

## Running experiments

```bash
# Single IMPALA run
$ python3 -m minihack.agent.polybeast.polyhydra model=baseline env=small_room total_steps=1000000
 
# Single RND run
$ python3 -m minihack.agent.polybeast.polyhydra model=rnd env=small_room total_steps=1000000

# To sweep on the cluster: add another --multirun command and comma-separate values
python3 -m minihack.agent.polybeast.polyhydra -m model=baseline,rnd env=big_room_random,big_room_monster total_steps=10000000
```

All environment and training parameters can be specified using command line arguments (or edited directly in config.yaml). See config.yaml file in the polybeast directory for more information. Be sure to set up appropriate paramters for logging with wandb framework (disabled by default).

## Replicating Results of the Paper

To replicate results of the paper performed using TorchBeast, simply run a sweep 5 runs with IMPALA and RND agents on corresponding environments. The `total_steps` parameter must be set appropriately.

```bash
python3 -m minihack.agent.polybeast.polyhydra -m model=baseline,rnd name=1,2,3,4,5 env=big_room_random,big_room_monster total_steps=10000000
```

For navigation tasks, the default parameters are already set. For skill acquisition tasks, additionally add `learning_rate=0.00005 msg.model=lt_cnn`.

The full list of environment name shortcuts can be looked up [here](./env_names.yaml).

## Ported environments

To use environments ported from [MiniGrid](https://github.com/maximecb/gym-minigrid), additionally install the original package:
```bash
pip3 install gym-minigrid
```

To download publically available [Boxoban levels](https://github.com/deepmind/boxoban-levels), run the `download_boxoban_levels.py` script in the `minihack/scripts/` directory.

# RLlib

## Running experiments

```bash
# Single DQN run
$ python3 -m minihack.agent.rllib.train algo=dqn env=small_room total_steps=1000000 dqn.buffer_size=500000
 
# Single PPO run
$ python3 -m minihack.agent.rllib.train  algo=ppo env=small_room total_steps=1000000 ppo.entropy_coeff=0.0001

# Single A2C run
$ python3 -m minihack.agent.rllib.train algo=ppo env=small_room total_steps=1000000 a2c.entropy_coeff=0.0001
```

All environment and training parameters can be specified using command line arguments (or edited directly in config.yaml). See config.yaml file in the rllib directory for more information. Be sure to set up appropriate paramters for logging with wandb framework (disabled by default).


## Replicating Results of the Paper

The following commands replicate the results of RLlib experiments in the paper:

```bash
$ python3 -m minihack.agent.rllib.train --multirun algo=dqn env=big_room lr=0.000001 seed=0,1,2,3,4 total_steps=10000000
$ python3 -m minihack.agent.rllib.train --multirun algo=ppo env=big_room lr=0.00001 seed=0,1,2,3,4 total_steps=10000000
$ python3 -m minihack.agent.rllib.train --multirun algo=a2c env=big_room lr=0.00001 seed=0,1,2,3,4 total_steps=10000000
```

# PAIRED Results

In order to replicate the results of our Unsupervised Experiment design experiments using the PAIRED algorithm, see [here](https://github.com/anonymouscollective/minihack-ued).

