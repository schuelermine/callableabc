from abc import ABCMeta
from inspect import signature

__all__ = ("CallableABCMetaDict", "CallableABCMeta", "CallableABC")


class CallableABCMetaDict(
    dict[str, object],
):
    """
    Dictionary used by CallableABCMeta to collect the definition of _class_call().
    """

    _class_call: object | None

    __slots__ = ("_class_call",)

    def __init__(self, *args: object, **kwargs: object) -> None:
        self._class_call = None
        super().__init__(self, *args, **kwargs)

    def __setitem__(self, key: str, value: object, /) -> None:
        if key == "_class_call":
            self._class_call = value
        super().__setitem__(key, value)


class CallableABCMeta(ABCMeta):
    """
    A metaclass that works like abc.ABC,
    but allows you to customize what happens when the class object gets called
    by implementing a _class_call() classmethod.
    """

    _class_call: object | None

    @classmethod
    def __prepare__(
        cls, __name: str, __bases: tuple[type, ...], **kwds: object
    ) -> CallableABCMetaDict:
        return CallableABCMetaDict()

    def __init__(
        self, name: str, bases: tuple[type, ...], namespace: CallableABCMetaDict
    ) -> None:
        self._class_call = namespace._class_call
        super().__init__(name, bases, namespace)

    def __call__(self, *args: object, **kwds: object) -> object:
        _class_call = self._class_call
        if _class_call is not None and callable(_class_call):
            try:
                # Try to catch incorrect args early to hide __class_call__
                sig = signature(_class_call)
                sig.bind(*args, **kwds)
            except ValueError:  # Signature does not exist
                pass
            return _class_call(*args, **kwds)
        return super().__call__(*args, **kwds)


class CallableABC(metaclass=CallableABCMeta):
    """
    Inherit this class and define a classmethod _class_call() to get an ABC but with custom call behaviour.
    Convenience instance of CallableABCMeta.
    """

    __slots__ = ()
