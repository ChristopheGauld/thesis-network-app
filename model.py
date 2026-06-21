"""Dynamical system discussed in the computational psychiatry project."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ModelParameters:
    """Parameters reported in *Dynamical Systems for Computational Psychiatry*."""

    tau_x: float = 14.0
    tau_y: float = 14.0
    tau_z: float = 1.0
    tau_f: float = 720.0
    s_max: float = 10.0
    r_s: float = 1.0
    r_b: float = 1.04
    lambda_s: float = 0.1
    lambda_b: float = 0.05
    p_max: float = 10.0
    predisposition_l: float = 0.2
    lambda_f: float = 1.0
    environmental_sensitivity: float = 4.0
    alpha: float = 0.5
    beta: float = 0.5


CLINICAL_PROFILES = {
    "Situation saine": dict(r_b=1.04, predisposition_l=0.20, environmental_sensitivity=4.0),
    "Spectre de la schizophrénie": dict(r_b=0.904, predisposition_l=0.20, environmental_sensitivity=4.0),
    "Trouble bipolaire à cycles rapides": dict(r_b=1.04, predisposition_l=1.01, environmental_sensitivity=10.0),
    "Deuil complexe persistant": dict(r_b=1.00, predisposition_l=0.60, environmental_sensitivity=4.5),
}


def derivatives(
    state: np.ndarray,
    params: ModelParameters,
    zeta: float = 1.0,
) -> np.ndarray:
    """Return the four derivatives from equations (1)-(4) of the project."""
    x, y, z, slow_f = state
    symptom_drive = params.s_max / (
        1.0 + np.exp(np.clip((params.r_s - y) / params.lambda_s, -60, 60))
    )
    potentiation_drive = params.p_max / (
        1.0 + np.exp(np.clip((params.r_b - y) / params.lambda_b, -60, 60))
    )
    dx = (symptom_drive - x) / params.tau_x
    dy = (
        potentiation_drive
        + slow_f * params.predisposition_l
        - x * y
        - z
    ) / params.tau_y
    dz = (
        params.environmental_sensitivity
        * (params.alpha * x + params.beta * y)
        * zeta
        - z
    ) / params.tau_z
    df = (y - params.lambda_f * slow_f) / params.tau_f
    return np.array([dx, dy, dz, df], dtype=float)


def _rk4_step(
    state: np.ndarray,
    dt: float,
    params: ModelParameters,
    zeta: float,
) -> np.ndarray:
    k1 = derivatives(state, params, zeta)
    k2 = derivatives(state + dt * k1 / 2, params, zeta)
    k3 = derivatives(state + dt * k2 / 2, params, zeta)
    k4 = derivatives(state + dt * k3, params, zeta)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def simulate(
    params: ModelParameters,
    initial_state: tuple[float, float, float, float] = (0.0, 0.1, 0.0, 0.0),
    duration: float = 800.0,
    steps: int = 2400,
    noise_strength: float = 0.0,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the reported model; ``noise_strength`` controls Gaussian zeta(t)."""
    if duration <= 0 or steps < 2:
        raise ValueError("duration must be positive and steps must be at least 2")
    time = np.linspace(0.0, duration, steps)
    states = np.zeros((steps, 4), dtype=float)
    states[0] = np.asarray(initial_state, dtype=float)
    dt = time[1] - time[0]
    rng = np.random.default_rng(seed)
    for index in range(1, steps):
        zeta = 1.0 + noise_strength * rng.normal()
        states[index] = _rk4_step(states[index - 1], dt, params, zeta)
        states[index, :2] = np.maximum(states[index, :2], 0.0)
    return time, states
