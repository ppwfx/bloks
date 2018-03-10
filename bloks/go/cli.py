from bloks import args
from bloks.go import facade


def build(arg=None):
    apps = args.get(["_golang", "_build"], arg)

    for app in apps:
        facade.build(app)