import os
import shutil
import subprocess
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


def push(image_name, tag, registry, namespace, username=None, password=None):
    client = docker.from_env()
    if username and password:
        client.login(registry=registry, username=username, password=password)
    registry_image_name = f"{registry}/{namespace}/{image_name}:{tag}"
    client.images.get(f"{image_name}:{tag}").tag(registry_image_name)
    for line in client.images.push(registry_image_name, stream=True, decode=True):
        print(line)
    client.close()
