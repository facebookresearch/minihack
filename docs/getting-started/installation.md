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

**Note:** Please refer to [NLE installation instructions](https://github.com/facebookresearch/nle#installation) when having NLE-related dependency issues on __MacOS__ and __Ubuntu 18.04__. NLE requires `cmake>=3.15` to be installed when building the package. 

**Note:** __Windows__ users should use [Docker](#docker).

**Note:** Baseline agents have separate installation instructions. See [here](https://github.com/facebookresearch/minihack#baseline-agents) for more details.

### Extending MiniHack

If you wish to extend MiniHack, please install the package as follows:

```bash
git clone https://github.com/facebookresearch/minihack
cd minihack
pip install -e ".[dev]"
pre-commit install
```

### Docker

We have provided several Dockerfiles for building images with pre-installed MiniHack. Please follow the instructions described [here](./docker/README.md).
