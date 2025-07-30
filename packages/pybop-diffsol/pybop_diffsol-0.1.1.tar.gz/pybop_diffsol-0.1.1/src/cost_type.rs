use pyo3::prelude::*;

#[pyclass]
pub(crate) enum CostType {
    NegativeGaussianLogLikelihood(),
    SumOfPower(i32),
    Minkowski(i32),
    SumOfSquares(),
    MeanAbsoluteError(),
    MeanSquaredError(),
    RootMeanSquaredError(),
}
