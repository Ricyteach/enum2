class EnumMeta(type):
    """Enum type metaclass."""

    _lookup = {}
    _members = {}

    def __init__(cls, name, bases, dct):
        super(EnumMeta, cls).__init__(name, bases, dct)
        drop = [
            "__module__",
            "__qualname__",
            "__doc__",
            "__metaclass__",
            "__new__",
            "__str__",
            "__repr__",
        ]
        member_dct = {name: value for name, value in dct.items() if name not in drop}
        EnumMeta._members[cls] = []
        members_list = EnumMeta._members[cls]
        for name, value in member_dct.items():
            obj = object.__new__(cls)
            obj.value = value
            obj.name = name
            setattr(cls, name, obj)
            members_list.append(obj) 

        EnumMeta._lookup.update(
            {cls: {value: name for name, value in member_dct.items()}}
        )


class Enum(object):
    """Parent class for an Enum type."""

    __metaclass__ = EnumMeta

    def __new__(cls, value):
        if value in cls._members[cls]:
            return value
        try:
            return getattr(cls, cls._lookup[cls][value])
        except (AttributeError, KeyError):
            raise ValueError("Invalid {} value: {!r}".format(cls.__name__, value))

    def __str__(self):
        return "{:s}.{:s}".format(type(self).__name__, self.name)

    def __repr__(self):
        return "<{:s}.{:s}: {!r}>".format(type(self).__name__, self.name, self.value)


if __name__ == "__main__":
    # tests
    class C(Enum):
        x = 1
        y = 2

    assert C.x.name == "x"
    assert C.x.value == 1
    assert C(1) == C.x
    try:
        C(12)
    except ValueError:
        pass
    else:
        assert False
