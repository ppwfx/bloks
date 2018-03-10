import os
import docker
from bloks import render, args
from bloks import logit


@logit.deco()
def build(build):
    src_path = "{}/{}".format(os.getcwd(), build["_path"])
    go_path = os.environ['GOPATH']

    env = {**build["_env"], **{"GOPATH": "/go", }}

    command = render.string_as_string("go build -o {{ _name }} .", build)

    docker.from_env(version="auto").containers.run(image=build["_image"],
                                                   command=command,
                                                   environment=env,
                                                   working_dir="/src",
                                                   volumes={
                                                       src_path: {'bind': '/src', 'mode': 'rw'},
                                                       go_path: {'bind': '/go', 'mode': 'rw'},
                                                   })
