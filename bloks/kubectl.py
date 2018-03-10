import bloks.render
import bloks.path
import bloks.sh
import bloks.kubernetes.provisioner
import yaml

from bloks import args, kubernetes, gtx


def apply(arg=None):
    templates = args.get(["_kubernetes", "_templates"], arg)

    bloks.kubernetes.provisioner.up()

    apply_each(templates)


def apply_each(templates):
    for template in templates:
        template = render_template(template)

        command = bloks.render.string_as_string(
            get_base_command() + " apply --namespace {{ _namespace }} --filename {{ _resource_path }}", template)

        bloks.sh.runo(command)


def delete(arg=None):
    templates = args.get(["_kubernetes", "_templates"], arg)

    bloks.kubernetes.provisioner.up()

    delete_each(templates)


def delete_each(templates):
    for template in templates:
        template = render_template(template)

        command = bloks.render.string_as_string(
            get_base_command() + " delete --namespace {{ _namespace }} --filename {{ _resource_path }}", template)

        bloks.sh.runo(command)


def logs(arg=None):
    templates = args.get(["_kubernetes", "_templates"], arg)

    bloks.kubernetes.provisioner.up()

    logs_each(templates)


def logs_each(templates):
    for template in templates:
        template = render_template(template)

        pod_names = kubernetes.facade.search_pods(namespace=template["_namespace"], name=template["_name"])
        template["_pod_name"] = pod_names[0]

        command = bloks.render.string_as_string(
            get_base_command() + " logs --namespace {{ _namespace }} {{ _pod_name }}", template)

        bloks.sh.runo(command)


def execute(arg=None):
    templates = args.get(["_kubernetes", "_templates"], arg)

    bloks.kubernetes.provisioner.up()

    execute_each(templates)


def execute_each(templates):
    for template in templates:
        template = render_template(template)

        pod_names = kubernetes.facade.search_pods(namespace=template["_namespace"], name=template["_name"])
        template["_pod_name"] = pod_names[0]

        command = bloks.render.string_as_string(
            get_base_command() + " exec -it --namespace {{ _namespace }} {{ _pod_name }} sh", template)

        bloks.sh.runo(command)


def get_base_command():
    config = gtx.get(['_kubernetes', '_config'])

    base_command = bloks.render.string_as_string(
        "kubectl --kubeconfig {{ _path }} --context {{ _context }}", config)

    return base_command


def render_template(template):
    full_template_path = bloks.render.string_as_string("{{ gtx._workdir }}/{{ _template }}", template)
    template["_resource_path"] = bloks.render.file_as_file(full_template_path, template)

    return template


def render(template_path, ctx):
    template_path = bloks.path.full(template_path)

    print(template_path)

    rendered = bloks.render.file_as_string(template_path, ctx)

    s = split_resources(rendered)

    a = to_dicts(s)

    return a


def to_dicts(resources_yaml):
    resources = {}

    for resource_yaml in resources_yaml:
        resource = yaml.load(resource_yaml)

        if resource["kind"] not in resources:
            resources[resource["kind"]] = {}

        resources[resource["kind"]][resource["metadata"]["name"]] = resource

    return resources


def split_resources(resources):
    return resources.split("---")
