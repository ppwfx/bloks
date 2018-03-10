from bloks import gtx


def get(levels, args):
    if isinstance(args, dict):
        return [args]

    if isinstance(args, str):
        if args == "all":
            return gtx.get(levels).items()
        else:
            return [gtx.get(levels)[args]]

    identifier = gtx.get(["_cli", "_identifier"])
    if identifier == "all":
        return gtx.get(levels).values()

    return [gtx.get(levels)[identifier]]


def remove_leading_underscores(data):
    new_data = {}
    for key, value in data.items():
        if key[0] == "_":
            key = key[1:]

        new_data[key] = value

    return new_data