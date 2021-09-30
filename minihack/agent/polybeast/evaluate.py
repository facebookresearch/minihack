# Copyright (c) Facebook, Inc. and its affiliates.

import minihack.agent.polybeast.models
from minihack.agent import get_env_shortcut
from minihack.agent.polybeast import polyhydra
import argparse
import time
import timeit
import os
import tempfile
import shutil
import glob

import gym
import torch
from omegaconf import OmegaConf


def get_action(model, obs, hidden, done, watch):
    with torch.no_grad():
        for key in obs.keys():
            shape = obs[key].shape
            obs[key] = torch.Tensor(obs[key].reshape((1, 1, *shape)))

        obs["done"] = torch.BoolTensor([done])

        out, hidden = model(obs, hidden)

        action = out["action"]

    if watch:
        input()

    return action, hidden


def load_model(env, checkpoint_path):
    pretrained_path = os.path.join(checkpoint_path, "checkpoint.tar")
    pretrained_config_path = os.path.join(checkpoint_path, "config.yaml")
    flags = OmegaConf.load(pretrained_config_path)
    flags["env"] = env
    flags = polyhydra.get_common_flags(flags)
    flags = polyhydra.get_environment_flags(flags)
    flags = polyhydra.get_learner_flags(flags)
    model = minihack.agent.polybeast.models.create_model(
        flags, torch.device("cpu")
    )

    checkpoint_states = torch.load(
        pretrained_path, map_location=torch.device("cpu")
    )

    model.load_state_dict(checkpoint_states["model_state_dict"])

    hidden = model.initial_state(batch_size=1)
    model.eval()
    return model, hidden


def eval(
    env,
    num_episodes,
    max_steps,
    seeds,
    savedir,
    no_render,
    render_mode,
    checkpoint_dir,
    watch,
    obs_keys,
    save_gif,
    gif_path,
    gif_duration,
):
    agent_env = get_env_shortcut(env)
    env = gym.make(
        env,
        savedir=savedir,
        max_episode_steps=max_steps,
        observation_keys=obs_keys.split(","),
    )
    if seeds is not None:
        env.seed(seeds)
    if not no_render:
        print("Available actions:", env._actions)

    obs = env.reset()
    done = False

    model, hidden = load_model(agent_env, checkpoint_dir)

    steps = 0
    episodes = 0
    reward = 0.0
    action = None

    mean_sps = 0
    mean_reward = 0.0
    mean_return = 0.0

    total_start_time = timeit.default_timer()
    start_time = total_start_time

    if save_gif:
        # Import pillow
        try:
            import PIL.Image
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "To safe GIF files of trajectories, please install Pillow:"
                " pip install Pillow"
            )
        # Create a tmp directory for individual screenshots
        tmpdir = tempfile.mkdtemp()

    while True:
        if watch and not no_render:
            print("Previous reward:", reward)
            if action is not None:
                print("Previous action: %s" % repr(env._actions[action]))
            env.render(render_mode)

        if save_gif:
            obs_image = PIL.Image.fromarray(obs["pixel_crop"])
            obs_image.save(os.path.join(tmpdir, f"e_{episodes}_s_{steps}.png"))

        action, hidden = get_action(model, obs, hidden, done, watch)
        if action is None:
            break

        obs, reward, done, info = env.step(action)
        steps += 1

        mean_reward += (reward - mean_reward) / steps

        if not done:
            continue

        time_delta = timeit.default_timer() - start_time

        print("Final reward:", reward)
        print("End status:", info["end_status"].name)
        print("Mean reward:", mean_reward)
        print("Total reward:", mean_reward * steps)

        mean_return += (mean_reward * steps) / num_episodes
        sps = steps / time_delta
        print("Episode: %i. Steps: %i. SPS: %f" % (episodes, steps, sps))

        episodes += 1
        mean_sps += (sps - mean_sps) / episodes

        start_time = timeit.default_timer()

        steps = 0
        mean_reward = 0.0

        if episodes == num_episodes:
            break
        env.reset()

    if save_gif:
        # Make the GIF and delete the temporary directory
        png_files = glob.glob(os.path.join(tmpdir, "e_*_s_*.png"))
        png_files.sort(key=os.path.getmtime)

        img, *imgs = [PIL.Image.open(f) for f in png_files]
        img.save(
            fp=gif_path,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=gif_duration,
            loop=0,
        )
        shutil.rmtree(tmpdir)

        print("Saving replay GIF at {}".format(os.path.abspath(gif_path)))

    env.close()
    print(
        "Finished after %i episodes and %f seconds. Mean sps: %f"
        % (episodes, timeit.default_timer() - total_start_time, mean_sps)
    )
    print(f"Mean return is {mean_return}")


def main():
    parser = argparse.ArgumentParser(
        description="Tool for evaluating pretrained models."
    )
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="MiniHack-Room-15x15-v0",
        help="Gym environment spec. Defaults to 'MiniHack-Room-15x15-v0'.",
    )
    parser.add_argument(
        "-c",
        "--checkpoint_dir",
        type=str,
        help="Path to checkpoint directory to load the model and configs. "
        + "This directory must include checkpoint.tar and config.yaml files.",
    )
    parser.add_argument(
        "-o",
        "--obs_keys",
        type=str,
        default="glyphs,chars,colors,specials,blstats,message",
        help="The observation keys as a string. Separate keys using a comma",
    )
    parser.add_argument(
        "-n",
        "--num_episodes",
        type=int,
        default=5,
        help="Number of episodes to be evaluated before exiting.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Number of maximum steps per episode.",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Seeds to send to NetHack. Can be a dict or int. "
        "Defaults to None (no seeding).",
    )
    parser.add_argument(
        "--savedir",
        default=None,
        help="Directory path where data will be saved. "
        "Defaults to None (not data saved).",
    )
    parser.add_argument(
        "--no-render", action="store_true", help="Disables env.render()."
    )
    parser.add_argument(
        "--render_mode",
        type=str,
        default="human",
        choices=["human", "full", "ansi"],
        help="Render mode. Defaults to 'human'.",
    )
    parser.add_argument(
        "--watch",
        dest="watch",
        action="store_true",
        help="Pressing the Enter key performs a step.",
    )
    parser.add_argument(
        "--no-watch",
        dest="watch",
        action="store_false",
        help="Not watching the replay.",
    )
    parser.set_defaults(watch=True)
    parser.add_argument(
        "--save_gif",
        dest="save_gif",
        action="store_true",
        help="Saving a GIF replay of the evaluated episodes.",
    )
    parser.add_argument(
        "--no-save_gif",
        dest="save_gif",
        action="store_false",
        help="Do not save GIF.",
    )
    parser.set_defaults(save_gif=False)
    parser.add_argument(
        "--gif_path",
        type=str,
        default="replay.gif",
        help="Where to save the produced GIF file.",
    )
    parser.add_argument(
        "--gif_duration",
        type=int,
        default=300,
        help="The duration of each gif image.",
    )
    flags = parser.parse_args()

    if flags.savedir == "args":
        flags.savedir = "{}_{}_{}.zip".format(
            time.strftime("%Y%m%d-%H%M%S"), flags.mode, flags.env
        )

    if flags.save_gif and "pixel_crop" not in flags.obs_keys:
        flags.obs_keys += ",pixel_crop"

    eval(**vars(flags))


if __name__ == "__main__":
    main()
