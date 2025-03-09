import numpy as np
import numpy.typing as npt
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform
from qadence import RydbergDevice, QuantumModel, chain, AnalogRX, AnalogRZ, QuantumCircuit, Register
import torch
from qadence.ml_tools import Trainer, TrainConfig, num_parameters
import nevergrad as ng
import matplotlib.pyplot as plt

global Q

def qubo_register_coords(Q: np.ndarray, device: RydbergDevice) -> list:
    """Compute coordinates for register."""

    def evaluate_mapping(new_coords, *args):
        """Cost function to minimize. Ideally, the pairwise
        distances are conserved"""
        Q, shape = args
        new_coords = np.reshape(new_coords, shape)
        interaction_coeff = device.coeff_ising
        new_Q = squareform(interaction_coeff / pdist(new_coords) ** 6)
        return np.linalg.norm(new_Q - Q)

    shape = (len(Q), 2)
    np.random.seed(0)
    x0 = np.random.random(shape).flatten()
    res = minimize(
        evaluate_mapping,
        x0,
        args=(Q, shape),
        method="Nelder-Mead",
        tol=1e-6,
        options={"maxiter": 200000, "maxfev": None},
    )
    return [(x, y) for (x, y) in np.reshape(res.x, (len(Q), 2))]

# Loss function to guide the optimization routine
def loss(model: QuantumModel, *args) -> tuple[torch.Tensor, dict]:
    global Q
    to_arr_fn = lambda bitstring: np.array(list(bitstring), dtype=int)
    cost_fn = lambda arr: arr.T @ Q @ arr
    samples = model.sample({}, n_shots=1000)[0]
    cost_fn = sum(samples[key] * cost_fn(to_arr_fn(key)) for key in samples)
    return torch.tensor(cost_fn / sum(samples.values())), {}

def q_register(Q: np.array):
    # Device specification and atomic register
    device = RydbergDevice(rydberg_level=70)

    reg = Register.from_coordinates(
        qubo_register_coords(Q, device), device_specs=device
    )

    # Analog variational quantum circuit
    layers = 2
    block = chain(*[AnalogRX(f"t{i}") * AnalogRZ(f"s{i}") for i in range(layers)])
    circuit = QuantumCircuit(reg, block)

    return circuit

def q_qubo(circuit, Q_calc):

    Q = Q_calc
    model = QuantumModel(circuit)
    # initial_counts = model.sample({}, n_shots=1000)[0]

    Trainer.set_use_grad(False)

    config = TrainConfig(max_iter=100)

    optimizer = ng.optimizers.NGOpt(
        budget=config.max_iter, parametrization=num_parameters(model)
    )

    # train_dataloader = to_dataloader(Q)
    
    trainer = Trainer(model, optimizer, config, loss)

    trainer.fit()

    optimal_counts = model.sample({}, n_shots=1000)[0]

    return optimal_counts

def q_plot(initial_counts, optimal_counts):
    # Known solutions to the QUBO problem.
    # solution_bitstrings = ["01011", "00111"]

    def plot_distribution(C, ax, title):
        C = dict(sorted(C.items(), key=lambda item: item[1], reverse=True))
        # color_dict = {key: "r" if key in solution_bitstrings else "b" for key in C}
        ax.set_xlabel("bitstrings")
        ax.set_ylabel("counts")
        ax.set_xticks([i for i in range(len(C.keys()))], C.keys(), rotation=90)
        # ax.bar(C.keys(), C.values(), color=color_dict.values())
        ax.set_title(title)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    plot_distribution(initial_counts, axs[0], "Initial counts")
    plot_distribution(optimal_counts, axs[1], "Optimal counts")