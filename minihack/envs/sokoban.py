# Copyright (c) Facebook, Inc. and its affiliates.
import numpy as np

from minihack.envs import register
from minihack import MiniHackNavigation
from nle import nethack

MOVE_ACTIONS = tuple(nethack.CompassDirection)
NAVIGATE_ACTIONS = MOVE_ACTIONS + (
    nethack.Command.OPEN,
    nethack.Command.KICK,
    nethack.Command.SEARCH,
)


class Sokoban(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 2000)
        kwargs["actions"] = kwargs.pop("actions", NAVIGATE_ACTIONS)

        self._time_penalty = kwargs.pop("penalty_time", 0)
        self._reward_shaping_coefficient = kwargs.pop(
            "reward_shaping_coefficient", 0
        )

        super().__init__(*args, **kwargs)

    def step(self, action: int):
        self._current_pits = self._object_positions(self.last_observation, "^")
        return super().step(action)

    def _is_episode_end(self, observation):
        result = super()._is_episode_end(observation)

        if result == self.StepStatus.TASK_SUCCESSFUL:
            # all pits should be filled
            if len(self._object_positions(self.last_observation, "^")) != 0:
                return self.StepStatus.RUNNING

        # stepping into a pit should result in death
        agent_pos = list(self._object_positions(observation, "@"))[0]
        if any([agent_pos == pos for pos in self._current_pits]):
            return self.StepStatus.DEATH

        return result

    def _reward_fn(self, last_observation, action, observation, end_status):
        if end_status == self.StepStatus.TASK_SUCCESSFUL:
            return 1
        elif end_status != self.StepStatus.RUNNING:
            return 0
        # add additional reward if pit is filled (number of pits is decreased)
        return (
            self._time_penalty
            + (
                len(self._object_positions(last_observation, "^"))
                - len(self._object_positions(observation, "^"))
            )
            * self._reward_shaping_coefficient
        )

    def _object_positions(self, observation, object_char):
        char_obs = observation[self._original_observation_keys.index("chars")]
        return set(
            (x, y) for x, y in zip(*np.where(char_obs == ord(object_char)))
        )


class MiniHackSokoban1a(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko1a.des", **kwargs)


class MiniHackSokoban1b(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko1b.des", **kwargs)


class MiniHackSokoban2a(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko2a.des", **kwargs)


class MiniHackSokoban2b(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko2b.des", **kwargs)


class MiniHackSokoban3a(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko3a.des", **kwargs)


class MiniHackSokoban3b(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko3b.des", **kwargs)


class MiniHackSokoban4a(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko4a.des", **kwargs)


class MiniHackSokoban4b(Sokoban):
    def __init__(self, *args, **kwargs):
        kwargs["reward_shaping_coefficient"] = 0.1
        kwargs["penalty_time"] = -0.001
        super().__init__(*args, des_file="soko4b.des", **kwargs)


register(
    id="MiniHack-Sokoban4a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban4a",
)
register(
    id="MiniHack-Sokoban4b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban4b",
)
register(
    id="MiniHack-Sokoban3a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban3a",
)
register(
    id="MiniHack-Sokoban3b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban3b",
)
register(
    id="MiniHack-Sokoban2a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban2a",
)
register(
    id="MiniHack-Sokoban2b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban2b",
)
register(
    id="MiniHack-Sokoban1a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban1a",
)
register(
    id="MiniHack-Sokoban1b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban1b",
)
