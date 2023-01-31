from functions import extract, build, delete_folder


def build_from_zip(file, folder, image_name, image_tag, builder, buildpack=None):
    extract(file, folder)
    logs = build(folder, image_name, image_tag, builder, buildpack=buildpack)
    for log in logs:
        yield log

    # delete folder after build
    delete_folder(folder)
