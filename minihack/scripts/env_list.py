# Copyright (c) Facebook, Inc. and its affiliates.

import minihack  # noqa
from gym import envs

skip_envs_list = ["MiniHack-Navigation-Custom-v0", "MiniHack-Skill-Custom-v0"]


def main():
    all_envs = envs.registry.all()
    env_ids = [
        env_spec.id
        for env_spec in all_envs
        if env_spec.id.startswith("MiniHack")
        and env_spec.id not in skip_envs_list
    ]
    print("\n".join(env_ids))


if __name__ == "__main__":
    main()
