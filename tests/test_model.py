import numpy as np
import pytest

from dynamical_model import ModelParameters, derivatives, simulate


def test_derivatives_are_finite():
    output = derivatives(np.array([0.2, 0.3, 0.4, 0.1]), ModelParameters())
    assert output.shape == (4,)
    assert np.isfinite(output).all()


def test_simulation_shape_and_initial_state():
    initial = (0.1, 0.2, 0.3, 0.05)
    time, states = simulate(ModelParameters(), initial, duration=12, steps=120)
    assert time.shape == (120,)
    assert states.shape == (120, 4)
    np.testing.assert_allclose(states[0], initial)
    assert np.isfinite(states).all()


def test_invalid_simulation_arguments():
    with pytest.raises(ValueError):
        simulate(ModelParameters(), duration=0)
