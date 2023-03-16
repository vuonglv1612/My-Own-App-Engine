import os
import shutil
import subprocess
import tarfile
import zipfile

import docker
from git import Repo


def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def extract(file, folder):
    # remove folder if exists
    delete_folder(folder)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(folder)


def clone(url, folder, branch=None):
    # remove folder if exists
    delete_folder(folder)
    repo = Repo.clone_from(url, folder)
    if branch:
        repo.git.checkout(branch)


def compress(folder_path, tar_file_path):
    with tarfile.open(tar_file_path, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))


def build(folder, image_name, image_tag, builder, buildpack=None):
    image = f"{image_name}:{image_tag}"
    args = [
        "pack",
        "build",
        image,
        "--path",
        folder,
        "--builder",
        builder
    ]
    if buildpack:
        args.extend(["--buildpack", buildpack])

    with subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            universal_newlines=True,
    ) as proc:
        for line in proc.stdout:
            yield line
        if proc.returncode != 0:
            yield False
        else:
            yield True


def create_remote_image(image_name, registry, namespace):
    registry_image_name = f"{registry}/{namespace}/{image_name}"
    return registry_image_name


def push(image_name, registry, namespace, username=None, password=None):
    client = docker.from_env()
    if username and password:
        client.login(registry=registry, username=username, password=password)
    registry_image_name = create_remote_image(image_name, registry, namespace)
    client.images.get(f"{image_name}").tag(registry_image_name)
    for line in client.images.push(registry_image_name, stream=True, decode=True):
        yield line
    client.images.remove(registry_image_name)
    client.images.remove(f"{image_name}")
    client.close()
