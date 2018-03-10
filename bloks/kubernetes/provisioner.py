import bloks.kubernetes.provisioners.minikube
from bloks import gtx


provisioners = {
    "minikube": bloks.kubernetes.provisioners.minikube,
}


def up():
    name = gtx.get([])["_kubernetes"]["_provisioner"]["_name"]

    provisioner = provisioners[name]

    if not provisioner.is_up():
        provisioner.start()


