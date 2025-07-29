class Argument:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


RAISE = Argument("raise")  # Constant indicates to raise when using this value.
SELF = Argument("self")  # Constant indicates to use itself using this value.
