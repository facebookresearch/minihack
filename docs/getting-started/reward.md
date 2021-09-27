# Reward Function

## Default Configuration

Reward functions in MiniHack can easily be configured. The default reward function of custom MiniHack environments is a sparse reward of +1 for reaching the staircase down (which terminates the episode), and 0 otherwise, with episodes terminating after a configurable number of timesteps. In addition, the agent receives a negative reward of -0.01 if the game timer doesn't progress during a step (e.g. the agent moves towards a wall).

These defaults can be easily adjusted using the following environment flags:

| Parameter     | Default Value | Description    |
|---------------|---------------|----------------|
|`reward_win`   |1| the reward received upon successfully completing an episode. |
|`reward_lose`  |0| the reward received upon death or aborting. |
|`penalty_mode` |"constant"| name of the mode for calculating the time step penalty. Can be ``constant``, ``exp``, ``square``, ``linear``, or ``always``. |
|`penalty_step` |-0.01| constant applied to amount of frozen steps. |
|`penalty_time` |0| constant applied to amount of non-frozen steps. |

## Reward Manager

We also provide an interface for designing custom reward functions. By using the [RewardManager](../api/minihack.html#minihack.RewardManager), users can control what events give the agent reward, whether those events can be repeated, and what combinations of events are sufficient or required to terminate the episode.

In order to use the reward managers, users need create an instance of the class and pass it to a MiniHack environment. In the example below, the agent receives +1 reward for eating an apple or +2 reward for wielding a dagger (both of which also terminate the episode). In addition, the agent receives -1 reward for standing on a sink, but the episode isn't termianted in this case.
```python
from minihack import RewardManager
reward_gen = RewardManager()
reward_gen.add_eat_event("apple", reward=1)
reward_gen.add_wield_event("dagger", reward=2)
reward_gen.add_location_event("sink", reward=-1, terminal_required=False)

env = gym.make("MiniHackSkill",
    def_file=des_file.
    reward_manager=reward_manager)
```
While the basic reward manager supports many events by default, users may want to extend this interface to define their own events. This can be done easily by inheriting from the [Event](../api/minihack.reward_manager.html#minihack.reward_manager.Event) class and implementing the `check` and `reset` methods. Beyond that, custom reward functions can be added to the reward manager through `add_custom_reward_fn` method. These functions take the environment instance, the previous observation, action taken and current observation, and should return a float.

We also provide two ways to combine events in a more structured way. The [SequentialRewardManager](../api/minihack.reward_manager.html#minihack.reward_manager.SequentialRewardManager) works similarly to the normal reward manager but requires the events to be completed in the sequence they were added, terminating the episode once the last event is complete. The [GroupedRewardManager](../api/minihack.reward_manager.html#minihack.reward_manager.GroupedRewardManager) combines other reward managers, with termination conditions defined across the reward managers (rather than individual events). This allows complex conjunctions and disjunctions of groups of events to specify termination. For example, one could specify a reward function that terminates if a sequence of events (a,b,c) was completed, or all events \{d,e,f\} were completed in any order and the sequence (g,h) was completed.
