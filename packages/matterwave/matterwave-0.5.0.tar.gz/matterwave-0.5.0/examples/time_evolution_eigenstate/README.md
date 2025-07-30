# Time evolution via split-step method
## TL;DR
```python
from fftarray import FFTWave, FFTDimension
from matterwave import split_step
import jax
import jax.numpy as jnp

from scipy.constants import hbar, pi
from matterwave.rb87 import m as m_rb87

omega_x = 2.*pi*100./3.
mass = m_rb87
dt = 1e-5
time_steps = 1000

def harmonic_potential_1d(x: float, value: complex):
    return 0.5 * mass * omega_x**2. * x**2.

def first_excited_state(x: float, value: complex):
    return 1./jnp.sqrt(2.)*(mass*omega_x/(pi*hbar))**(1./4.) * \
            jnp.exp(-mass*omega_x*x**2./(2.*hbar)+0.j) * \
                2*jnp.sqrt(mass*omega_x/hbar)*x

def split_step_scan_iteration(wf, *_):
    wf = split_step(wf, mass=mass, dt=dt, V_kernel=harmonic_potential_1d)
    return wf, {'wf_x1_psi': wf.psi_pos[x1], 'wf_x2_psi': wf.psi_pos[x2]}

x = FFTDimension(pos_min=-50e-6, pos_max=50e-6, freq_middle=0, n=2048)
wf_init = FFTWave(x = x)
wf_first_excited = wf_init.map_pos_space(first_excited_state)

wf_initial_pos = wf_first_excited.psi_pos[:]
x1 = jnp.argmin(jnp.real(wf_initial_pos)) # Minimum
x2 = jnp.argmax(jnp.real(wf_initial_pos)) # Maximum

time_array = np.arange(time_steps * dt, step=dt)
wf_after_time_evolution, carry = jax.lax.scan(
    f=split_step_scan_iteration,
    init=wf_first_excited,
    xs=time_array[1:]
)
```
## Physics
### Quantum harmonic oscillator
This example aims to perform a time evolution of a 1d wavefunction in the first excited state of the 1d quantum harmonic oscillator. The physics is described by the following Hamiltonian:
```math
\hat{H} = \hat T + \hat V = \frac{\hat p ^2}{2m} + \frac{1}{2} m \omega_x^2 \hat x ^2
```
with the momentum operator $`\hat p`$, and the position operator $`\hat x`$. Additionally, we choose the mass $`m`$ of Rb-87 and the angular frequency $`\omega_x=2\pi * \frac{100}{3}`$. The first excited state of the quantum harmonic oscillator is given as the following 1d wavefunction:
```math
\Psi(x) = \sqrt{2}\times \left(\frac{m\omega_x}{\pi\hbar}\right)^{1/4}e^{-\frac{m\omega_x x^2}{2\hbar}} \sqrt{\frac{m\omega_x}{\hbar}}x.
```
For more details visit the Wikipedia [page](https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator) on the physics of the quantum harmonic oscillator.
### Split-step method
In quantum mechanics, we perform a time evolution via the time evolution operator $`\hat U(dt) = e^{-i\hat H\cdot dt/\hbar}`$. We can propagate an initial wavefunction in small time steps $`dt`$ according to:
```math
\Psi (x,t+dt) = e^{-i\hat H\cdot dt/\hbar} \Psi (x, t) = e^{-i(\hat T + \hat V )\cdot dt/\hbar} \Psi (x, t)
```
where we split the Hamiltonian into the kinetic energy operator $`\hat T`$ and the potential energy operator $`\hat V`$. To save computational resources, we would like to use the fact that $`\hat T`$ is diagonal in momentum (frequency) space and $`\hat V`$ is diagonal in position space. Therefore we split the upper equation into seperate exponentials:
```math
\Psi (x,t+dt) = e^{-i\hat T\cdot dt/(2\hbar)} e^{-i\hat V\cdot dt/\hbar} e^{-i\hat T\cdot dt/(2\hbar)} \Psi (x, t) + \mathcal{O}(dt^3)
```
and apply the first and third exponential in frequency space and the second exponential in position space. We transform the wavefunction $`\Psi`$ between the spaces via a FFT (and an inverse FFT). For more details and the exact placement of the FFTs, have a look at this [article](https://www.algorithm-archive.org/contents/split-operator_method/split-operator_method.html)

## Code

The implemented class `FFTWave` together with the implemented `split_step` method perform the required math to apply the split-step method with the harmonic potential $`\hat V`$ as the input argument `V_kernel`. The script [dashboard.py](dashboard.py) implements the time evolution of the first excited state for 1000 time steps with $`dt= 10^{-5}`$. The script can be started via `panel serve dashboard.py --port 5006` which outputs the results and further comments in a browser dashboard at http://localhost:5006/dashboard. If you would like to play around and edit the script, consider adding the flag `--autoreload` when starting the script for automatic reloading on a saved edit of the script.

Please make sure to have all the required packages installed (the installation guide can be found [here](https://gitlab.projekt.uni-hannover.de/iqo-seckmeyer/unified_wf_2)).
