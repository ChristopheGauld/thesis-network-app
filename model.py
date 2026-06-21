"""Simulation utilities for the pedagogical X–Y–Z dynamical system."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ModelParameters:
    coupling_yx: float = 1.15
    coupling_zy: float = 0.95
    feedback_xy: float = 0.35
    feedback_xz: float = 0.20
    feedback_yz: float = 0.30
    decay_x: float = 0.85
    decay_y: float = 0.75
    decay_z: float = 0.65
    nonlinearity: float = 0.12
    external_input: float = 0.20
    tau_x: float = 1.00
    tau_y: float = 0.82
    tau_z: float = 0.62


def derivatives(state: np.ndarray, params: ModelParameters) -> np.ndarray:
    """Return derivatives for X=symptom, Y=mechanism, Z=context/intervention."""
    x, y, z = state
    cubic = params.nonlinearity
    dx = params.tau_x * (
        params.coupling_yx * y - params.decay_x * x - cubic * x**3
    )
    dy = params.tau_y * (
        params.coupling_zy * z
        + params.feedback_xy * x
        - params.decay_y * y
        - cubic * y**3
    )
    dz = params.tau_z * (
        params.external_input
        + params.feedback_xz * x
        + params.feedback_yz * y
        - params.decay_z * z
        - cubic * z**3
    )
    return np.array([dx, dy, dz], dtype=float)


def _rk4_step(state: np.ndarray, dt: float, params: ModelParameters) -> np.ndarray:
    k1 = derivatives(state, params)
    k2 = derivatives(state + dt * k1 / 2, params)
    k3 = derivatives(state + dt * k2 / 2, params)
    k4 = derivatives(state + dt * k3, params)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def simulate(
    params: ModelParameters,
    initial_state: tuple[float, float, float] = (0.25, 0.20, 0.15),
    duration: float = 24.0,
    steps: int = 600,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the system with a deterministic fourth-order Runge–Kutta method."""
    if duration <= 0 or steps < 2:
        raise ValueError("duration must be positive and steps must be at least 2")
    time = np.linspace(0.0, duration, steps)
    states = np.zeros((steps, 3), dtype=float)
    states[0] = np.asarray(initial_state, dtype=float)
    dt = time[1] - time[0]
    for index in range(1, steps):
        states[index] = _rk4_step(states[index - 1], dt, params)
    return time, states
