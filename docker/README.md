# Building Docker images

Here we include Dockerfiles for building images on Ubuntu 16.04 (Xenial), Ubuntu 18.04 (Bionic), and Ubuntu 20.04 (Focal).

To build any of the Dockerfiles (e.g. `Dockerfile-bionic`) locally, run:

```bash
git clone https://github.com/facebookresearch/minihack
cd minihack
docker build -f docker/Dockerfile-bionic . -t minihack:latest
```

The git repository is installed inside a conda distribution, and can be found in /opt/minihack inside the images.
