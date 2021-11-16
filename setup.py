#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
#
#  MINIHACK_RELEASE_BUILD
#    If set, builds wheel (s)dist such as to prepare it for upload to PyPI.
#

import os
import setuptools
import subprocess


packages = [
    "minihack",
    "minihack.envs",
    "minihack.scripts",
    "minihack.tiles",
    "minihack.tests",
    "minihack.agent",
    "minihack.agent.polybeast",
    "minihack.agent.polybeast.models",
    "minihack.agent.polybeast.core",
    "minihack.agent.rllib",
    "minihack.agent.common",
    "minihack.agent.common.envs",
    "minihack.agent.common.models",
    "minihack.agent.common.util",
]

entry_points = {
    "console_scripts": [
        "mh-play = minihack.scripts.play:main",
        "mh-guiplay = minihack.scripts.play_gui:main",
        "mh-envs = minihack.scripts.env_list:main",
    ]
}

install_requires = ["numpy>=1.16", "gym"]
if not os.getenv("READTHEDOCS"):
    install_requires.append("nle>=0.7.3")

extras_deps = {
    "dev": [
        "pre-commit>=2.0.1",
        "black>=19.10b0",
        "flake8>=3.7",
        "flake8-bugbear>=20.1",
        "pytest>=5.3",
        "pytest-benchmark>=3.1.0",
        "sphinx==4.0.2",
        "sphinx-rtd-theme==1.0.0",
        "myst-parser==0.15.1",
        "nbsphinx==0.8.6",
    ],
    "polybeast": [
        "torch>=1.3.1",
        "hydra-core>=1.0.0",
        "hydra-colorlog>=1.0.0",
        "hydra-submitit-launcher>=1.1.1",
        "wandb>=0.10.31",
        "pyyaml",
    ],
    "rllib": [
        "torch>=1.3.1",
        "ray[rllib]==1.3.0",
        "ray[default]==1.3.0",
        "hydra-core>=1.0.0",
        "hydra-colorlog>=1.0.0",
        "hydra-submitit-launcher>=1.1.1",
        "wandb>=0.10.31",
    ],
    "wiki": [
        "inflect",
        "stanza",
    ],
}

extras_deps["all"] = [item for group in extras_deps.values() for item in group]


if __name__ == "__main__":
    with open("README.md") as f:
        long_description = f.read()
    cwd = os.path.dirname(os.path.abspath(__file__))
    sha = "Unknown"
    version = open("version.txt", "r").read().strip()

    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=cwd)
            .decode("ascii")
            .strip()
        )
    except subprocess.CalledProcessError:
        pass

    if sha != "Unknown" and not os.getenv("MINIHACK_RELEASE_BUILD"):
        version += "+" + sha[:7]
    print("Building wheel {}-{}".format("minihack", version))

    version_path = os.path.join(cwd, "minihack", "version.py")
    with open(version_path, "w") as f:
        f.write("__version__ = '{}'\n".format(version))
        f.write("git_version = {}\n".format(repr(sha)))

    setuptools.setup(
        name="minihack",
        version=version,
        description="MiniHack The Planet: "
        + "A Sandbox for Open-Ended Reinforcement Learning Research",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="The MiniHack Team",
        url="https://github.com/facebookresearch/minihack",
        license="Apache License, Version 2.0",
        entry_points=entry_points,
        packages=packages,
        install_requires=install_requires,
        extras_require=extras_deps,
        python_requires=">=3.7",
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Development Status :: 4 - Beta",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Games/Entertainment",
        ],
        zip_safe=False,
        include_package_data=True,
    )
