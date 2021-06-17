# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, RewardManager
from gym.envs import registration


class MiniHackUnlock(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(["You succeed in unlocking the chest"])
        super().__init__(
            *args, des_file="chest.des", reward_manager=rwrd_mngr, **kwargs
        )


class MiniHackUnlockLoot(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(["You carefully open the chest..."])
        super().__init__(
            *args, des_file="chest.des", reward_manager=rwrd_mngr, **kwargs
        )


class MiniHackUnlockEat(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_eat_event("apple")
        super().__init__(
            *args, des_file="chest.des", reward_manager=rwrd_mngr, **kwargs
        )


registration.register(
    id="MiniHack-Unlock-v0",
    entry_point="minihack.envs.skills_chest:MiniHackUnlock",
)
registration.register(
    id="MiniHack-UnlockLoot-v0",
    entry_point="minihack.envs.skills_chest:MiniHackUnlockLoot",
)
registration.register(
    id="MiniHack-UnlockEat-v0",
    entry_point="minihack.envs.skills_chest:MiniHackUnlockEat",
)
