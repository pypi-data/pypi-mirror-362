def forwardable(cls):
    def create_accessor(target, attrname):
        return lambda self: getattr(getattr(self, target), attrname)

    used_names = set()

    for target, attrnames in cls.__delegator_definitions__.items():
        if isinstance(attrnames, str):
            attrnames = [attrnames]

        for attrname in attrnames:
            if attrname in used_names:
                raise RuntimeError(f'Forwarding atttribute "{attrname}" is defined twice')
            setattr(cls, attrname, property(create_accessor(target, attrname)))
            used_names.add(attrname)

    return cls
