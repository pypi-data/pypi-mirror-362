
import panel as pn
pn.extension()
from bokeh.io import output_notebook
output_notebook()

from scipy.constants import pi
from matterwave.rb87 import k_L, hbarkv

from dbg_tools import dbg
# angular frequency used to initialize the ground state (of quantum harmonic
# oscillator)
omega_x = 2*pi*10 # Hz

rabi_frequency = 25144.285917282104 # Hz
phi_0 = 0. # phase jump
bragg_acc = 0. # bragg acceleration
sigma_bs = 25e-6 # temporal pulse width (s)
w_r = 2 * hbarkv * k_L # rb87 constant


import numpy as np
# define how many sigmas of the gauss to sample in each direction before
# reaching zero intensity:
sampling_range_mult = 4. # * sigma_bs
dt_bs = 1e-6 # time step size
# total number of pulse grid steps = gauss_width * scaling_factor / step_size
steps_limit = int(round(sigma_bs * sampling_range_mult / dt_bs))
t_offset = steps_limit*dt_bs
nt_bs = 2*steps_limit # number of time steps for beam splitter

from fftarray import FFTDimension, FFTArray
from fftarray.backends.jax_backend import JaxTensorLib
from fftarray.fft_constraint_solver import fft_dim_from_constraints
from fftarray.tools import *

from matterwave.rb87 import m as mass_rb87
from matterwave import get_ground_state_ho
from matterwave.helpers import generate_panel_plot
from scipy.constants import hbar


from functools import reduce
from typing import Callable, Union, Any

# coordinate grid
x_dim: FFTDimension = fft_dim_from_constraints(
    name = "x",
    pos_min = -150e-6,
    pos_max = 50e-6,
    freq_min = -12*k_L,
    freq_max = 4*k_L,
    loose_params = ["freq_min"]
)

# initialize FFTArray as harmonic oscillator groundstate
wf: FFTArray = get_ground_state_ho(
    dim = x_dim,
    tlib =  JaxTensorLib(),
    omega = omega_x,
    mass = mass_rb87
)

# dbg(generate_panel_plot(wf))

wf = shift_frequency(wf, {"x": 2*k_L})

# dbg(generate_panel_plot(wf))

def propagate(wf: FFTArray, *, dt: Union[float, complex], mass: float) -> FFTArray:
    k_sq = reduce(lambda a,b: a+b, [(2*np.pi*dim.fft_array(tlib=wf.tlib, space="freq", eager=eager))**2. for dim, eager in zip(wf.dims, wf.eager)])
    return wf.into(space="freq") * np.exp((-1.j * dt * hbar / (2*mass)) * k_sq) # type: ignore

def propagate_open(wf: FFTArray, *, dt: Union[float, complex], mass: float) -> FFTArray:
    k_sq = reduce(lambda a,b: a+b, [(2*np.pi*dim.fft_array(tlib=wf.tlib, space="freq", eager=eager))**2. for dim, eager in zip(wf.dims, wf.eager)])
    # dbg(generate_panel_plot(k_sq))
    k_mask = x_dim.fft_array(tlib=JaxTensorLib(), space="freq") > -4*k_L
    x_mask = x_dim.fft_array(tlib=JaxTensorLib(), space="pos") > -50e-6
    # dbg(generate_panel_plot(k_mask))
    # dbg(generate_panel_plot(x_mask))
    propagator = np.exp((-1.j * dt * hbar / (2*mass)) * k_sq)
    propagator = (propagator.into(space="pos")*x_mask).into(space="freq")
    # print(np.abs(k_sq.into(space="pos").values)**2)
    # dbg(generate_panel_plot(propagator))
    # dbg(generate_panel_plot(propagator * k_mask))
    # print((propagator).values)
    # print((propagator * k_mask).values)
    wf = wf * x_mask
    wf = wf.into(space="freq") * propagator
    # wf = wf.into(space="freq") * propagator
    wf = wf.into(space="pos") * x_mask
    return wf

wf = propagate_open(wf, dt=200e-5, mass=mass_rb87)
dbg(generate_panel_plot(wf))




