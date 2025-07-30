# Bragg Beam Splitter

## TL;DR

Reduced version of [dashboard.py](dashboard.py):
```python
import jax.numpy as jnp
from jax.lax import scan
from fftarray import FFTWave, FFTDimension
from matterwave import set_ground_state, split_step
from scipy.constants import pi, hbar
from matterwave.rb87 import m as mass_rb87, k_L, hbarkv

# angular frequency used to initialize the ground state (of quantum harmonic oscillator)
omega_x = 2*pi*10 # Hz
w_r = 2 * hbarkv * k_L # rb87 constant
# Rabi frequency. This specific value was found as a binary search to optimize a 50/50 split of the two momentum classes for this specific beam splitter duration and pulse form.
rabi_frequency = 25144.285917282104 # Hz
phi_0 = 0. # phase jump
bragg_acc = 0. # bragg acceleration
sigma_bs = 25e-6 # temporal pulse width (s)
# define how many sigmas of the gauss to sample in each direction before reaching zero intensity:
sampling_range_mult = 4. # * sigma_bs
dt_bs = 1e-6 # time step size
# total number of pulse grid steps = gauss_width * scaling_factor / step_size
steps_limit = int(round(sigma_bs * sampling_range_mult / dt_bs))
t_offset = steps_limit*dt_bs
nt_bs = 2*steps_limit # number of time steps for beam splitter
steps_limit = int(round(sigma_bs * sampling_range_mult / dt_bs)) # max number of time steps
t_offset = steps_limit*dt_bs # the peak of the ramp
t_extent_bs = 2*t_offset # total time
t_list = jnp.arange(0, t_extent_bs+dt_bs, dt_bs) # time

x = FFTDimension(pos_min = -50e-6, pos_max = 50e-6, freq_middle=0., freq_extent = 10*k_L, loose_params = ["freq_extent"])
wf_init = FFTWave(x = x)
wf_init = set_ground_state(wf_init, omega = omega_x, mass = mass_rb87)

def gauss(t: float, sigma: float):
    return jnp.exp(-0.5 * (t / sigma)**2)

def V_kernel(value: float, x: float, ramp: float, t: float):
    return rabi_frequency * ramp * 2. * hbar * jnp.cos(
        k_L * (x - 0.5 * bragg_acc * t**2)
        - 0.5 * w_r * t
        + phi_0/2.
    )**2

gauss_offset = gauss(t = -t_offset, sigma = sigma_bs)

def step(wf: FFTWave, t: float):
    ramp = gauss(t = t-t_offset, sigma = sigma_bs) - gauss_offset
    wf = split_step(wf,
        mass = mass_rb87,
        dt = dt_bs,
        V_kernel = V_kernel, 
        kwargs = {"ramp": ramp, "t": t}
    )
    abs_pos = jnp.abs(wf.psi_pos)**2
    abs_freq = jnp.abs(wf.psi_freq)**2
    return wf, {"abs_pos": abs_pos, "abs_freq": abs_freq}

wf_final_bs, wf_data_bs = scan(f = step, init = wf_init, xs = t_list)
```

## Physics

### The Bragg Beam Splitter

The Bragg beam splitter splits the wavefunction into two momentum states (but same internal state). 
Here, the main physics is sketched. 
The interested reader is referred to [the textbook by Grynberg, Aspect and Fabre](https://www.cambridge.org/core/books/introduction-to-quantum-optics/F45DCE785DC8226D4156EC15CAD5FA9A). 

The formalism describing the Bragg atom-light interaction is based on a semi-classical model. 
The atoms are described via quantum mechanics (in terms of a wavefunction) while the light is described classically since its intensity is so high that there are always very many photons. 
The Hamiltonian of the system is:

```math
\hat H = \frac{\hat p^2}{2m} - \hat{\vec D} \vec E_L (\vec r, t)
```

where $`\hat p`$ is the momentum operator, $`\hat{\vec D}`$ is the dipole operator and $`\vec E_L`$ is the electric field. 
The electric field can be described by two counterpropagating laser beams with frequencies $`\omega_L+\omega_r`$ (drives the transition $`| g,0 \rangle \rightarrow | e, \hbar k_L \rangle`$) and $`\omega_r`$ (drives the transition $`| e, \hbar k_L \rangle \rightarrow | g, 2\hbar k_L\rangle`$). 
Note that $` \frac{(2\hbar k_L)^2}{2m} = \hbar \omega_r`$ . 
It should be noted that both lasers are detuned by $`\Delta`$, such that the transition $`|g,0 \rangle \rightarrow | e, \hbar k_L \rangle`$ is unlikely to happen without the stimulated emission directly after it. 
Here, a one dimensional wavefunction is considered: $`\Psi (x)`$. 
Adiabatic elimination of the excited state then leads to

```math
\hat H = -\frac{\hbar^2}{2m}\nabla^2 + 2 \hbar \Omega \cos ^2 \left( k_L x - \frac{\omega_r}{2} t \right)
```

where $`\Omega`$ is the effective Rabi frequency. 
$`\Omega`$ is determined by the laser properties and has typically a Gaussian temporal profile to ensure good velocity selectivity. 
If the atoms are freely falling, an acceleration term $`\frac{1}{2}a_\text{laser}t^2`$ is added to the phase inside the squared cosine such that the laser beams stay resonant to the falling atoms. 
Also common is an additional constant phase shift $`\Phi_0`$.

After the atom-light interaction, the atom is left in a superposition of states $`|g,0\rangle`$ and $`|g,2\hbar k_L\rangle`$, and typically higher orders like $`|g,-2\hbar k_L\rangle`$ and $`|g,4\hbar k_L\rangle`$ ([Siemß 2020](https://link.aps.org/doi/10.1103/PhysRevA.102.033709)). 
Idealized, this sequence applies a momentum transfer of $`2\hbar k_L`$ to the atom with a $`50\%`$ chance.


## Code
This example demonstrates the implementation of a Bragg beam splitter with the framework of unified_wf. 
It mainly covers the usage of the `FFTWave` class and the `split_step` function. 

The output is presented in a panel dashboard. Simply run the python program by writing `panel serve dashboard.py --port 5006` into the terminal (assuming the terminal path is set to [this](https://gitlab.projekt.uni-hannover.de/iqo-seckmeyer/unified_wf_2/-/tree/examples/examples/bragg_beam_splitter) directory). 
The dashboard can be found at http://localhost:5006/dashboard. 
Without a GPU the initial run of the dashboard may take about 20 seconds to a minute depending on your CPU.
If you want to make some changes to this program, add the flag `--autoreload` to the terminal command. 
By this, the dashboard will automatically reload, when you save changes.

Please make sure to have all the required packages installed (the installation guide can be found [here](https://gitlab.projekt.uni-hannover.de/iqo-seckmeyer/unified_wf_2)). 
