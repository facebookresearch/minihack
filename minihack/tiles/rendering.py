# Copyright (c) Facebook, Inc. and its affiliates.

from minihack import MiniHackSkill
from nle.nethack.actions import MiscDirection
import PIL.Image
import PIL.ImageChops
import math


def get_image(pixel_obs, full_screen=False, resize=None, relative=False):
    image = PIL.Image.fromarray(pixel_obs)
    if not full_screen:
        bg = PIL.Image.new(image.mode, image.size, image.getpixel((0, 0)))
        diff = PIL.ImageChops.difference(image, bg)
        diff = PIL.ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            image = image.crop(bbox)

    if resize is not None:
        x_resize, y_resize = resize
        if relative:
            image = image.resize(
                (int(image.width * x_resize), int(image.height * y_resize))
            )
        else:
            image = image.resize((x_resize, y_resize))

    return image


def get_des_file_rendering(
    des_file,
    n_images=1,
    full_screen=False,
    full_obs=True,
    resize=None,
    relative=True,
    wizard=False,
):
    class MHCustom(MiniHackSkill):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, des_file=des_file, **kwargs)

    def get_pixel_obs(env, full_obs=True):
        obs = env.reset()
        if full_obs and wizard:
            for c in (
                "#wizintrinsic\rt\r\r#wizmap\r#wizwish\r"
                + "a potion of object detection\r"
            ):
                obs, sds = env.env.step(ord(c))
            msg = (
                obs[env._original_observation_keys.index("message")]
                .tobytes()
                .decode("utf-8")
            )

            for c in f"q{msg[0]}":
                obs, sds = env.env.step(ord(c))

            obs, _, _, _ = env.step(env._actions.index(MiscDirection.WAIT))
        return obs

    env = MHCustom(
        savedir=None,
        archivefile=None,
        observation_keys=("pixel",),
        wizard=wizard,
    )
    if n_images == 1:
        obs = get_pixel_obs(env, full_obs=full_obs)
        image = get_image(
            obs["pixel"],
            full_screen=full_screen,
            resize=resize,
            relative=relative,
        )
        return image
    else:
        images = []
        for _i in range(n_images):
            obs = get_pixel_obs(env, full_obs=full_obs)
            images.append(
                get_image(
                    obs["pixel"],
                    resize=resize,
                    relative=relative,
                    full_screen=full_screen,
                )
            )
        width = images[0].width
        height = images[0].height
        result = PIL.Image.new(
            "RGB",
            ((width * 3) + 10, ((height + 5) * math.ceil(n_images / 3)) - 5),
            color=(200, 200, 200),
        )
        for j in range(math.ceil(n_images / 3)):
            for i in range(3):
                try:
                    result.paste(
                        images[(j * 3) + i],
                        ((width + 5) * i, (height + 5) * j),
                    )
                except IndexError:
                    return result
        return result
