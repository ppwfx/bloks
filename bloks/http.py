from bloks import args, render
import requests
import logging as log


def get(arg=None):
    reqs = args.get(['_http', '_get'], arg)

    get_each(reqs)


def get_each(reqs):
    for req in reqs:
        proxies = get_proxies(req)

        log.info(__name__ + ".get_each " + str(proxies))

        response = requests.get(req["_url"], proxies=proxies, timeout=req["_timeout"])

        print(response.text)


def get_proxies(req):
    log.info(__name__ + ".get_proxies " + str(locals()))

    proxies = None
    if req["_socks5_host"] and req["_socks5_port"]:
        template = "socks5://{{ _socks5_host }}:{{ _socks5_port }}"

        if req["_socks5_user"] and req["_socks5_pass"]:
            template = "socks5://{{ _socks5_user }}:{{ _socks5_pass }}@{{ _socks5_host }}:{{ _socks5_port }}"

        proxy_url = render.string_as_string(template, req)
        proxies = {
            'https': proxy_url,
            'http': proxy_url,
        }

    return proxies