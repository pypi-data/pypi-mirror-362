# Finding the ground state via imaginary time evolution

## TL;DR

```python
from scipy.constants import pi, Boltzmann
from matterwave.rb87 import m as m_rb87
from fftarray import FFTWave, FFTDimension
from matterwave import split_step, set_ground_state, get_e_kin
from jax.lax import scan

mass = m_rb87 # kg
omega_x_init = 2.*pi*0.1 # Hz
omega_x = 2.*pi # Hz
dt = 1e-4 # s

x = FFTDimension(pos_min = -200e-6, pos_max = 200e-6, freq_middle = 0., n = 2048)
wf_init = FFTWave(x = x)
wf_init = set_ground_state(wf_init, omega=omega_x_init, mass=mass)

def V_kernel(value: complex, x: float):
    return 0.5 * mass * omega_x**2. * x**2.

def step(wf: FFTWave, *_):
    E_kin = get_e_kin(wf, m=mass, return_microK=True) 
    E_pot = wf.expectation_value_pos(V_kernel) / (Boltzmann * 1e-6)
    E_tot = E_kin + E_pot
    wf = split_step(wf=wf, dt=dt, mass=mass, V_kernel=V_kernel, is_complex=True)
    return wf, {"E_kin": E_kin, "E_pot": E_pot, "E_tot": E_tot}

wf_final, energies = scan(f=step, init=wf_init, xs=None, length=10654)
```

## Physics

### Quantum harmonic oscillator
Consider the quantum harmonic oscillator (QHO) - the quantum-mechanical analog of the classical harmonic oscillator. The Hamiltonian is defined as 

```math
H = \hat T + \hat V = \frac{\hat p^2}{2m} + \frac{1}{2}m w^2\hat x^2
```

where $`\hat p`$ is the momentum operator, $`m`$ is the mass, $`\omega`$ is the angular frequency, and $`\hat x`$ is the position operator.

Our goal is to find the ground state of a one-dimensional QHO for a given angular frequency $`\omega_x`$. For a given initial state the imaginary time evolution can be iteratively applied to evolve the initial state to the ground state of our system. 

### The imaginary time evolution
The imaginary time evolution is equivalent to applying the split-step operator

```math
e^{-\tfrac{i}{\hbar}H \text{dt}} \approx e^{-\tfrac{i}{\hbar}\frac{\hat T}{2} \text{dt}} e^{-\tfrac{i}{\hbar}\hat V \text{dt}} e^{-\tfrac{i}{\hbar}\frac{\hat T}{2} \text{dt}}
```

with imaginary time step $`\text{dt}=-i\text{dt}`$. By exchanging the time step, the time evolution operator turns into a real-valued coefficient. Expanding the initial state in terms of eigenstates of the system $`\Psi = \sum_n a_n\Psi_n`$ reveals that each eigenstate $`\Psi_n`$ is scaled by $`e^{-\frac{1}{\hbar} E_n \text{dt}}a_n`$ where $`H \Psi_n = E_n \Psi_n`$. Thus, by iteratively applying the split-step operator an approximation for the ground state will remain. States with higher energy will be suppressed by their small coefficient. Note that the wavefunction has to be normalized after each application as the split-step operator became non-unitary. Spoiler alert: this is covered inside the `split_step` function if the argument `is_complex` is set to `True`.

## Code
Implementing the imaginary time evolution with the framework of unified_wf_2 is straightforward. Many required functions, e.g., the split-step operator application, are already efficiently defined and only need to be imported.

This example mainly covers the usage of the `FFTWave` class, the `split_step` function, and the computation of the wavefunction's kinetic and potential energy.

The output is presented in a panel dashboard. Simply run the python program by writing `panel serve dashboard.py --port 5006` into the terminal (assuming the terminal path is set to [this](https://gitlab.projekt.uni-hannover.de/iqo-seckmeyer/unified_wf_2/-/tree/examples/examples/imaginary_time_groundstate) directory). The dashboard can be found at http://localhost:5006/dashboard. If you want to make some changes to this program, add the flag `--autoreload` to the terminal command. By this, the dashboard will automatically reload, when you save changes.

Please make sure to have all the required packages installed (the installation guide can be found [here](https://gitlab.projekt.uni-hannover.de/iqo-seckmeyer/unified_wf_2)). 
