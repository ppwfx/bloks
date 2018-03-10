from bloks import sh, args, render


def get(arg=None):
    requests = args.get(['_http', '_get'], arg)

    get_each(requests)


def get_each(requests):
    for request in requests:
        command = render.string_as_string(
            "curl -v --socks5-hostname {{ _socks5_user }}:{{ _socks5_pass }}@{{ _socks5_host }}:{{ _socks5_port }} {{ _url }}", request)

        sh.runo(command, check=False)
