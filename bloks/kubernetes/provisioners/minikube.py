import subprocess
import bloks.sh


def is_up():
    completed = bloks.sh.run("minikube status --format {{.MinikubeStatus}}")

    up = False
    if completed.stdout.decode("utf-8") == "Running":
        up = True

    return up


def start():
    completed = bloks.sh.runo("minikube start")
