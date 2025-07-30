import math
Pi = 3.14159265358979323846
h = (6.626 * (10 ** -34))
h_bar = (h / (2 * Pi))

def EnergyLevelsPlanckConstant(v: float) -> float:
    ELP = h * v
    print(f"SADUFINANCE RESULT OF (PLANCK'S-BASED) ENERGY LEVELS: {ELP}")

def EnergyLevelsReducedPlanck(n: int, w: float) -> float:
    ELRP = (n + 0.5) * (h_bar * w)
    print(f"SADUFINANCE RESULT OF (REDUCED-PLANCK'S-BASED) ENERGY LEVELS: {ELRP}")


def WaveFunction(m: float, w: float, n: float, e: float, H: float, x: float) -> float:
    ELWF = (math.sqrt((m * w) / (Pi * h_bar)) * (1 / math.sqrt((2 ** n) * math.factorial(n))) * (
                ((m * w) / h_bar) ** 1 / 4) * e * H * (math.sqrt(((m * w) / h_bar) * x)))
    print(f"SADUFINANCE RESULT OF (WAVE-FUNCTION-BASED) ENERGY LEVELS: {ELWF}")


def QuantumHarmonicOscillator(m: float, d: float, x: float, w: float) -> float:
    QHO = (-((h_bar ** 2) / (2 * m)) * ((d ** 2) / (d * (x ** 2))) * 0.5 * m * (w ** 2) * (x ** 2))
    print(f"SADUFINANCE RESULT OF QUANTUM HARMONIC OSCILLATOR: {QHO}")


def QuantumAnharmonicOscillator(m: float, w: float, x: float, s: float) -> float:
    QAO = ((0.5 * m * (w ** 2) * (x ** 2)) + ((s / 4) * (x ** 4)))
    print(f"SADUFINANCE RESULT OF QUANTUM ANHARMONIC OSCILLATOR: {QAO}")


def QuantumAnharmonicHamiltonian(m: float, d: float, x: float, w: float, s: float) -> float:
    HAMILTONIAN = (-((h_bar ** 2) / (2 * m)) * ((d ** 2) / (d * (x ** 2))) * (
                0.5 * m * (w ** 2) * (x ** 2) + (s / 4) * (x ** 4)))
    print(f"SADUFINANCE RESULT OF ANHARMONIC OSCILLATOR HAMILTONIAN OPERATOR: {HAMILTONIAN}")

def PerturbationTheory(n: float, w: float, s: float, m: float, d: float, e: float, x: float) -> float:
    PERTURBATION = (((n + 0.5) * (h_bar * w)) + s * ((math.sqrt((m * w) / (Pi * h_bar)) * (
                 1 / math.sqrt((2 ** n) * math.factorial(n))) * (((m * w) / h_bar) ** 1 / 4) * e * (
                                                                      -((h_bar ** 2) / (2 * m)) * (
                                                                          (d ** 2) / (d * (x ** 2))) * (
                                                                                  0.5 * m * (w ** 2) * (x ** 2) + (
                                                                                      s / 4) * (x ** 4))) * (
                                                              math.sqrt(((m * w) / h_bar) * x))) * ((x ** 4) / 4) * (
                                                                     math.sqrt((m * w) / (Pi * h_bar)) * (1 / math.sqrt(
                                                                 (2 ** n) * math.factorial(n))) * (
                                                                                 ((m * w) / h_bar) ** 1 / 4) * e * (
                                                                                 -((h_bar ** 2) / (2 * m)) * (
                                                                                     (d ** 2) / (d * (x ** 2))) * (
                                                                                             0.5 * m * (w ** 2) * (
                                                                                                 x ** 2) + (s / 4) * (
                                                                                                         x ** 4))) * (
                                                                         math.sqrt(((m * w) / h_bar) * x)))))
    print(f"SADUFINANCE RESULT OF PERTURBATION THEORY: {PERTURBATION}")


def DimensionalOscillatorEnergy(w: float, N: int) -> float:
    DQHOEL = ((h_bar * w) * (sum(range(N + 1)) + (N / 2)))
    print(f"SADUFINANCE RESULT OF DIMENSIONAL OSCILLATOR ENERGY: {DQHOEL}")

