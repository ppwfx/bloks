import os
import shutil
import logging


def env(names):
    complete = True
    for name in names:
        if os.getenv(name) is None:
            complete = False
            logging.info("env variable {} is missing".format(name))

    if not complete:
        raise Exception("incomplete environment variables")


def executables(names):
    complete = True
    for name in names:
        if shutil.which(name) is None:
            complete = False
            logging.info("executable {} is missing".format(name))

    if not complete:
        raise Exception("incomplete environment variables")

