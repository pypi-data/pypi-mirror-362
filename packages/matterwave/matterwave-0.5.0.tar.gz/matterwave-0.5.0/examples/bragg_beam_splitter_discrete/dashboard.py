# math lib for computation on CPU/GPU/TPU
import numpy as np
import jax.numpy as jnp
# unified_wf
from fftarray import FFTArray, FFTDimension
from fftarray.fft_array import FreqArray
from fftarray.backends.jax_backend import JaxTensorLib, fft_array_scan
from matterwave import get_ground_state_ho, split_step, propagate
from dbg_tools import dbg, global_timer
# constants
from scipy.constants import pi, hbar
from matterwave.rb87 import m as mass_rb87, k_L, hbarkv
# writing and plotting to the panel dashboard
import panel as pn
import holoviews as hv

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Slider, Button

# dashboard header
pn.pane.Markdown("# Bragg Beam Splitter", width=500).servable()

# ------------------------------ default values ------------------------------ #
# angular frequency used to initialize the ground state (of quantum harmonic
# oscillator)
omega_x = 2*pi*10 # Hz
# laser pulse parameters
# Rabi frequency. This specific value was found as a binary search to
# optimize a 50/50 split of the two momentum classes for this specific beam
# splitter duration and pulse form.
rabi_frequency = 25144.285917282104 # Hz
phi_0 = 0. # phase jump
bragg_acc = 0. # bragg acceleration
sigma_bs = 25e-6 # temporal pulse width (s)
# define how many sigmas of the gauss to sample in each direction before
# reaching zero intensity:
sampling_range_mult = 4. # * sigma_bs
dt_bs = 1e-6 # time step size
# total number of pulse grid steps = gauss_width * scaling_factor / step_size
steps_limit = int(round(sigma_bs * sampling_range_mult / dt_bs))
t_offset = steps_limit*dt_bs
nt_bs = 2*steps_limit # number of time steps for beam splitter
dt_free = 5e-5 # defines time step size for free propagation
nt_free = 50 # number of time steps for free propagation
# time lists
t_list_bs = np.arange(nt_bs)*dt_bs
t_list_free = t_list_bs[-1]+np.arange(1,nt_free+1)*dt_free
t_list = np.concatenate((t_list_bs, t_list_free))

# laser start      intensity peak        laser end    ...   free propagation
#  --------------------------------------------------------------------------> t
#  |                    |                    |        ...
#  0                t_offset            2*t_offset

w_r = 2 * hbarkv * k_L # rb87 constant

# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 1: Initialization of global variables",
                 width=1000).servable()
pn.pane.Markdown(f"Mass = {mass_rb87} kg <br>\
    Rabi frequency = {rabi_frequency} Hz <br>\
    Phase jump: phi_0 = {phi_0} <br>\
    Laser temporal width: sigma_bs = {sigma_bs} s <br>\
    Time grid step = {dt_bs} s <br>", width=1000).servable()

# ------------------------ initialize the wavefunction ----------------------- #
global_timer("Wavefunction initialization.")

x_dim = FFTDimension("x",
    # pos_min = -50e-6,
    # pos_max = 50e-6,
    pos_middle=0.,
    d_freq=0.1*k_L,
    freq_middle = 0.,
    freq_extent = 32*k_L,
    loose_params = ["freq_extent"],
    default_tlib = JaxTensorLib(),
)

freqs = x_dim.fft_array(space="freq")
freqs_values = np.array(freqs)
zero_mask = freqs_values==0
freqs_values[zero_mask] = 1.
freqs_values[np.logical_not(zero_mask)] = 0.

dbg(str(freqs_values))
wf_init = FreqArray(values=jnp.array(freqs_values), dims=[x_dim], eager=False)


# wf_init = get_ground_state(
#     dim = x_dim,
#     omega = omega_x,
#     mass = mass_rb87
# )

# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 2: Initialize the wavefunction",
                 width=1000).servable()
pn.pane.Markdown(f"The wavefunction is initialized as the ground state of the \
    quantum harmonic oscillator with angular frequency `omega_x`. It is \
    displayed below:", width=1000).servable()
dbg(wf_init)
dbg(wf_init.fft_array(space="freq").values)

# --------------------------- Gauss helper function -------------------------- #
def gauss(t: float, sigma: float):
    """Return Gaussian function.

	Parameters
	----------
	t : float
		Time value.
	sigma : float
		Width.

	Returns
	-------
	float
		The Gaussian function at t with width sigma.
    """
    return jnp.exp(-0.5 * (t / sigma)**2)

# --------------------------------- potential -------------------------------- #
def V(x_dim: FFTDimension, ramp: float, t: float):
    """Kernel defining the Bragg beam splitter pulse. A kernel has to have the
 	arguments value and x,y,z (dependent on which dimention is initialized). Other
	arguments are optional.

	Parameters
	----------
	value : float
		The wavefunction. Not used here.
	x : float
		The x value.
	ramp : float
		The pulse ramp (scaling the rabi frequency).
	t : float
		The global time.

	Returns
	-------
	float
		The potential at x.
    """
    return rabi_frequency * ramp * 2. * hbar * np.cos(
        k_L * (x_dim.fft_array(space="pos") - 0.5 * bragg_acc * t**2)
        - 0.5 * w_r * t
        + phi_0/2.
    )**2

# shift the gauss function by gauss_offset s.t. it is zero at the grid border
gauss_offset = gauss(t = -t_offset, sigma = sigma_bs)

# ------------------------------ dashboard text ------------------------------ #
pn.pane.Markdown("## Step 2: Define the Bragg beam splitter potential",
                 width=1000).servable()
pn.pane.Markdown(f"The potential at the peak value (t = {t_offset} s) \
                 is displayed below:", width=1000).servable()

def plot_potential():
    """Plot the potential versus the wavefunction's x-grid.
    """
    v_values = V(x_dim = x_dim, ramp = 1., t = t_offset)
    plot = hv.Curve((x_dim.fft_array(space="pos"), v_values.fft_array(space="pos")))
    plot.opts(hv.opts.Curve(
        height=400,
        width=800,
        title="The potential versus the wavefunction's x-grid",
        xlabel="x",
        ylabel="V_kernel / hbar",
        tools=["hover", "xwheel_zoom"],
        line_width=1
    ))
    pn.Column(plot).servable()

plot_potential()

# -------------------------- evolve the wavefunction ------------------------- #
def step_bs(wf: FFTArray, t: float):
    """Step function for jax.lax.scan. Apply the Bragg beam splitter pulse.

	Parameters
	----------
	wf : FFTWave
		The wavefunction.
	wf : float
		The time.

	Returns
	-------
	FFTWave
		The final wavefunction
    """
    ramp = gauss(t = t-t_offset, sigma = sigma_bs) - gauss_offset
    wf = split_step(wf,
        mass = mass_rb87,
        dt = dt_bs,
        V = V(x_dim = x_dim, ramp = ramp, t = t),
        # V_fun = partial(V, x_dim = x_dim, ramp = ramp, t = t)
    )
    return wf, {
        "abs_pos": (np.abs(wf.fft_array(space="pos"))**2).values,
        "abs_freq": (np.abs(wf.fft_array(space="freq"))**2).values,
    }

def step_free(wf: FFTArray, t: float):
    """Step function for jax.lax.scan. Freely propagate the wavefunction.

	Parameters
	----------
	wf : FFTWave
		The wavefunction.
	wf : float
		The time.

	Returns
	-------
	FFTWave
		The final wavefunction
    """
    # The automatic input matching fails because this is essentially a no-op in the loop.
    # This loop actually does not need to be scan but could just be vmap because there is no data dependency.
    wf = propagate(wf, dt = dt_free, mass = mass_rb87).evaluate_lazy_state()
    return wf, {
        "abs_pos": (np.abs(wf.fft_array(space="pos"))**2).values,
        "abs_freq": (np.abs(wf.fft_array(space="freq"))**2).values,
    }

global_timer("Iteration.") # Start a timer for the iteration
# calls jax.lax.scan to start the iteration
# scan returns the final wavefunction and a dictionary containing lists of
# |\Psi(x)|^2 and |\Psi(kx)|^2 at different time steps
wf_final_bs, wf_data_bs = fft_array_scan(
    f = step_bs,
    init = wf_init,
    xs = t_list_bs
)

wf_final_free, wf_data_free = fft_array_scan(
    f = step_free,
    init = wf_final_bs,
    xs = t_list_free
)

# ------------------------------ dashboard text ------------------------------ #
pn.Column(pn.layout.Divider(margin=(10, 0, 0, 0)), width = 1400).servable()
pn.pane.Markdown("## Step 3: Evolve the wavefunction in time",
                 width=1000).servable()
pn.pane.Markdown(f"The wavefunction is evolved in time using the split-step \
                 method and the Bragg beam splitter potential. The intensity \
                 of the laser beam is Gaussian shaped (with width `sigma_bs`) \
                 in time. The main laser pulse is performed during the time \
                 interval [0, {2*t_offset*1e6}]µs. The rest of the time, the \
                 wavefunction is freely propagated. Note that the free \
                 propagation is computed and animated with a larger time step. \
                 The propagation of the wavefunction can appear faster than it \
                 is due to the constant animation frame rate.",
                 width=1000).servable()

# -------------------- animate the wavefunction evolution -------------------- #
# animation is iterating through t_list with steps animation_time_step_mult for
# the beam splitter part, otherwise 1
anim_time_step_mult = 5
pn.pane.Markdown(f"Only every {anim_time_step_mult}th time step of the beam \
                 splitter sequence is used for the animation.",
                 width=1000).servable()
def plot_wavefunction_evolution():
    """Plot and animate the evolution of the wavefunction in position and
    momentum space.
    """
    renderer = hv.renderer("bokeh")
    ### Initialization
    # x values
    x_list = np.array(x_dim.fft_array(space="pos"))
    # create time list for animation
    # (only take every anim_time_step_mult'th element of t_list_bs)
    plt_t_list = np.concatenate((
        t_list_bs[::anim_time_step_mult],
        t_list_free
    ))
    # initial values
    wf_init_abs_pos = (np.abs(wf_init.fft_array(space="pos"))**2).values
    wf_init_abs_freq = (np.abs(wf_init.fft_array(space="freq"))**2).values
    # list of all position space values
    plt_wf_final_pos = np.concatenate((
        # initial value
        [wf_init_abs_pos],
        # beam splitter values: take only every anim_time_step_mult'th value
        wf_data_bs["abs_pos"][anim_time_step_mult::anim_time_step_mult],
        # free propagation values
        wf_data_free["abs_pos"]
    ))
    # list of all momentum space values
    plt_wf_final_freq = np.concatenate((
        # initial value
        [wf_init_abs_freq],
        # beam splitter values: take only every anim_time_step_mult'th value
        wf_data_bs["abs_freq"][anim_time_step_mult::anim_time_step_mult],
        # free propagation values
        wf_data_free["abs_freq"]
    ))
    ### Create figures
    # create position space figure
    hmap_pos = hv.HoloMap(
        {i: hv.Curve((x_list, abs_pos))
            for i, abs_pos in enumerate(plt_wf_final_pos)}
    )
    hmap_pos.opts(hv.opts.Curve(
        height=400,
        width=600,
        title="Position space",
        xlabel="x",
        ylabel="$$|\Psi(x)|^2$$",
        tools=["hover"],
        line_width=1
    ))
    plot_pos = renderer.get_plot(hmap_pos)
    # create momentum space figure
    hmap_freq = hv.HoloMap(
        {i: hv.Curve((x_list, abs_freq))
            for i, abs_freq in enumerate(plt_wf_final_freq)}
    )
    hmap_freq.opts(hv.opts.Curve(
        height=400,
        width=600,
        title="Momentum space",
        xlabel="kx",
        ylabel="$$|\Psi(kx)|^2$$",
        tools=["hover"],
        line_width=1
    ))
    plot_freq = renderer.get_plot(hmap_freq)
    # create V_kernel ramp(t) figure
    ramp_list = [
        float(gauss(t = t-t_offset, sigma = sigma_bs) - gauss_offset)
        for t in plt_t_list]
    ramp_pt = lambda i: [ramp_list[i] if j==i else None
                            for j in range(len(plt_t_list))]
    ramp_plot = hv.Curve((plt_t_list, ramp_list))
    ramp_pt_plot = lambda i: hv.Points((plt_t_list, ramp_pt(i)))
    hmap_V = hv.HoloMap({i: ramp_plot*ramp_pt_plot(i)
                            for i in range(len(plt_t_list))})
    hmap_V.opts(
        height=200,
        width=600,
        title="V_kernel ramp",
        xlabel="t",
        ylabel="ramp"
    )
    hmap_V.opts(hv.opts.Curve(tools=["hover"]))
    hmap_V.opts(hv.opts.Points(color="red", size=5))
    plot_V = renderer.get_plot(hmap_V)

    # define time slider
    t_slider = Slider(
        title="Time in µs",
        value=0.,
        start=float(t_list[0])/1e-6,
        end=float(t_list[-1])/1e-6,
        step=dt_bs/1e-6,
        margin=(5, 5, 5, 20)
    )

    def time_changed(attr, old, new):
        """Called when the time slider was updated.
        """
        # get the wavefunction for the current time step (given by slider)
        j = (np.abs(plt_t_list - t_slider.value*1e-6)).argmin()
        # updates the plots
        plot_pos.update(j)
        plot_freq.update(j)
        plot_V.update(j)

    def update_time():
        """Iteratively called in every animation step.
        """
        time = t_slider.value*1e-6
        if time <= nt_bs*dt_bs:
            time += anim_time_step_mult*dt_bs
        else:
            time += dt_free
            if time > float(t_list[-1]):
                time = float(t_list[0])
        t_slider.value = time/1e-6 # calles time_changed

    # create button to start the animation
    t_anim_btn = Button(label='► Play', width=60, margin=(5, 10, 5, 5))
    callback_id = None
    def animate():
        """Animate the wavefunction in time. Play and pause the animation.
		"""
        nonlocal callback_id
        if t_anim_btn.label == '► Play':
            t_anim_btn.label = '❚❚ Pause'
            callback_id = curdoc().add_periodic_callback(update_time, 100)
        else:
            t_anim_btn.label = '► Play'
            curdoc().remove_periodic_callback(callback_id)

	# call time_changed() when the time slider's value changes
    t_slider.on_change("value", time_changed)
    # call animate() when the Play/Pause button is pressed
    t_anim_btn.on_click(animate)

    # create layout for all elements
    anim_layout = layout([
        [t_anim_btn, t_slider, plot_V.state],
        [plot_pos.state, plot_freq.state],
    ], sizing_mode='fixed')

    curdoc().add_root(anim_layout)
    pn.panel(anim_layout).servable()

global_timer("Plotting animation.")
plot_wavefunction_evolution()

# ------------------------------ dashboard text ------------------------------ #
pn.Column(pn.layout.Divider(margin=(10, 0, 0, 0)), width = 1400).servable()
pn.pane.Markdown("## The resulting wavefunction",
                 width=1000).servable()
pn.pane.Markdown("The wavefunction after performing the Bragg beam splitter is \
                 displayed below:",
                 width=1000).servable()
dbg(wf_final_bs)