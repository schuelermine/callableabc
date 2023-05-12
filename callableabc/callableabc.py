from abc import ABCMeta


def make_callable_abc_meta(class_call_name: str, /) -> type:
    class CallableABCMeta(ABCMeta):
        def __init__(
            self, name: str, bases: tuple[type, ...], namespace: dict[str, object]
        ) -> None:
            if class_call_name not in namespace:
                raise TypeError(
                    f"can't create CallableABC({class_call_name!r}) class without a {class_call_name} method"
                )
            super().__init__(name, bases, namespace)

        __init__.qualname = "CallableABCMeta.__init__"  # type: ignore

        def __call__(self, *args: object, **kwargs: object) -> object:
            return getattr(self, class_call_name)(*args, **kwargs)

        __call__.qualname = "CallableABCMeta.__call__"  # type: ignore

    CallableABCMeta.__qualname__ = "CallableABCMeta"
    return CallableABCMeta


def make_callable_abc(class_call_name: str = "class_call", /) -> type:
    callable_abc = make_callable_abc_meta(class_call_name)(
        "CallableABC", (), {class_call_name: staticmethod(make_callable_abc)}
    )
    callable_abc.__qualname__ = "CallableABC"
    return callable_abc


CallableABC: type = make_callable_abc()
