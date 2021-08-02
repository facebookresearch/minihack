# Interface

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

The `gym.make` command can also be used to override specific environment parameters:
```python
env = gym.make(
   "MiniHack-River-v0",
   reward_win=1,
   observation_keys=("pixel", "glyphs", "colors", "chars"),
   max_episode_steps=100,
)
```

_TODO_: link to all __init__ configurations of the environment (both MiniHack and NLE)???


## Playing as a human

MiniHack also comes with a few scripts that allow to get some environment rollouts, and play with the action space:

```bash
# Play the MiniHack in the Terminal as a human
$ python -m minihack.scripts.play --env MiniHack-River-v0

# Use a random agent
$ python -m minihack.scripts.play --env MiniHack-River-v0  --mode random

# Play the MiniHack with graphical user interface (gui)
$ python -m minihack.scripts.play_gui --env MiniHack-River-v0
```