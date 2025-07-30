from pybop_diffsol import DiffsolDense, DiffsolSparse, Config
import numpy as np

import pytest

solver_classes = [
    DiffsolDense,
    DiffsolSparse,
]


@pytest.mark.parametrize("solver_class", solver_classes)
def test_solve(solver_class):
    config = Config()
    model = solver_class(
        """
        in = [r, k]
        r { 1 } k { 1 }
        u_i { y = 0.1 }
        F_i { (r * y) * (1 - (y / k)) }
        """,
        config,
    )
    times = np.linspace(0.0, 1.0, 100)
    k = 1.0
    r = 1.0
    y0 = 0.1
    model.set_params(np.array([r, k]))
    y = model.solve(times)
    soln = k / (1.0 + (k - y0) * np.exp(-r * times) / y0)
    np.testing.assert_allclose(y[0], soln, rtol=1e-5)
