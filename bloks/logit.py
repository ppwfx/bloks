import time
import logging
from inspect import getargspec

level = 0
on = True


def get_indent():
    global level
    return " |   " * level


def log(text):
    for l in text.split("\n"):
        if on:
            logging.info("%s %s", get_indent(), l)
        else:
            print(l)


def deco(log_return=True):
    def deco(fn):
        def wrapper(*args, **kwargs):
            t1 = time.time()

            #enrich simple args somehow
            #args = args
            # print(args)
            #
            # argspec = getargspec(fn)
            # print(argspec)
            #
            # arg_map = {}
            # for i, name in enumerate(argspec[0]):
            #     if i + 1 == len(args):
            #         break
            #     arg_map[name] = args[i]

            kargs = kwargs

            mod = str.replace(fn.__module__, "bloks.", "")
            mod = str.replace(mod, ".facade", "")

            if on:
                log("{} {} {}".format(mod, fn.__name__ , kargs))

            global level
            level += 1
            returnn = fn(*args, **kwargs)
            level -= 1


            t2 = time.time()
            duration = str((t2 - t1))

            du = round(float(duration), 2)

            if on:
                if log_return:
                    if returnn == None:
                        returnn = ""
                    log(" ⦦ {} {}".format(du, returnn))
                else:
                    log(" ⦦ {}".format(du))


            return returnn

        return wrapper

    return deco