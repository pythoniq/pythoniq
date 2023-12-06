def singleton(cls):
    class SingletonClass(cls):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if SingletonClass._instance is None:
                SingletonClass._instance = super(SingletonClass, cls).__new__(cls, *args, **kwargs)
                SingletonClass._instance._sealed = False

            return SingletonClass._instance

        def __init__(self, *args, **kwargs):
            if self._sealed:
                return

            super(SingletonClass, self).__init__(*args, **kwargs)
            self._sealed = True

    SingletonClass.__name__ = cls.__name__

    return SingletonClass
