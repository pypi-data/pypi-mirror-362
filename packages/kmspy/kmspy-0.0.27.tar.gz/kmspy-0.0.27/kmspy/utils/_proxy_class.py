from typing import Dict, List


changer_methods = set("__setitem__ __setslice__ __delitem__ update append extend add insert pop popitem remove setdefault __iadd__".split())


def _callback_getter(obj):
    def callback(name):
        obj._has_changed = True
    return callback

def _proxy_decorator(func, callback):
    def wrapper(*args, **kw):
        callback(func.__name__)
        return func(*args, **kw)
    wrapper.__name__ = func.__name__
    return wrapper

def _proxy_class(cls, obj):
    new_dct = cls.__dict__.copy()
    for key, value in new_dct.items():
        if key in changer_methods:
            new_dct[key] = _proxy_decorator(value, _callback_getter(obj))
    return type("proxy_"+ cls.__name__, (cls,), new_dct)


class TrackedClass:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_changed = False

    def __getattribute__(self, name):
        if name in changer_methods:
            self.has_changed = True
        return super().__getattribute__(name)


def change_tracker(cls):
    return type(cls.__name__, (TrackedClass, cls), {})


@change_tracker
class ObservableList(List):...


@change_tracker
class ObservableDict(Dict):...


# 동적으로 생성할 수도 있지만, 자동완성이 되지 않음
# for cls in [list, dict]:
#     class_name = f"Observable{cls.__name__.title()}"
#     globals()[class_name] = change_tracker(type(class_name, (cls,), {}))


if __name__ == "__main__":
    NotifierList = ObservableList()

    print("Before", NotifierList.has_changed)
    # Before False
    NotifierList.append(0)
    print("After", NotifierList.has_changed)
    # After True
