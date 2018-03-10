import googleapiclient.discovery

import google


def get_client():
    container = googleapiclient.discovery.build("container", "v1")

    google.storage

    return container.projects()
