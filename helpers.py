from threading import Thread


def run_in_thread(fn):
    def run(*k, **kw):
        name = fn.__name__
        t = Thread(target=fn, args=k, kwargs=kw, name=name)
        t.start()
        return t
    return run


class EffectSingleTone(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if EffectSingleTone.__instance is None:
            EffectSingleTone.__instance = object.__new__(cls)
            # EffectSingleTone.__instance = object.__init__(cls)

            EffectSingleTone.__instance.__init__(*args, **kwargs)
            pass
            # EffectSingleTone.__instance._args = args
            # EffectSingleTone.__instance._kwargs = kwargs

        return EffectSingleTone.__instance


