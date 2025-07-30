from pydecora.decorators.singleton import singleton

def test_singleton_instance():
    @singleton
    class A:
        def __init__(self, val):
            self.val = val

    a1 = A(10)
    a2 = A(20)

    assert a1 is a2
    assert a1.val == 10
