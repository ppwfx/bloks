import shutit
import sys
import os
import subprocess
import logging as log

from bloks import gtx




def runo(command, check=True, env={}):
    log.info(__name__ + ".runo : " + str(locals()))

    completed = None
    try:
        completed = subprocess.run(command, shell=True, check=check, env={})
    except Exception as e:
        log.error("command failed")

        if gtx.get(["_ignore-errors"]) == False:
            raise

    return completed


def run(command):
    log.info(__name__ + ".run " + str(locals()))

    completed = None
    try:
        completed = subprocess.run(command, shell=True, check=True,
                                   stdout=subprocess.PIPE)
    except Exception as e:
        log.info("command failed")
        raise

    return completed