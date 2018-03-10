# https://github.com/kubernetes-incubator/client-python

import logging as log
import time
from kubernetes import client, config, watch
from bloks.kubernetes import utils
from bloks import logit


config.load_kube_config()
v1 = client.CoreV1Api()



@logit.deco()
def search_pods(namespace, name):
    pods = v1.list_namespaced_pod(namespace, watch=False)

    names = []
    for pod in pods.items:
        if name in pod.metadata.name:
            names.append(pod.metadata.name)

    return names





@logit.deco()
def run(namespace, name, image, command, env):
    body = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': name
        },
        'spec': {
            'containers': [{
                'image': image,
                'name': name,
                "command": command.split(" "),
                "imagePullPolicy": "IfNotPresent",

                "env": utils.convert_env(env)
            }],
            "restartPolicy": "Never",
        }
    }

    if name in search_pods(namespace, name):
        delete_namespaced_pod(namespace, name, body={})

        wait_for_pod_deleted(namespace, name, timeout=5)

    create_namespaced_pod(namespace, body)

    wait_for_pod_phase(namespace, name, phases=["Succeeded", "Failed", "Unknown"], timeout=5)


@logit.deco(log_return=False)
def delete_namespaced_pod(namespace, name, body):
    return v1.delete_namespaced_pod(**locals())


@logit.deco()
def create_namespaced_pod(namespace, body):
    v1.create_namespaced_pod(namespace=namespace, body=body)

    name = body["metadata"]["name"]
    # count = 10
    # w = watch.Watch()
    #
    # v1.read_namespaced_pod_log()
    # for event in w.stream(v1.list_namespace, timeout_seconds=10):
    #     print("Event: %s %s" % (event['type'], event['object'].metadata.name))
    #     count -= 1
    #     if not count:
    #         w.stop()

    wait_for_pod_phase(namespace, name, ["Running"], 5)


       # w = watch.Watch()
    # for event in w.stream(v1.read_namespaced_pod_log, namespace=namespace, name=name):
    #     print("Event: %s %s" % (event['type'], event['object'].metadata.name))

    log_namespaced_pod_log(namespace, name)

    return

@logit.deco()
def log_namespaced_pod_log(namespace, name):
    ret = v1.read_namespaced_pod_log(namespace=namespace, name=name)

    logit.log(ret)

@logit.deco()
def read_namespaced_pod(namespace, name):
    return v1.read_namespaced_pod(**locals())


# Pending
# Running
# Succeeded
# Failed
# Unknown
# https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#pod-phase
@logit.deco()
def wait_for_pod_phase(namespace, name, phases, timeout=0):
    phases = [p.lower() for p in phases]

    start_time = time.time()

    while True:
        resp = v1.read_namespaced_pod(name=name, namespace=namespace)

        phase = resp.status.phase.lower()
        if phase in phases:
            return phase

        time.sleep(0.1)

        if timeout != 0:
            if time.time() - start_time > timeout:
                log.error(__name__ + ".wait_for_pod_phase " + str(resp.status))

                raise Exception("Timed out")


@logit.deco()
def wait_for_pod_deleted(namespace, name, timeout=0):
    start_time = time.time()

    while True:
        names = search_pods(namespace, name)

        if name not in names:
            break

        time.sleep(0.1)

        if timeout != 0:
            if time.time() - start_time > timeout:
                raise Exception("Timed out")