# Used for Brython, so live reloads on Python files work
# FIXME: use in pyscript/micropython

class MockObject:
    def __init__(self, name=None):
        # Directly assign to __dict__ to avoid triggering our custom __setattr__
        self.__dict__["_name"] = name

    def __getattr__(self, name):
        # Return new MockObject for any requested attribute
        return MockObject(name=name)

    def __setattr__(self, name, value):
        # Allow setting "private" attributes (starting with _)
        if name.startswith("_"):
            super().__setattr__(name, value)
        # Ignore all other attribute assignments
        # (they won't be stored and will remain mockable)

    def __call__(self, *args, **kwargs):
        # Return new mock object when called as a function
        return MockObject()

    def __repr__(self):
        return f"<MockObject {self._name}>" if self._name else "<MockObject>"

# Module-level implementation
_cache = {}

def __getattr__(name):
    if name not in _cache:
        _cache[name] = MockObject(name=name)
    return _cache[name]
