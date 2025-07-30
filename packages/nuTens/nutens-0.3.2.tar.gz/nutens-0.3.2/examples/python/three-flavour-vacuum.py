import nuTens as nt
from nuTens import tensor
from nuTens.tensor import Tensor
import matplotlib.pyplot as plt
import typing

N_ENERGIES = 10000

def build_PMNS(theta12: Tensor, theta13: Tensor, theta23: Tensor, deltaCP: Tensor):
    """ Construct a PMNS matrix in the usual parameterisation """
    # set up the three matrices to build the PMNS matrix
    M1 = Tensor.zeros([1, 3, 3], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)
    M2 = Tensor.zeros([1, 3, 3], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)
    M3 = Tensor.zeros([1, 3, 3], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)

    M1.set_value([0, 0, 0], 1.0)
    M1.set_value([0, 1, 1], tensor.cos(theta23))
    M1.set_value([0, 1, 2], tensor.sin(theta23))
    M1.set_value([0, 2, 1], -tensor.sin(theta23))
    M1.set_value([0, 2, 2], tensor.cos(theta23))
    M1.requires_grad(True)

    M2.set_value([0, 1, 1], 1.0)
    M2.set_value([0, 0, 0], tensor.cos(theta13))
    M2.set_value([0, 0, 2], tensor.mul(tensor.sin(theta13), tensor.exp(tensor.scale(deltaCP, -1.0J))))
    M2.set_value([0, 2, 0], -tensor.mul(tensor.sin(theta13), tensor.exp(tensor.scale(deltaCP, 1.0J))))
    M2.set_value([0, 2, 2], tensor.cos(theta13))
    M2.requires_grad(True)

    M3.set_value([0, 2, 2], 1.0)
    M3.set_value([0, 0, 0], tensor.cos(theta12))
    M3.set_value([0, 0, 1], tensor.sin(theta12))
    M3.set_value([0, 1, 0], -tensor.sin(theta12))
    M3.set_value([0, 1, 1], tensor.cos(theta12))
    M3.requires_grad(True)

    # Build PMNS
    PMNS = tensor.matmul(M1, tensor.matmul(M2, M3))
    PMNS.requires_grad(True)

    return PMNS


## First we build up a tensor to contain the test energies
energies = Tensor.ones([N_ENERGIES, 1], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, False)

for i in range(N_ENERGIES):
    energies.set_value([i,0], (1.0e-6 + i*0.2e-3) * nt.units.GeV)

energies.requires_grad(True)

## define tensors with oscillation parameters
theta23 = Tensor([0.82], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)
theta13 = Tensor([0.15], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)
theta12 = Tensor([0.58], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)
deltaCP = Tensor([1.5], nt.dtype.scalar_type.complex_float, nt.dtype.device_type.cpu, True)

## make the matrix
PMNS = build_PMNS(theta12, theta13, theta23, deltaCP)

## set the mass tensor
masses = Tensor.zeros([1,3], nt.dtype.scalar_type.float, nt.dtype.device_type.cpu, True)

masses.set_value([0,0], 0.0)
masses.set_value([0,1], 0.00868 * nt.units.eV)
masses.set_value([0,2], 0.0501 * nt.units.eV)

## print info about the parameters
print("PMNS: ")
print(PMNS.to_string())

print("\nMasses: ")
print(masses.to_string())
print()

## set up the propagator object
propagator = nt.propagator.Propagator(3, 295.0 * nt.units.km)
matter_solver = nt.propagator.ConstDensitySolver(3, 2.79)

propagator.set_PMNS(PMNS)
propagator.set_masses(masses)

## uncomment for matter oscillations
#propagator.set_matter_solver(matter_solver)

## run!
propagator.set_energies(energies)
probabilities = propagator.calculate_probabilities()

## print out some test values
prob_sum = tensor.scale(tensor.sum(probabilities, [0]), 1.0 / float(N_ENERGIES))
print("energy integrated probabilities: ")
print(prob_sum.to_string())

## check that the autograd functionality works
mu_survival_prob = prob_sum.get_values([1,1])
print("mu survival prob:")
print(mu_survival_prob.to_string())

mu_survival_prob.backward()
print("theta_13 grad: ")
print(theta13.grad().to_string())


## make plots of the oscillation probabilities
energy_list = []
e_survival_prob_list = []
mu_survival_prob_list = []
tau_survival_prob_list = []

mu_to_e_prob_list = []
mu_to_tau_prob_list = []
mu_total_prob_list = []

for i in range(N_ENERGIES):
    energy_list.append(energies.get_value([i, 0]))
    e_survival_prob_list.append(probabilities.get_value([i, 0, 0]))
    mu_survival_prob_list.append(probabilities.get_value([i, 1, 1]))
    tau_survival_prob_list.append(probabilities.get_value([i, 2, 2]))

    mu_to_e_prob_list.append(probabilities.get_value([i, 1, 0]))
    mu_to_tau_prob_list.append(probabilities.get_value([i, 1, 2]))

    mu_total_prob_list.append(
        probabilities.get_value([i, 1, 0]) +
        probabilities.get_value([i, 1, 1]) + 
        probabilities.get_value([i, 1, 2])
    )

plt.plot([ e / nt.units.GeV for e in energy_list], e_survival_prob_list, label = "electron")
plt.plot([ e / nt.units.GeV for e in energy_list], mu_survival_prob_list, label = "muon")
plt.plot([ e / nt.units.GeV for e in energy_list], tau_survival_prob_list, label = "tau")
plt.xlabel("Energy [GeV]")
plt.ylabel("Survival probability")
plt.legend()
plt.show()
plt.savefig("survival_probs.png")

plt.clf()
fig, axs = plt.subplots(2, 1, sharex=True)
axs[1].plot([ e / nt.units.GeV for e in energy_list], mu_to_e_prob_list, label = "numu -> nue")
axs[1].set_ylim((0.0, 0.1))
axs[0].plot([ e / nt.units.GeV for e in energy_list], mu_to_tau_prob_list, label = "numu -> nutau")
axs[0].plot([ e / nt.units.GeV for e in energy_list], mu_survival_prob_list, label = "numu -> numu")
axs[0].plot([ e / nt.units.GeV for e in energy_list], mu_total_prob_list, label = "Total")
axs[1].set_xlabel("Energy [GeV]")
axs[0].legend()
axs[1].legend()
fig.suptitle("Three flavour oscillation probabilities")
fig.supylabel("Oscillation probability")
fig.savefig("oscillation_probs.png")
