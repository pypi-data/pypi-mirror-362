# math lib for computation on CPU/GPU/TPU
import numpy as np
import jax.numpy as jnp
# unified_wf
from fftarray import FFTArray, FFTDimension, FreqArray
from fftarray.backends.jax_backend import JaxTensorLib, fft_array_scan
from matterwave import get_ground_state_ho, split_step, propagate, norm, normalize
from dbg_tools import dbg, global_timer
# constants
from scipy.constants import pi, hbar
from matterwave.rb87 import m as mass_rb87, k_L, hbarkv, hbark, m
# writing and plotting to the panel dashboard
import panel as pn
import holoviews as hv

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Slider, Button

# dashboard header
pn.pane.Markdown("# Bragg Beam Splitter", width=500).servable()

def run(t_free = 1e-5):
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
    nt_free = 4 # number of time steps for free propagation
    dt_free = t_free/nt_free # defines time step size for free propagation

    # time lists
    t_list_bs = np.arange(nt_bs)*dt_bs
    t_list_free = t_list_bs[-1]+np.arange(1,nt_free+1)*dt_free
    t_list_bs2 = t_list_bs+t_list_free[-1]+t_list_bs[-1]
    t_list = np.concatenate((t_list_bs, t_list_free, t_list_bs2))

    # laser start      intensity peak        laser end    ...   free propagation
    #  --------------------------------------------------------------------------> t
    #  |                    |                    |        ...
    #  0                t_offset            2*t_offset

    w_r = 2 * hbarkv * k_L # rb87 constant
    w_r = 2 * hbar * k_L**2/(2*m)
    dbg(m)
    dbg(hbar)
    dbg(w_r)

    # ------------------------ initialize the wavefunction ----------------------- #
    global_timer("Wavefunction initialization.")

    x_dim = FFTDimension("x",
        pos_min = -100e-6,
        pos_max = 100e-6,
        freq_middle = 0.,
        freq_extent = 32*k_L/(2*np.pi),
        loose_params = ["freq_extent"],
        default_tlib = JaxTensorLib(),
    )

    wf_init = get_ground_state_ho(
        dim = x_dim,
        sigma_p = 0.003 * hbark,
        mass = mass_rb87
    )

    # dbg(wf_init)

    # --------------------------- Gauss helper function -------------------------- #
    def gauss(t: float, sigma: float):

        return jnp.exp(-0.5 * (t / sigma)**2)

    # --------------------------------- potential -------------------------------- #
    def V(x_dim: FFTDimension, ramp: float, t: float):
        return rabi_frequency * ramp * 2. * hbar * np.cos(
            k_L * (x_dim.fft_array(space="pos") - 0.5 * bragg_acc * t**2)
            - 0.5 * w_r * t
            + phi_0/2.
        )**2

    # shift the gauss function by gauss_offset s.t. it is zero at the grid border
    gauss_offset = gauss(t = -t_offset, sigma = sigma_bs)


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

    # plot_potential()

    # -------------------------- evolve the wavefunction ------------------------- #
    def step_bs(wf: FFTArray, t: float):
        ramp = gauss(t = t-t_offset, sigma = sigma_bs) - gauss_offset
        wf = split_step(wf,
            mass = mass_rb87,
            dt = dt_bs,
            V = V(x_dim = x_dim, ramp = ramp, t = t),
            # V_fun = partial(V, x_dim = x_dim, ramp = ramp, t = t)
        )
        return wf, None
        return wf, {
            "abs_pos": (np.abs(wf.fft_array(space="pos"))**2).values,
            "abs_freq": (np.abs(wf.fft_array(space="freq"))**2).values,
        }

    def step_free(wf: FFTArray, t: float):
        wf = propagate(wf, dt = dt_free, mass = mass_rb87).evaluate_lazy_state()
        return wf, None
        return wf, {
            "abs_pos": (np.abs(wf.fft_array(space="pos"))**2).values,
            "abs_freq": (np.abs(wf.fft_array(space="freq"))**2).values,
        }

    global_timer("Iteration.") # Start a timer for the iteration
    finished_steps = []
    step_data = []

    def add_seq(final, step, anim_time_step_mult=1):
        finished_steps.append(final)
        # step_data.append({name: arr[anim_time_step_mult::anim_time_step_mult] for name, arr in step.items()})
        return final

    wf = wf_init

    wf = add_seq(*fft_array_scan(
        f = step_bs,
        init = wf,
        xs = t_list_bs
    ), 5)

    wf = add_seq(*fft_array_scan(
        f = step_free,
        init = wf,
        xs = t_list_free
    ))
    wf = add_seq(*fft_array_scan(
        f = step_bs,
        init = wf,
        xs = t_list_bs
    ), 5)
    # wf = add_seq(*fft_array_scan(
    #     f = step_free,
    #     init = wf,
    #     xs = t_list_free
    # ))


    # -------------------- animate the wavefunction evolution -------------------- #
    # animation is iterating through t_list with steps animation_time_step_mult for
    # the beam splitter part, otherwise 1
    anim_time_step_mult = 5
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
            t_list_free,
            t_list_bs2[::anim_time_step_mult],
        ))
        # initial values
        wf_init_abs_pos = (np.abs(wf_init.fft_array(space="pos"))**2).values
        wf_init_abs_freq = (np.abs(wf_init.fft_array(space="freq"))**2).values
        # list of all position space values
        plt_wf_final_pos = np.concatenate((
            # initial value
            [wf_init_abs_pos],
            *[arrs["abs_pos"] for arrs in step_data],
        ))
        # list of all momentum space values
        plt_wf_final_freq = np.concatenate((
            # initial value
            [wf_init_abs_freq],
            *[arrs["abs_freq"] for arrs in step_data],
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
    # plot_wavefunction_evolution()

    # dbg(wf)
    wf_freq: FreqArray = wf.fft_array(space="freq")
    mask = lambda min, max: FreqArray(jnp.logical_and(x_dim.fft_array(space="freq").values > min*k_L/(2*np.pi), x_dim.fft_array(space="freq").values < max*k_L/(2*np.pi)), dims=[x_dim], eager=False)
    wf_freq_0hbark = wf_freq * mask(-1,1)
    # dbg(wf_freq_0hbark)
    wf_freq_2hbark = wf_freq * mask(1,3)
    # dbg(wf_freq_2hbark)
    # dbg(norm(wf_freq_0hbark))
    # dbg(norm(wf_freq_2hbark))
    return norm(wf_freq_0hbark), norm(wf_freq_2hbark)

import pandas as pd
import hvplot.pandas
import cloudpickle
file_name = "output3.cpkl"

run(0)
run(1e-4)
run(1.2e-3)
def compute():
    df = pd.DataFrame(columns=["pop", "port", "T_free"])
    # for T_free in np.arange(500)*4e-6:
    # for T_free in np.linspace(0.,1.3e-3, 1500):
    for T_free in np.linspace(0.,1e-4, 30):
        p_0hbark, p_2hbark = run(T_free)
        df = df.append({"pop": p_0hbark, "port": "0hbark", "T_free": T_free}, ignore_index=True)
        df = df.append({"pop": p_2hbark, "port": "2hbark", "T_free": T_free}, ignore_index=True)

    with open(file_name, "wb") as f:
        cloudpickle.dump(df, f)

# compute()
with open(file_name, "rb") as f:
    df = cloudpickle.load(f)



dbg(df.hvplot.scatter(x="T_free", y="pop", by="port"))
print(df)

