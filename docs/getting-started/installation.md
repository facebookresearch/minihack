# Installation

MiniHack is available on [pypi](https://pypi.org/project/gym-minigrid/) and can be installed as follows:
```bash
pip install minihack
```

We advise using a conda environment for this:

```bash
conda create -n minihack python=3.8
conda activate minihack
pip install minihack
```

**NOTE:** If you wish to extend MiniHack, please install the package as follows:

```bash
git clone https://github.com/ucl-dark/minihack
cd minihack
pip install -e ".[dev]"
pre-commit install
```

**NOTE:** Baseline agents have separate installation instructions. See [here](#baseline-agents) for more details.

**NOTE:** NLE requires `cmake>=3.15` to be installed when building the package. Checkout out [here](https://github.com/facebookresearch/nle#installation) how to install it in __MacOS__ and __Ubuntu 18.04__.
**NOTE: **Windows users need to user [Docker](#docker)**.
