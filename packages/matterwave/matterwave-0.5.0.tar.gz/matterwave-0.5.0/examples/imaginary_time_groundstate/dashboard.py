# math lib for computation on CPU/GPU/TPU
import numpy as np
# unified_wf
from fftarray import FFTArray, FFTDimension
from fftarray.backends.jax_backend import JaxTensorLib, fft_array_scan
from matterwave import split_step, get_ground_state_ho, get_e_kin, expectation_value
from dbg_tools import dbg, global_timer

# constants
from scipy.constants import pi, hbar, Boltzmann
from matterwave.rb87 import m as m_rb87
# writing and plotting to the panel dashboard
import panel as pn
import holoviews as hv

# ----------------------------- preliminary notes ---------------------------- #
# Consider the 1D quantum harmonic oscillator (QHO) with angular frequency
# omega_x. We want to find the ground state and its energy by using the
# imaginary time evolution. We start with an arbitrary state (e.g. the ground
# state of a QHO-potential with angular frequency omega_x_init) which we evolve
# by applying the split-step operator with imaginary time steps dt->-idt. After
# many iterations we get an approximation for the ground state.

# dashboard header
pn.pane.Markdown("# Imaginary Time Evolution", width=500).servable()

global_timer("Initialization.") # start timer for the initialization

# ----------------------- initialize gloabal variables ----------------------- #
# here: mass of rb87
mass = m_rb87 # kg
# the angular frequency of the QHO whose ground state and energy is to find:
omega_x = 2.*pi # Hz
# omega_x_init is used to generate the initial state that will be evolved to the
# desired ground state (the generated state is the ground state of the QHO with
# angular frequency omega_x_init):
omega_x_init = 2.*pi*0.1 # Hz
# time step for split-step:
dt = 1e-4 # s
# choose dimension x [m]


# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 1: Initialization of global variables",
                 width=1000).servable()
pn.pane.Markdown("The mass: `mass` = {} kg. <br>The angular frequency of the \
    system we're interested in: `omega_x` = {} Hz. <br>The angular frequency \
    used for the initial state: `omega_x_init` = {} Hz. <br>The time step for \
    the split-step operator: dt = {} s. \
    ".format(mass, omega_x, omega_x_init, dt), width=1000).servable()


# ------------------------ initialize the wavefunction ----------------------- #
# insert the constraints for the x dimension, all other free variables will be
# set accordingly
x_dim = FFTDimension("x",
    pos_min = -200e-6,
    pos_max = 200e-6,
    freq_middle = 0.,
    n = 2048,
    default_tlib=JaxTensorLib(),
)
# initialize the wavefunction as the ground state of the QHO with omega_x_init
wf_init = get_ground_state_ho(x_dim, omega=omega_x_init, mass=mass)


# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 2: Initialize the wavefunction",
                 width=1000).servable()
pn.pane.Markdown("The resolution of the wavefunction's discrete position and \
    frequency space is determined by the arguments of the `FFTWave` class.<br> \
    The wavefunction itself is initialized with zeros. \
    ".format(wf_init), width=1000).servable()
pn.pane.Markdown("Here, the wavefunction is set to the ground state of the QHO \
    with frequency `omega_x_init`. <br>It is displayed below: \
    ".format(wf_init), width=1000).servable()

# plot the wavefunction with dbg
dbg(wf_init)



# The energy at the given point x
# Defining the quantum harmonic oscillator potential.
V = 0.5 * mass * omega_x**2. * x_dim.fft_array(space="pos")**2.
# ------------------- perform the imaginary time evolution ------------------- #
def step(wf: FFTArray, *_):
    """
    The step function for the iteration using jax.lax.scan.

    Args:
        wf (FFTWave): The wavefunction which sould be evolved.

    Returns:
        Tuple[FFTWave, dict]: Returns the wavefunction for the next iteration
        step and a dictionary containing the energy values.
    """
    # save the energy in µK to avoid small values (~1e-33 for Joule)
    # calculate the kinetic energy (result is returned in µK)
    E_kin = get_e_kin(wf, m=mass, return_microK=True)
    # calculate the potential energy (and convert to µK)
    E_pot = expectation_value(wf, V) / (Boltzmann * 1e-6)
    # calculate the total energy
    E_tot = E_kin + E_pot
    # split-step application (set is_complex=True to use imaginary time step)
    wf = split_step(wf=wf, dt=dt, mass=mass, V=V, is_complex=True)
    # split_step() normalizes the wavefunction if: is_complex=True
    # return the wavefunction for the next iteration step and the energies in a
    # dictionary for plotting (every iteration the energies are appended to a
    # list)
    return wf, {"E_kin": E_kin, "E_pot": E_pot, "E_tot": E_tot}

# stops the previous timer ("Iteration") and starts to time "Iteration"
global_timer("Iteration.")

# 10654 iteration steps are performed (this was found to be enough such that the
# total energy converges)
N_iter = 10654
# calls jax.lax.scan to start the iteration
# scan returns the final wavefunction and a dictionary containing the energies
# {"E_kin": [...], "E_pot": [...], "E_tot": [...]}
wf_final, energies = fft_array_scan(f=step, init=wf_init, xs=None, length=N_iter)

# the analytical solution of the ground state energy
E_tot_analy = 0.5*omega_x*hbar/(Boltzmann * 1e-6) #microK

# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 3: Performing the imaginary time evolution",
                 width=1000).servable()
pn.pane.Markdown("{} iteration steps have been performed. Each iteration the \
    wavefunction is evolved by the split-step operator with imaginary time. \
    <br>In addition, the wavefunction's kinetic and potential energy are \
    calculated. \
    ".format(N_iter), width=1000).servable()
pn.pane.Markdown("The resulting wavefunction is shown below:",
                 width=1000).servable()

# display the ground state wavefunction (output of the iteration)
dbg(wf_final)

# -------------------------------- plot energy ------------------------------- #
# plot the energy trend during the imaginary time evolution
global_timer("Plotting.")
pn.extension()
E_kin_plt = hv.Curve(energies["E_kin"], label="Kinetic Energy")
E_pot_plt = hv.Curve(energies["E_pot"], label="Potential Energy")
E_tot_plt = hv.Curve(energies["E_tot"], label="Total Energy")
# make E_tot_analy same shape as E_tot
E_tot_analy_list = np.full_like(energies["E_tot"], E_tot_analy)
E_tot_analy_plt= hv.Curve(E_tot_analy_list,
                          label="Ground state energy (analytical solution)")
# combining the three curves into one plot:
overlay = E_kin_plt*E_pot_plt*E_tot_plt*E_tot_analy_plt
# styling
overlay.opts(height=500,
             width=800,
             legend_position="top_right",
             title="Energy values during imaginary time evolution",
             xlabel="Iteration step",
             ylabel="µK")
overlay.opts(hv.opts.Curve(tools=["hover"]))
# dashbboard text
pn.pane.Markdown("The energy values during the imaginary time evolution are \
    presented below. <br>Additionally, the analytically computed ground state \
    energy is shown for reference. \
    ", width=1000).servable()
# show the plot
pn.Column(overlay).servable()

global_timer("-"*10)