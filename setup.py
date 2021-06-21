#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
#
import os
import pathlib
import subprocess
import sys

import setuptools
from setuptools.command import build_ext
from distutils import spawn
from distutils import sysconfig


packages = [
    "minihack",
    "minihack.envs",
    "minihack.agent",
    "minihack.scripts",
    "minihack.tiles",
]

entry_points = {
    "console_scripts": [
        "mh-play = minihack.scripts.play:main",
        "mh-guiplay = minihack.scripts.play_gui:main",
    ]
}


extras_deps = {
    "dev": [
        "pre-commit>=2.0.1",
        "black>=19.10b0",
        "flake8>=3.7",
        "flake8-bugbear>=20.1",
        "sphinx>=2.4.4",
        "sphinx-rtd-theme==0.4.3",
    ],
    "polybeast": [
        "torch>=1.3.1",
        "hydra-core>=1.0.0",
        "hydra-colorlog>=1.0.0",
        "hydra-submitit-launcher>=1.1.1",
        "wandb>=0.10.31",
    ],
    "rllib": [
        "torch>=1.3.1",
        "ray[rllib]>=1.3.0",
        "hydra-core>=1.0.0",
        "hydra-colorlog>=1.0.0",
        "hydra-submitit-launcher>=1.1.1",
        "wandb>=0.10.31",
    ],
}

extras_deps["all"] = [item for group in extras_deps.values() for item in group]


if __name__ == "__main__":
    with open("README.md") as f:
        long_description = f.read()

    setuptools.setup(
        name="minihack",
        version="0.1.0b",
        description=(
            "MiniHack The Planet: ",
            "A Sandbox for Open-Ended Reinforcement Learning Research",
        ),
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="The MiniHack Dev Team",
        url="https://github.com/MiniHackPlanet/minihack",
        license="NetHack General Public License",
        entry_points=entry_points,
        packages=packages,
        install_requires=["nle==0.7.1", "numpy>=1.16", "gym>=0.15"],
        extras_require=extras_deps,
        python_requires=">=3.7",
        classifiers=[
            "License :: OSI Approved :: Nethack General Public License",
            "Development Status :: 4 - Beta",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: C",
            "Programming Language :: C++",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Games/Entertainment",
        ],
        zip_safe=False,
        include_package_data=True,
    )
