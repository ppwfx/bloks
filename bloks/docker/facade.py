import docker
from bloks import render, args, logit


def get_build_context_path(ctx):
    return render.string_as_string("{{ gtx._workdir }}/{{ _build_ctx }}", ctx)


def get_dockerfile_path(ctx):
    return render.string_as_string("{{ gtx._workdir }}/{{ _build_ctx }}/{{ _dockerfile }}", ctx)


@logit.deco()
def build(image):
    build_ctx_path = get_build_context_path(image)
    dockerfile_path = get_dockerfile_path(image)
    dockerfile = render.file_as_file(dockerfile_path, image)

    return docker.from_env(version="auto").images.build(path=build_ctx_path,
                                                        dockerfile=dockerfile,
                                                        tag="{}:latest".format(image["_tag"]))

