import QuantumOscillators

class Wrapper:
    def __init__(self):
        self.Uncertainty = QuantumOscillators

    def __getattr__(self, item):
        return getattr(self.lib_ins, item)

    def documentation(self):
        return "for getting more information visit: "


Sadu = Wrapper()