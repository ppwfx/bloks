from pprint import pprint
from bloks import render, kubectl, http, sh, gtx, curl
import bloks.kubernetes.cmd
import bloks.go.cli
import bloks.speech.facade
import bloks.docker.cli
import click
import project
import logging


blue = "\033[1;34m%s\033[1;0m"
yellow = "\033[1;33m%s\033[1;0m"
green = "\033[1;32m%s\033[1;0m"
red = "\033[1;31m%s\033[1;0m"

logging.addLevelName(logging.INFO, green % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, yellow % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, red % logging.getLevelName(logging.ERROR))

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('tool', required=False)
@click.argument('action', required=False)
@click.argument('identifier', required=False)
@click.option('-i', '--ignore-errors', is_flag=True, default=False, help='ignore errors')
@click.option('-v', '--verbose', is_flag=True, default=False, help='verbose output')
def tools(tool=None, action=None, identifier=None, ignore_errors=False, verbose=False):
    gtx.init()

    gtx.set(["_ignore-errors"], ignore_errors)

    # if tool is None:
    #     phrases = bloks.speech.facade.listen(["kubecontrol", "apply", "delete", "logs", "exec", "execute", "kube", "run", "go", "build", "docker", "build", "http", "get", "curl", "get", "pro", "pipe", "worker", "datastore", "proxy"])
    #
    #     tool = phrases[0]
    #     action = phrases[1]
    #     identifier = phrases[2]

    gtx.set(["_cli"], {
        "_tool": tool,
        "_action": action,
        "_identifier": identifier,
    })

    toolset = {
        "kubecontrol": {
            "apply": kubectl.apply,
            "delete": kubectl.delete,
            "logs": kubectl.logs,
            "exec": kubectl.execute,
            "execute": kubectl.execute,
        },
        "kube": {
            "run": bloks.kubernetes.cmd.run,
        },
        "go": {
            "build": bloks.go.cli.build,
        },
        "docker": {
            "build": bloks.docker.cli.build,
        },
        "http": {
            "get": http.get
        },
        "curl": {
            "get": curl.get
        },
        "pro": {
            "pipe": project.pipe,
        },
        "test": {
            "test": test,
        }
    }

    toolset[tool][action]()


def test():
    sh.runo("env", {"YO": "yoyoy"})


if __name__ == '__main__':
    gtx.init()

    #bloks.kubernetes.cmd.register()

    #print(gtx.get(["_cmd", "_tree"]))

    tools()
    try:
        tools()
        render.remove_temporary_files()
    except Exception as e:
        # pprint(gtx.get([]))

        raise
