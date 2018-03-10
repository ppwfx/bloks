import os
import jinja2
from bloks import gtx


temporary_files = []


def file_as_file(path, ctx):
    output = file_as_string(path, ctx)

    output_path = path + ".tmp"
    with open(output_path, "w") as file:
        file.write(output)

    add_temporary_file(output_path)

    return output_path


def file_as_string(path, ctx):
    path, filename = os.path.split(path)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './'),
        undefined=jinja2.StrictUndefined,
    )

    ctx["gtx"] = gtx.get([])
    return env.get_template(filename).render(ctx)


def add_temporary_file(path):
    global temporary_files
    temporary_files.append(path)


def remove_temporary_files():
    for f in list(set(temporary_files)):
        os.remove(f)


def full_path_file(path, file):
    return "{}/{}/{}".format(os.getcwd(), path, file)


def string_as_string(text, ctx):
    env = jinja2.Environment(
        loader=jinja2.BaseLoader,
        undefined=jinja2.StrictUndefined,
    )

    ctx["gtx"] = gtx.get([])
    return env.from_string(text).render(ctx)
