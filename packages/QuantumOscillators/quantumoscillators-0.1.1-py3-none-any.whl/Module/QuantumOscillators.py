import math
from typing import Optional

Pi = 3.14159265358979323846
h = (6.626 * (10 ** -34))
h_bar = (h / (2 * Pi))


class QuantumOscillators:
    def __init__(self, x1: float, x2: float, x3: float, x4: float, x5: float, x6: float, x7: float, x8: float,
                 x9: float, x10: float) -> float:
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.x7 = x7
        self.x8 = x8
        self.x9 = x9
        self.x10 = x10

    def EnergyLevelsPlanckConstant(v: float) -> float:
        ELP = h * v
        print(f"SADUFINANCE RESULT OF (PLANCK'S-BASED) ENERGY LEVELS: {ELP}")

    def EnergyLevelsReducedPlanck(n: int, w: float) -> float:
        ELRP = (n + 0.5) * (h_bar * w)
        print(f"SADUFINANCE RESULT OF (REDUCED-PLANCK'S-BASED) ENERGY LEVELS: {ELRP}")
        '''
        1. n: REPRESENTS THE QUANTUM NUMBER.
        2. w: REPRESENTS THE ANGULAR FREQUENCY.
        '''

    def WaveFunction(m: float, w: float, n: float, e: float, H: float, x: float) -> float:
        ELWF = (math.sqrt((m * w) / (Pi * h_bar)) * (1 / math.sqrt((2 ** n) * math.factorial(n))) * (
                    ((m * w) / h_bar) ** 1 / 4) * e * H * (math.sqrt(((m * w) / h_bar) * x)))
        print(f"SADUFINANCE RESULT OF (WAVE-FUNCTION-BASED) ENERGY LEVELS: {ELWF}")
        '''
        1. H: REPRESENTS HARMITE POLYNOMIALS OPERATOR. GOT RELATION WITH OBSERVABLES.
        2. x: REPRESENTS PARTICLE'S POSITION.
        3: n: REPRESENTS THE QUANTUM NUMBER.
        '''

    def QuantumHarmonicOscillator(m: float, d: float, x: float, w: float) -> float:
        QHO = (-((h_bar ** 2) / (2 * m)) * ((d ** 2) / (d * (x ** 2))) * 0.5 * m * (w ** 2) * (x ** 2))
        print(f"SADUFINANCE RESULT OF QUANTUM HARMONIC OSCILLATOR: {QHO}")
        '''
        1. h: (PRONOUNCED h BAR) - REPRESENTS THE REDUCED PLANC'S CONSTANT, THAT IS RELATED TO ENERGY AND ITS DYNAMICS.
        2. m: REPRESENTS THE MASS OF THE PARTICLE.
        3. x: REPRESENTS THE POSITION OF THE PARTICLE IN THE QUANTUM SPACE; i.e HILBERT SPACE.
        4. w: REPRESENTS THE ANGULAR FREQUENCY OF THE PARTICLE, -- OTHER QUANTUM DYNAMICS DETERMINES ITS VALUE --.
        '''

    def QuantumAnharmonicOscillator(m: float, w: float, x: float, s: float) -> float:
        QAO = ((0.5 * m * (w ** 2) * (x ** 2)) + ((s / 4) * (x ** 4)))
        print(f"SADUFINANCE RESULT OF QUANTUM ANHARMONIC OSCILLATOR: {QAO}")
        '''
        s: REPRESENTS THE STRENGTH OF ANHARMONICITY.
        '''

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
        '''
        1. s: REPRESENTS THE ANHARMONIC STRENGTH.
        2. PERTURBATION THEORY APPLIED ON CERTIAN TYPES OF THE QFT.
        3. SPECIFIC COMPLICATED ARGUMENTS ARE SOLVED ON BEHALF OF YOU.
        '''

    def DimensionalOscillatorEnergy(w: float, N: int) -> float:
        DQHOEL = ((h_bar * w) * (sum(range(N + 1)) + (N / 2)))
        print(f"SADUFINANCE RESULT OF DIMENSIONAL OSCILLATOR ENERGY: {DQHOEL}")

    def NDIMENSIONALHARMONICOSCILLATOR(self, s: float, dt: float, m: float, w: float):
        DerivativeX1 = ((s * (self.x1 + dt) - s * (self.x1)) / dt)
        DerivativeX2 = ((s * (self.x2 + dt) - s * (self.x2)) / dt)
        DerivativeX3 = ((s * (self.x3 + dt) - s * (self.x3)) / dt)
        DerivativeX4 = ((s * (self.x4 + dt) - s * (self.x4)) / dt)
        DerivativeX5 = ((s * (self.x5 + dt) - s * (self.x5)) / dt)
        DerivativeX6 = ((s * (self.x6 + dt) - s * (self.x6)) / dt)
        DerivativeX7 = ((s * (self.x7 + dt) - s * (self.x7)) / dt)
        DerivativeX8 = ((s * (self.x8 + dt) - s * (self.x8)) / dt)
        DerivativeX9 = ((s * (self.x9 + dt) - s * (self.x9)) / dt)
        DerivativeX10 = ((s * (self.x10 + dt) - s * (self.x10)) / dt)
        NDHO1 = (-((h_bar ** 2) / 2 * m) * (DerivativeX1) + (0.5 * m * (w ** 2)) * (self.x1 ** 2))
        NDHO2 = (-((h_bar ** 2) / 2 * m) * (DerivativeX1 + DerivativeX2) + (0.5 * m * (w ** 2)) * (
                    (self.x1 ** 2) + (self.x2 ** 2)))
        NDHO3 = (-((h_bar ** 2) / 2 * m) * (DerivativeX1 + DerivativeX2 + DerivativeX3) + (0.5 * m * (w ** 2)) * (
                    (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2)))
        NDHO4 = (-((h_bar ** 2) / 2 * m) * (DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4) + (
                    0.5 * m * (w ** 2)) * ((self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2)))
        NDHO5 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5) + (0.5 * m * (w ** 2)) * (
                             (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2)))
        NDHO6 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5 + DerivativeX6) + (
                             0.5 * m * (w ** 2)) * (
                             (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2) + (
                                 self.x6 ** 2)))
        NDHO7 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5 + DerivativeX6 + DerivativeX7) + (
                             0.5 * m * (w ** 2)) * (
                             (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2) + (
                                 self.x6 ** 2) + (self.x7 ** 2)))
        NDHO8 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5 + DerivativeX6 + DerivativeX7 + DerivativeX8) + (
                             0.5 * m * (w ** 2)) * (
                             (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2) + (
                                 self.x6 ** 2) + (self.x7 ** 2) + (self.x8 ** 2)))
        NDHO9 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5 + DerivativeX6 + DerivativeX7 + DerivativeX8 + DerivativeX9) + (
                             0.5 * m * (w ** 2)) * (
                             (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2) + (
                                 self.x6 ** 2) + (self.x7 ** 2) + (self.x8 ** 2) + (self.x9 ** 2)))
        NDHO10 = (-((h_bar ** 2) / 2 * m) * (
                    DerivativeX1 + DerivativeX2 + DerivativeX3 + DerivativeX4 + DerivativeX5 + DerivativeX6 + DerivativeX7 + DerivativeX8 + DerivativeX9 + DerivativeX10) + (
                              0.5 * m * (w ** 2)) * (
                              (self.x1 ** 2) + (self.x2 ** 2) + (self.x3 ** 2) + (self.x4 ** 2) + (self.x5 ** 2) + (
                                  self.x6 ** 2) + (self.x7 ** 2) + (self.x8 ** 2) + (self.x9 ** 2) + (self.x10 ** 2)))
        print(
            f"SADUPOST RESULT OF DERIVATIVES OF THE FOLLOWING DIMENSIONS --> 1D: {DerivativeX1}, 2D: {DerivativeX2}, 3D: {DerivativeX3}, 4D: {DerivativeX4}, 5D: {DerivativeX5}, 6D: {DerivativeX6}, 7D: {DerivativeX7}, 8D: {DerivativeX8}, 9D: {DerivativeX9}, 10D: {DerivativeX10}")
        print(
            f"SADUPOST RESULT OF DIMENSIONAL OSCILLATOR ACCORDING TO NUMBER OF DIMENSIONS --> 1D: {NDHO1},  2D: {NDHO2}, 3D: {NDHO3}, 4D: {NDHO4}, 5D: {NDHO5}, 6D: {NDHO6}, 7D: {NDHO7}, 8D: {NDHO8}, 9D: {NDHO9}, 10D: {NDHO10},")
        '''
        REMARKS: THE METHOD DEMONSTRATES DERIVATIVES AND N-DIMENSIONAL OSCILLATOR RESULTS.
        THE METHOD DISPLAYS ALL POSSIBLE VALUES ACCORDING TO THE NUMBER OF DIMENSIONS OF THE QUANTUM SYSTEM OF DESIRE.
        THE METHOD RELIES ON THE PROVIDED NUMBER OF x (position) VALUES INPUTED TO THE CLASS *NOT TO THE METHOD.
        THE METHOD TAKES THESE VALUES, CALCULATES EACH POSSIBLE DIMENSION BASED ON THESE INPUT VALUES.
        INSTRUCTIONS -- METHOD SPECIFIC --:
        FIRST CREATE AN OBJECT AS AN INSTANCE OF THE CLASS.
        SECOND USING THIS OBJECT TO NAVIGATE TO THIS METHOD AND PROVIDE THE REQUIRED ARGUMENTS.
        '''


'''
THE FOLLOWING REPRESENTS AN EXAMPLES OF HOW TO USE THE METHODS ABOVE:
CHANGE THE VALUES WITH YOUR OWN:
'''
'''
QuantumOscillators.EnergyLevelsPlanckConstant(2.4392)
QuantumOscillators.EnergyLevelsReducedPlanck(1.23, 0.834)
QuantumOscillators.QuantumHarmonicOscillator(1.2, 4.2, 0.9, 0.34565)
QuantumOscillators.QuantumAnharmonicOscillator(1.9, 0.894, 2, 0.8)
QuantumOscillators.QuantumAnharmonicHamiltonian(1.783, 1.2, 2, 0.234, 1.938)
QuantumOscillators.PerturbationTheory(3, 1.2342, 0.834, 1.4325, 0.742, 0.2394, 2)
QuantumOscillators.DimensionalOscillatorEnergy(0.4532, 8)
QNDO = QuantumOscillators(0.348, 0.543, 1.3425, 0.12983, 0.2349, 1.9823, 1.3525, 0.93892, 0.9853, 1.242)
QNDO.NDIMENSIONALHARMONICOSCILLATOR(0.242, 0.342, 1.352, 0.3523)
'''
