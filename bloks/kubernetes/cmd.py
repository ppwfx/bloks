from bloks import args, gtx
from bloks.kubernetes import facade


def register():
    for key in gtx.get(["_kubernetes", "_run"]).keys():
        gtx.register_cmd("kube", "run", key, run)


def run(arg=None):
    pods = args.get(["_kubernetes", "_run"], arg)
    for pod in pods:
        facade.run(**args.remove_leading_underscores(pod))