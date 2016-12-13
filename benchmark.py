#!/usr/bin/python

class benchmark():
    """flag mean that value is more bigger more better or more smaller more better."""
    def __init__(self, name, value, flag):
        self.name = name
        self.value = value
        self.flag = flag

    def __repr__(self):
        #return ":".join([self.name, self.value])
        return "<benchmark object>"

    def __add__(self, other):
        if (self.name != other.name):
            raise TypeError
        if (self.flag != other.flag):
            raise TypeError
        value = self.value + other.value
        return benchmark(self.name, value, self.flag)
