# Copyright (c) Facebook, Inc. and its affiliates.

import gym
from gym.envs import registration


def register(id, **kwargs):
    if gym.__version__ >= "0.21":
        # Starting with version 0.21, gym wraps everything by the
        # OrderEnforcing wrapper by default (which isn't in gym.wrappers).
        # This breaks our seed() calls and some other code. Disable.
        kwargs["order_enforce"] = False

    registration.register(id, **kwargs)
