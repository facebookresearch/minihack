# Copyright (c) Facebook, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
import os

env_name_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "env_names.yaml"
)
with open(env_name_path, "r") as stream:
    env_short_to_full = yaml.safe_load(stream)

env_full_to_short = {v: k for k, v in env_short_to_full.items()}


def is_env_registered(env):
    return env in env_full_to_short.keys() or env in env_short_to_full.keys()


def get_env_shortcut(env_gym_name):
    try:
        return env_full_to_short[env_gym_name]
    except KeyError:
        raise KeyError(
            "Could not find an environement with a registered "
            f"name: {env_gym_name}. For the full list, see {env_name_path}."
        )


def get_env_gym_name(env_shortcut):
    try:
        return env_short_to_full[env_shortcut]
    except KeyError:
        raise KeyError(
            "Could not find an environement with a shortcut name:"
            f"{env_shortcut}. For the full list, see {env_name_path}."
        )
