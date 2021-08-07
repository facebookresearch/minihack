#!/usr/bin/env python3
# This file is adapted from
# github.com/maximecb/gym-minigrid/blob/master/manual_control.py

import argparse
import numpy as np
import gym
from nle import nethack
import minihack  # noqa
from minihack.tiles.window import Window


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env",
        help="gym environment to load",
        default="MiniHack-CorridorBattle-v0",
    )

    args = parser.parse_args()

    observation_keys = ("pixel", "message")
    env = gym.make(args.env, observation_keys=observation_keys)

    def reset():
        obs = env.reset()
        redraw(obs)

    def step(action):
        obs, reward, done, info = env.step(action)

        if done:
            print("Episode Completed!")
            reset()
        else:
            redraw(obs)

    def key_handler(event):
        if event.key == "escape":
            window.close()
            return

        if event.key == "backspace":
            reset()
            return

        if event.key.startswith("ctrl+"):
            ch = nethack.C(event.key[5])
        else:
            ch = ord(event.key)

        try:
            action = env._actions.index(ch)
            step(action)
        except (ValueError, TypeError):
            print(
                f"Selected action {event.key} is not in action list. "
                "Please try again."
            )

    window = Window("MiniHack the Planet - " + args.env)
    window.reg_key_handler(key_handler)

    def redraw(obs):
        img = obs["pixel"]
        msg = obs["message"]
        msg = msg[: np.where(msg == 0)[0][0]].tobytes().decode("utf-8")
        window.show_obs(img, msg)

    reset()

    # Blocking event loop
    window.show(block=True)


if __name__ == "__main__":
    main()
