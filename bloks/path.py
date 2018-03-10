import bloks.render


def full(relative):
    return bloks.render.string_as_string("{{ gtx._workdir }}/{{ relative}}", {"relative": relative})