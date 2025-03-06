# Loading the necessary packages, please make any necessary python installations
# Can execute as is
from pulser import Pulse, Sequence, Register
from pulser_simulation import QutipEmulator
from pulser.devices import DigitalAnalogDevice
from pulser.waveforms import InterpolatedWaveform
from itertools import combinations
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
#import igraph

#Excercise A: reproducing a grpah arch
qubits = {'0':(0, 0), '1':(-4, -7), '2':(4, -7), '3':(8, 6), '4':(-8, 6)}
reg = Register(qubits)

#reg.draw(blockade_radius = DigitalAnalogDevice.rydberg_blockade_radius(1.0), draw_graph = True, draw_half_radius = True)

# Estimating sequence parameters
link_max = 10 # Insert your computation, Maximal distance in micrometers between connected qubits in the example quantum register
no_link_min = 13.6# Insert your computation, Minimal distance in micrometers between non-connected qubits in the example quantum register

# Parametrising the adiabatic evolution based on computed values
# Can execute as is
Omega_min = DigitalAnalogDevice.interaction_coeff / no_link_min**6
Omega_max = DigitalAnalogDevice.interaction_coeff / link_max**6
Omega = (Omega_max - Omega_min) / 2 # we choose a random value between the min and the max


# Detuning parameters for the adiabatic evolution
# Can execute as is
delta_0 = -5 # just has to be negative
delta_f = -delta_0 # just has to be positive
T = 4500 # time in ns, we choose a time long enough to ensure the propagation of information


# Building the sequence
adiabatic_pulse = Pulse(
    InterpolatedWaveform(T, [1e-9, Omega, 1e-9]),
    InterpolatedWaveform(T, [delta_0, 0, delta_f]),
    0,
)


# Creating the channel for the laser pulse
# Can execute as is
seq = Sequence(reg, DigitalAnalogDevice)
seq.declare_channel("ising", "rydberg_global")
seq.add(adiabatic_pulse, "ising")

# Executing the sequence
# Can execute as is
simul = QutipEmulator.from_sequence(seq)
results = simul.run()
final = results.get_final_state()
count_dict = results.sample_final_state()


def plot_distribution(C):
    C = dict(sorted(C.items(), key=lambda item: item[1], reverse=True))
    indexes = ["01011", "00111"] # MIS indexes
    color_dict = {key: "r" if key in indexes else "g" for key in C}
    plt.figure(figsize=(12, 6))
    plt.xlabel("bitstrings")
    plt.ylabel("counts")
    plt.bar(C.keys(), C.values(), width=0.5, color=color_dict.values())
    plt.xticks(rotation="vertical")
    plt.show()

#plot_distribution(count_dict)

success_probability = []
for T in 1000 * np.linspace(1, 10, 10):
    seq = Sequence(reg, DigitalAnalogDevice)
    seq.declare_channel("ising", "rydberg_global")
    adiabatic_pulse = Pulse(
        InterpolatedWaveform(T, [1e-9, Omega, 1e-9]),
        InterpolatedWaveform(T, [delta_0, 0, delta_f]),
        0,
    )
    seq.add(adiabatic_pulse, "ising")
    simul = QutipEmulator.from_sequence(seq)
    results = simul.run()
    final = results.get_final_state()
    count_dict = results.sample_final_state()
    success_probability.append((count_dict["01011"]+count_dict["00111"])/1000)
    
plt.figure(figsize=(12, 6))
plt.plot(range(1, 11), np.array(success_probability), "--o")
plt.xlabel("total time evolution (μs)", fontsize=14)
plt.ylabel("approximation ratio", fontsize=14)
plt.savefig('first test')
