from pprint import pprint

import yaml
import os


__gtx = {}


def load_yaml(path=""):
    if path == "":
        path = "./make/env/development.yaml"

    with open(path, 'r') as stream:
        return yaml.load(stream)


def init():
    global __gtx
    __gtx = load_yaml()
    __gtx["_workdir"] = os.getcwd()


def get(keys, default=None):
    ctx = __gtx
    for key in keys:
        if default != None:
            if key not in ctx:
                return default

        ctx = ctx[key]

    return ctx


def set(keys, data, safe=True):
    ctx = __gtx
    for i, key in enumerate(keys):
        if not is_last_index(i, keys):
            if not safe:
                if key not in ctx:
                    ctx[key] = {}

            ctx = ctx[key]
        print(key)
        ctx[key] = data


def register_cmd(tool, action, identifier, cmd):
    set(["_cmd", "_tree", tool, action, identifier], cmd, safe=False)

    phrases = get(["_cmd", "_phrases"], [])
    phrases.extend([tool, action, identifier])
    set(["_cmd", "_phrases"], phrases)


def is_last_index(i, list):
    return i == len(list) - 1
