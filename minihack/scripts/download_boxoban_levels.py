# Copyright (c) Facebook, Inc. and its affiliates.

import os
import zipfile
import pkg_resources

DESTINATION_PATH = pkg_resources.resource_filename("minihack", "dat")
BOXOBAN_REPO_URL = (
    "https://github.com/deepmind/boxoban-levels/archive/refs/heads/master.zip"
)


def download_boxoban_levels():
    print("Downloading Boxoban levels...")
    os.system(
        f"wget -c --read-timeout=5 --tries=0 "
        f'"{BOXOBAN_REPO_URL}" -P {DESTINATION_PATH}'
    )
    print("Boxoban levels downloaded, unpacking...")

    zip_file = os.path.join(DESTINATION_PATH, "master.zip")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(DESTINATION_PATH)

    os.remove(zip_file)


if __name__ == "__main__":
    download_boxoban_levels()
