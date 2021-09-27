# Installation

MiniHack is available on [pypi](https://pypi.org/project/minihack/) and can be installed as follows:
```bash
pip install minihack
```

We advise using a conda environment for this:

```bash
conda create -n minihack python=3.8
conda activate minihack
pip install minihack
```

````{note}
NLE requires `cmake>=3.15` to be installed when building the package. Check out [here](https://github.com/facebookresearch/nle#installation) how to install it on __MacOS__ and __Ubuntu 18.04__. __Windows__ users should use [Docker](#docker).
````

## Extending MiniHack

If you wish to extend MiniHack, please install the package as follows:

```bash
git clone https://github.com/facebookresearch/minihack
cd minihack
pip install -e ".[dev]"
pre-commit install
```

## Docker

We have provided some docker images. Please follow the instructions described [here](https://github.com/facebookresearch/minihack/tree/main/docker).
