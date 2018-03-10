from bloks import args
from bloks.docker import facade


def build(arg=None):
    images = args.get(["_docker", "_image"], arg)

    for image in images:
        facade.build(image)