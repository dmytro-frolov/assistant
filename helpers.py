from threading import Thread


def run_in_thread(fn):
    def run(*k, **kw):
        name = fn.__name__
        t = Thread(target=fn, args=k, kwargs=kw, name=name)
        t.start()
        return t
    return run


class EffectSingleTone(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if EffectSingleTone._instance is None:
            EffectSingleTone._instance = object.__new__(cls)

        return EffectSingleTone._instance
