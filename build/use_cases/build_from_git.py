from functions import build, clone


def build_from_git(url, branch, folder, image_name, image_tag, builder, buildpack=None):
    clone(url, folder, branch)
    logs = build(folder, image_name, image_tag, builder, buildpack=buildpack)
    for log in logs:
        yield log
