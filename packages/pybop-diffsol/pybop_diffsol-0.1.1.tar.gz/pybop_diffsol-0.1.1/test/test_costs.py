from pybop_diffsol import DiffsolDense, DiffsolSparse, Config
from pybop_diffsol import CostType
import numpy as np
import sys

import pytest

solver_classes = [
    DiffsolDense,
    DiffsolSparse,
]


dp = 0.1
k = 1.0
r = 1.0
y0 = 0.1
sigma = 0.1
n = 100
times = np.linspace(0.0, 1.0, n)
p = 2


def soln(times, r, k, y0):
    return k / (1.0 + (k - y0) * np.exp(-r * times) / y0)


def dsoln_dr(times, r, k, y0):
    return (
        -k
        * (k - y0)
        * np.exp(-r * times)
        / (y0 * (1.0 + (k - y0) * np.exp(-r * times) / y0) ** 2)
    )


def dsoln_dk(times, r, k, y0):
    return (1.0 + (k - y0) * np.exp(-r * times) / y0) ** -2


soln_orig = soln(times, r, k, y0)
soln_dp = soln(times, r + dp, k + dp, y0)

cost_types = [
    CostType.NegativeGaussianLogLikelihood(),
    CostType.SumOfPower(p),
    CostType.Minkowski(p),
    CostType.SumOfSquares(),
    CostType.MeanAbsoluteError(),
    CostType.MeanSquaredError(),
    CostType.RootMeanSquaredError(),
]

cost_name_and_type = [(type(t).__name__, t) for t in cost_types]

cost_expected = [
    -0.5 * np.log(2 * np.pi)
    - np.log(sigma)
    - 0.5
    * np.sum((soln_dp - soln_orig) ** 2)
    / (sigma**2),  # NegativeGaussianLogLikelihood
    np.sum((soln_dp - soln_orig) ** p),  # SumOfPower
    np.sum((soln_dp - soln_orig) ** p) ** (1 / p),  # Minkowski
    np.sum((soln_dp - soln_orig) ** 2),  # SumOfSquares
    np.sum(np.abs(soln_dp - soln_orig)) / n,  # MeanAbsoluteError
    np.sum((soln_dp - soln_orig) ** 2) / n,  # MeanSquaredError
    np.sqrt(np.mean((soln_dp - soln_orig) ** 2)),  # RootMeanSquaredError
]


eps = 1e-4
fd_dr = (soln(times, r + eps, k, y0) - soln(times, r - eps, k, y0)) / (2 * eps)
fd_dk = (soln(times, r, k + eps, y0) - soln(times, r, k - eps, y0)) / (2 * eps)
# dsoln = np.array([dsoln_dr(times, r, k, y0), dsoln_dk(times, r, k, y0)])
dsoln = np.array([fd_dr, fd_dk])

sens_expected = [
    -np.sum((soln_dp - soln_orig) * dsoln, axis=1)
    / (sigma**2),  # NegativeGaussianLogLikelihood
    p * np.sum((soln_dp - soln_orig) ** (p - 1) * dsoln, axis=1),  # SumOfPower
    (1.0 / p)
    * p
    * np.sum((soln_dp - soln_orig) ** (p - 1) * dsoln, axis=1)
    * np.sum((soln_dp - soln_orig) ** p) ** ((1 / p) - 1),  # Minkowski
    2 * np.sum((soln_dp - soln_orig) * dsoln, axis=1),  # SumOfSquares
    np.sum(np.sign(soln_dp - soln_orig) * dsoln, axis=1) / n,  # MeanAbsoluteError
    2 * np.sum((soln_dp - soln_orig) * dsoln, axis=1) / n,  # MeanSquaredError
    np.sum((soln_dp - soln_orig) * dsoln, axis=1)
    / (n * np.sqrt(np.mean((soln_dp - soln_orig) ** 2))),  # RootMeanSquaredError
]

solver_cost_type_and_expected = [
    (cls, cost_name, cost, expected)
    for cls in solver_classes
    for (cost_name, cost), expected in zip(cost_name_and_type, cost_expected)
]
solver_sens_type_and_expected = [
    (cls, cost_name, cost, expected)
    for cls in solver_classes
    for (cost_name, cost), expected in zip(cost_name_and_type, sens_expected)
]


# def test_sens_calculation():
#    dr = dsoln_dr(times, r, k, y0)
#    dk = dsoln_dk(times, r, k, y0)
#    fd_dr = (soln(times, r + eps, k, y0) - soln(times, r - eps, k, y0)) / (2 * eps)
#    fd_dk = (soln(times, r, k + eps, y0) - soln(times, r, k - eps, y0)) / (2 * eps)
#    np.testing.assert_allclose(dr, fd_dr, rtol=1e-5)
#    np.testing.assert_allclose(dk, fd_dk, rtol=1e-5)

model_str = """
in = [r, k]
r { 1 } k { 1 }
u_i { y = 0.1 }
F_i { (r * y) * (1 - (y / k)) }
"""


@pytest.mark.parametrize(
    "solver_class, cost_name, cost_type, expected", solver_cost_type_and_expected
)
def test_costs(solver_class, cost_name, cost_type, expected):
    config = Config()
    model = solver_class(model_str, config)

    model.set_params(np.array([r, k]))
    data = model.solve(times).reshape(-1)

    if isinstance(cost_type, CostType.NegativeGaussianLogLikelihood):
        model.set_params(np.array([r, k]), sigma=sigma)
    else:
        model.set_params(np.array([r, k]))
        cost = model.cost(times, data, cost_type)
        np.testing.assert_allclose(cost, 0.0, rtol=1e-5)

    if isinstance(cost_type, CostType.NegativeGaussianLogLikelihood):
        model.set_params(np.array([r + dp, k + dp]), sigma=sigma)
    else:
        model.set_params(np.array([r + dp, k + dp]))

    cost = model.cost(times, data, cost_type)
    np.testing.assert_allclose(cost, expected, rtol=1e-4)


@pytest.mark.skipif(
    sys.platform == "win32", reason="Sensitivity analysis not supported on Windows"
)
@pytest.mark.parametrize(
    "solver_class, cost_name, cost_type, expected", solver_sens_type_and_expected
)
def test_sens(solver_class, cost_name, cost_type, expected):
    config = Config()
    config.rtol = 1e-10
    config.atol = 1e-10
    model = solver_class(model_str, config)

    model.set_params(np.array([r, k]))
    data = model.solve(times).reshape(-1)

    if isinstance(cost_type, CostType.NegativeGaussianLogLikelihood):
        model.set_params(np.array([r + dp, k + dp]), sigma=sigma)
    else:
        model.set_params(np.array([r + dp, k + dp]))

    (cost, sens) = model.sens(times, data, cost_type)
    print("Cost:", cost, "Expected:", expected, "Type:", cost_name)
    np.testing.assert_allclose(sens, expected, rtol=1e-1)
