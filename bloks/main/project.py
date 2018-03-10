from bloks import go, gtx, docker, kubectl


def pipe():
    identifier = gtx.get(["_cli"])["_identifier"]

    ctx = gtx.get(["_golang", "_build", identifier])
    go.build_in_container(ctx)

    ctx = gtx.get(["_docker", "_image", identifier])
    docker.build(ctx)

    kubectl.delete(identifier)

    kubectl.apply(identifier)

    kubectl.logs(identifier)
