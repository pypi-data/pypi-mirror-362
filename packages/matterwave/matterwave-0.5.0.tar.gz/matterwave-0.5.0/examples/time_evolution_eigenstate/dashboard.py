from fftarray import FFTDimension
from fftarray.backends.jax_backend import JaxTensorLib, fft_array_scan
from matterwave import split_step
import jax
from jax.config import config
config.update("jax_enable_x64", True)

# Math packages
import numpy as np

# Constants
from scipy.constants import hbar, pi
from matterwave.rb87 import m as m_rb87

# Visualization
from dbg_tools import dbg
from dbg_tools.vis_backends.panel import panel_rendering
import holoviews as hv
import panel as pn
pn.extension()

### Variable settings for our numerical time evolution of the initial wavefunction ###

# Frequency of harmonic potential
omega_x = 2.*pi*100./3.
# Mass of (matter) wavefunction
mass = m_rb87
# Numerical settings for time evolution
dt = 1e-5
time_steps = 1000

### ------------------------------------------------------------------------------ ###

def markdown(docstring):
    pn.pane.Markdown(docstring, width=800).servable()

markdown("""
    # Time evolution via split-step method
    ## An example using the first excited state of the harmonic oscillator
    """)


markdown("""
    ### Step 1: Initialization of an FFTWave object
    The FFTWave object will later hold the numerical representation of the wavefunction.

    It features the required split-step method for the time evolution including the FFTs between position and frequency space.

    The following graphic shows the default FFTWave object initialized with fixed pos_min=-50e-6m, pos_max=50e-6m, freq_middle=0, n=2048:
""")

# Initialization of an FFTWave object in 1d fitting our 1d wavefunction.
# The given arguments should yield a unique solution for the
# required parameters to efficiently compute the FFT of our wave function.
x_dim = FFTDimension("x",
    pos_min = -50e-6,
    pos_max = 50e-6,
    freq_middle = 0.,
    n = 2048,
    default_tlib=JaxTensorLib(),
    default_force_precision="fp64"
)


markdown("""
    ### Step 2: Definition of the 1d harmonic potential and the first excited state

    The **mass** of the (matter) wavefunction needs to be defined, in this case the mass of Rubidium-87 is used.

    The **angular frequency** of the harmonic potential needs to be defined, in this case omega = 2pi*100./3.

    Using these parameters, the wavefunction is defined as the first excited state of the harmonic oscillator. See on [Wikipedia](https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator) for more details.

    The wavefunction can be transferred to the FFTWave object in position space. The resulting FFTWave object shows wavefunction in position and frequency space:
""")

"""
The function serves as the kernel defining our 1d potential in terms of the grid positions.
Here, it is the harmonic potential w.r.t. the given mass "mass" and frequency "omega_x".
More information on the physics can be found here: https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator.

Args:
    x (float): x position where to calculate the 1d harmonic potential.
    value (complex): Not relevant for the harmonic potential. Only placed as a kwarg for compatibility.

Returns:
    complex: Potential energy value at the given x-position. y- and z-position have no influence.
"""

harmonic_potential_1d = (0.5 * mass * omega_x**2.) * x_dim.fft_array(space="pos")**2.

# Insert the wavefunction (defined in position space) into our FFTWave object
# via mapping the values of our above defined kernel to
# the respective grid values in position space
# The inserted wavefunction needs to be a callable object with complex output.
wf_first_excited = 1./np.sqrt(2.)*(mass*omega_x/(pi*hbar))**(1./4.) * \
             np.exp(-mass*omega_x * x_dim.fft_array(space="pos")**2./(2.*hbar)+0.j) * \
                 2*np.sqrt(mass*omega_x/hbar)*x_dim.fft_array(space="pos")
# dbg(mass)
# wf_first_excited = -mass* dbg(x_dim.pos**2.)

dbg(wf_first_excited) # Shows FFTWave object representing first excited state of the harmonic oscillator

markdown("""
    ### Step 3a: Time evolution of the first excited state

    The time evolution of the wavefunction is being performed via the split-step method.
    For a short explanation have a look at the README.md and for a more thorough explanation read [this](https://www.algorithm-archive.org/contents/split-operator_method/split-operator_method.html).

    The split-step method is implemented such that it takes an FFTWave object and propagates the wavefunction for a given time step dt and potential V, in this case a harmonic potential.

    The following is the FFTWave object after 1000 steps with dt=1e-5. As expected for an eigenstate, the probability densities stay the same:
""")

# Calculate grid positions of min and max of the initial wavefunction's real part.
# These correspond to the two maxima of the probability density.
wf_initial_pos = wf_first_excited.fft_array(space="pos")
x1 = np.argmin(np.real(wf_initial_pos)) # Minimum
x2 = np.argmax(np.real(wf_initial_pos)) # Maximum

# Function to calculate the phase from the complex wavefunction evaluated at some position.
def phase_from_value(value):
    return np.arccos(np.real(value/np.abs(value)))

# Initialize lists to store the wavefunction instances for both points x1, x2
# for each time step with the first entry for the initial wave function.
wf_x1_list = [np.array(wf_first_excited.fft_array(space="pos"))[x1]]
wf_x2_list = [np.array(wf_first_excited.fft_array(space="pos"))[x2]]

def split_step_scan_iteration(wf, *_):
    wf = split_step(wf, mass=mass, dt=dt, V=harmonic_potential_1d)
    return wf, {'wf_x1_values': wf.fft_array(space="pos").values[x1], 'wf_x2_values': wf.fft_array(space="pos").values[x2]}

### The following is the logic that jax.lax.scan mimics under the hood ###

# 1. carry = {'wf_x1_values': [], 'wf_x2_values': []}
# 2. wf = wf_first_excited
# 3. for t in xs:
#      ### Perform a single split step of the wavefunction wf w.r.t to
#      ### the 1d harmonic potential from above given as V_kernel
#      ### and overwrite the old FFTWave object with the propagated FFTWave object
# 4.   wf = split_step(wf, mass=mass, dt=dt, V_kernel = harmonic_potential_1d, kernel_kwargs = {})
#      ### Calculate and store the wavefunction instances at positions x1,x2
# 5.   storage['wf_x1_values'].append(wf.values_pos[x1])
# 6.   storage['wf_x2_values'].append(wf.values_pos[x2])
# 7. wf_after_time_evolution = wf

### ------------------------------------------------------------------------- ###

time_array = np.arange(time_steps) * dt
# TODO Why not freq_fft necessary?
wf_after_time_evolution, carry = fft_array_scan(f=split_step_scan_iteration, init=wf_first_excited, xs=time_array[1:])

dbg(wf_after_time_evolution) # FFTWave object representing the time evolution of the first excited state

markdown("""
    ### Step 3b: Phases during time evolution of the first excited state

    During the time evolution the phase of the wavefunction on a fixed point can be monitored.
    Here, we choose to monitor the phase of the two respective maxima of the wavefunction's probabilty density.

    The changing phase is shown over the period of 1000 steps, i.e., 0.01s in total. They change from 0 to pi and vice versa:
""")

wf_x1_list += list(carry['wf_x1_values'])
wf_x2_list += list(carry['wf_x2_values'])

# Calculate the phases for all instances of the wavefunction
wf_x1_list = list(map(phase_from_value,wf_x1_list))
wf_x2_list = list(map(phase_from_value,wf_x2_list))

# Preparation of a holoviews plot and pushing it to the Panel dashboard
def panel_plotting(time_array, wf_x1_list, wf_x2_list):
    plot_x1 = hv.Curve((time_array, wf_x1_list), label='Maximum 1').opts(tools=['hover'])
    plot_x2 = hv.Curve((time_array, wf_x2_list), label='Maximum 2').opts(tools=['hover'])
    title = 'Time evolution'
    plot = (plot_x1 * plot_x2)
    plot.opts(fontscale=1.5, width=800, height=500,
              title=title, xlabel='Time', ylabel='Phase',
              legend_position='right', legend_offset=(0,150))
    pn.Column(plot).servable()

    # pip install selenium is required for the following
    # hv.save(plot, 'time_evolution_{}_steps_omega={:.2f}pi.png'.format(time_steps, omega_x/(pi)), fmt='png')

panel_plotting(time_array, wf_x1_list, wf_x2_list)