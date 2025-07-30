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

import pandas as pd
import hvplot.pandas
import cloudpickle

from functools import partial

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
    phi_0 = 0. # phase jump
    bragg_acc = 0. # bragg acceleration
    sigma_bs = 25e-6 # temporal pulse width (s)
    # define how many sigmas of the gauss to sample in each direction before
    # reaching zero intensity:
    sampling_range_mult = 4. # * sigma_bs
    dt_bs = 1e-7 # time step size
    # total number of pulse grid steps = gauss_width * scaling_factor / step_size
    tau = 30e-6
    steps_limit_cebs = int(round(tau / dt_bs))
    steps_limit_gauss = int(round(sigma_bs * sampling_range_mult / dt_bs))

    t_offset_gauss = steps_limit_gauss*dt_bs
    t_offset_cebs = steps_limit_cebs*dt_bs
    nt_bs_gauss = 2*steps_limit_gauss # number of time steps for beam splitter
    nt_bs_cebs = steps_limit_cebs+1 # number of time steps for beam splitter
    nt_free = 4 # number of time steps for free propagation
    dt_free = t_free/nt_free # defines time step size for free propagation

    # time lists
    t_list_bs_gauss = np.arange(nt_bs_gauss)*dt_bs
    t_list_bs_cebs = np.arange(nt_bs_cebs)*dt_bs
    # dbg(pd.DataFrame({"t": t_list_bs, "ramp": jnp.max(jnp.array([t_list_bs*0., jnp.tanh(8*t_list_bs/tau)*jnp.tanh(8*(1-t_list_bs/tau))]), axis=0)}).hvplot.scatter(x="t", y="ramp"))

    # t_list_free = t_list_bs[-1]+np.arange(1,nt_free+1)*dt_free
    # t_list_bs2 = t_list_bs+t_list_free[-1]+t_list_bs[-1]
    # t_list = np.concatenate((t_list_bs, t_list_free, t_list_bs2))

    # laser start      intensity peak        laser end    ...   free propagation
    #  --------------------------------------------------------------------------> t
    #  |                    |                    |        ...
    #  0                t_offset            2*t_offset

    # w_r = 2 * hbarkv * k_L # rb87 constant
    # dbg(w_r)
    w_r = hbar * k_L**2/(2*m)
    dbg(m)
    dbg(hbar)
    dbg(w_r)

    # ------------------------ initialize the wavefunction ----------------------- #
    global_timer("Wavefunction initialization.")

    x_dim = FFTDimension("x",
        pos_min = -100e-6,
        pos_max = 400e-6,
        freq_middle = 0.,
        freq_extent = 90*k_L/(2*np.pi),
        loose_params = ["freq_extent"],
        default_tlib = JaxTensorLib(),
    )

    wf_init = get_ground_state_ho(
        dim = x_dim,
        sigma_p = 0.005 * hbark,
        mass = mass_rb87
    )

    # dbg(wf_init)

    # --------------------------- Gauss helper function -------------------------- #
    def gauss(t: float, sigma: float):
        return jnp.exp(-0.5 * (t / sigma)**2)


    # --------------------------------- potential -------------------------------- #
    def V(x_dim: FFTDimension, ramp: float, t: float, n: int, rabi_frequency):
        # dbg(n)
        return rabi_frequency * ramp * 2 * hbar * np.cos(
        # return rabi_frequency * ramp * 2. * hbar * np.cos(
            k_L * (x_dim.fft_array(space="pos") - 0.5 * bragg_acc * t**2)
            - n * w_r * t
            + phi_0/2.
        )**2


    # -------------------------- evolve the wavefunction ------------------------- #
    def step_bs_cebs(wf: FFTArray, t: float, n: int, rabi_frequency: float):
        # ramp = gauss(t = t-t_offset, sigma = sigma_bs) - gauss_offset
        ramp = jnp.max(jnp.array([0, jnp.tanh(8*t/tau)*jnp.tanh(8*(1-t/tau))]))
        wf = split_step(wf,
            mass = mass_rb87,
            dt = dt_bs,
            V = V(x_dim = x_dim, ramp = ramp, t = t, n = n, rabi_frequency=rabi_frequency),
            # V_fun = partial(V, x_dim = x_dim, ramp = ramp, t = t)
        )
        return wf, {
            "ramp": ramp
        }

    gauss_offset = gauss(t = -t_offset_gauss, sigma = sigma_bs)
    def step_bs_gauss(wf: FFTArray, t: float, n: int, rabi_frequency):
        ramp = gauss(t = t-t_offset_gauss, sigma = sigma_bs) - gauss_offset
        wf = split_step(wf,
            mass = mass_rb87,
            dt = dt_bs,
            V = V(x_dim = x_dim, ramp = ramp, t = t, n=n, rabi_frequency=rabi_frequency),
            # V_fun = partial(V, x_dim = x_dim, ramp = ramp, t = t)
        )
        return wf, {
            "ramp": ramp
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

    def add_seq(final, step, t_list_bs):
        finished_steps.append(final)
        dbg(final)
        dbg(pd.DataFrame({"t": t_list_bs, "ramp": step["ramp"]}).hvplot.scatter(x="t", y="ramp"))
        return final

    wf = wf_init

    df = pd.DataFrame(columns=["pop", "rel_mom", "N"])
    for N in range(1,10):
        # dbg(N)
        # wf = add_seq(*fft_array_scan(
        #     f = partial(step_bs_gauss, n=4*N-2, rabi_frequency=2.*25144.285917282104),
        #     init = wf,
        #     xs = t_list_bs_gauss
        # ), t_list_bs_gauss)
        wf = add_seq(*fft_array_scan(
            f = partial(step_bs_cebs, n=4*N-2, rabi_frequency = 7.96*w_r),
            init = wf,
            xs = t_list_bs_cebs
        ), t_list_bs_cebs)
        for mom in 2*(np.arange(-5,5)+N):
            mask = lambda min, max: FreqArray(jnp.logical_and(x_dim.fft_array(space="freq").values > min*k_L/(2*np.pi), x_dim.fft_array(space="freq").values < max*k_L/(2*np.pi)), dims=[x_dim], eager=False)
            masked = wf.fft_array(space="freq") * mask(mom-1,mom+1)
            pop = norm(masked)
            df = df.append({"pop": pop, "rel_mom": mom-2*N, "N": 2*N}, ignore_index=True)
            # dbg(mom)
            # dbg(pop)

    dbg(df.hvplot.scatter(x="N", y="pop", by="rel_mom"))
        # wf = add_seq(*fft_array_scan(
        #     f = partial(step_bs, n=2),
        #     init = wf,
        #     xs = t_list_bs
        # ), 5)
    # wf = add_seq(*fft_array_scan(
    #     f = step_mirror,
    #     init = wf,
    #     xs = t_list_bs
    # ), 5)

    # wf = add_seq(*fft_array_scan(
    #     f = step_free,
    #     init = wf,
    #     xs = t_list_free
    # ))
    # wf = add_seq(*fft_array_scan(
    #     f = step_bs,
    #     init = wf,
    #     xs = t_list_bs
    # ), 5)
    # wf = add_seq(*fft_array_scan(
    #     f = step_free,
    #     init = wf,
    #     xs = t_list_free
    # ))


    wf_freq: FreqArray = wf.fft_array(space="freq")
    mask = lambda min, max: FreqArray(jnp.logical_and(x_dim.fft_array(space="freq").values > min*k_L/(2*np.pi), x_dim.fft_array(space="freq").values < max*k_L/(2*np.pi)), dims=[x_dim], eager=False)
    wf_freq_0hbark = wf_freq * mask(-1,1)
    # dbg(wf_freq_0hbark)
    wf_freq_2hbark = wf_freq * mask(1,3)
    # dbg(wf_freq_2hbark)
    # dbg(norm(wf_freq_0hbark))
    # dbg(norm(wf_freq_2hbark))
    return norm(wf_freq_0hbark), norm(wf_freq_2hbark)


file_name = "output3.cpkl"

run(0)
# run(1e-4)
# run(1.2e-3)
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
# with open(file_name, "rb") as f:
#     df = cloudpickle.load(f)



# dbg(df.hvplot.scatter(x="T_free", y="pop", by="port"))
# print(df)

