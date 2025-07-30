pub(crate) mod config;
pub(crate) mod cost_type;
pub(crate) mod error;
pub(crate) mod problem;

pub(crate) use config::Config;
pub(crate) use cost_type::CostType;
pub(crate) use error::PyDiffsolError;
pub(crate) use problem::Diffsol;

use numpy::{PyArray1, PyArray2, PyReadonlyArray1};
use pyo3::prelude::*;

macro_rules! create_diffsol_class {
    ($name:ident, $matrix:ty, $linear_solver:ty) => {
        #[pyclass]
        pub(crate) struct $name(Diffsol<$matrix>);

        #[pymethods]
        impl $name {
            #[new]
            fn new(code: &str, config: &Config) -> Result<Self, PyDiffsolError> {
                let inner = Diffsol::new(code, config)?;
                Ok(Self(inner))
            }

            #[pyo3(signature = (params, sigma=None))]
            fn set_params<'py>(
                &mut self,
                params: PyReadonlyArray1<'py, f64>,
                sigma: Option<f64>,
            ) -> Result<(), PyDiffsolError> {
                self.0.set_params(params, sigma)
            }

            #[pyo3(signature = (times, data, cost_type))]
            fn cost<'py>(
                &mut self,
                py: Python<'py>,
                times: PyReadonlyArray1<'py, f64>,
                data: PyReadonlyArray1<'py, f64>,
                cost_type: &CostType,
            ) -> Result<f64, PyDiffsolError> {
                match cost_type {
                    CostType::NegativeGaussianLogLikelihood() => self
                        .0
                        .cost_negative_gaussian_log_likelihood::<$linear_solver>(py, times, data),
                    CostType::SumOfPower(p) => self
                        .0
                        .cost_sum_of_power::<$linear_solver>(py, times, data, *p),
                    CostType::Minkowski(p) => {
                        self.0.cost_minkowski::<$linear_solver>(py, times, data, *p)
                    }
                    CostType::SumOfSquares() => self
                        .0
                        .cost_sum_squared_error::<$linear_solver>(py, times, data),
                    CostType::MeanAbsoluteError() => self
                        .0
                        .cost_mean_absolute_error::<$linear_solver>(py, times, data),
                    CostType::MeanSquaredError() => self
                        .0
                        .cost_mean_squared_error::<$linear_solver>(py, times, data),
                    CostType::RootMeanSquaredError() => self
                        .0
                        .cost_root_mean_squared_error::<$linear_solver>(py, times, data),
                }
            }

            #[cfg(feature = "diffsol-llvm")]
            #[pyo3(signature = (times, data, cost_type))]
            fn sens<'py>(
                &mut self,
                py: Python<'py>,
                times: PyReadonlyArray1<'py, f64>,
                data: PyReadonlyArray1<'py, f64>,
                cost_type: &CostType,
            ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
                match cost_type {
                    CostType::NegativeGaussianLogLikelihood() => self
                        .0
                        .cost_negative_gaussian_log_likelihood_sens::<$linear_solver>(
                            py, times, data,
                        ),
                    CostType::SumOfPower(p) => self
                        .0
                        .cost_sum_of_power_sens::<$linear_solver>(py, times, data, *p),
                    CostType::Minkowski(p) => self
                        .0
                        .cost_minkowski_sens::<$linear_solver>(py, times, data, *p),
                    CostType::SumOfSquares() => self
                        .0
                        .cost_sum_squared_error_sens::<$linear_solver>(py, times, data),
                    CostType::MeanAbsoluteError() => self
                        .0
                        .cost_mean_absolute_error_sens::<$linear_solver>(py, times, data),
                    CostType::MeanSquaredError() => self
                        .0
                        .cost_mean_squared_error_sens::<$linear_solver>(py, times, data),
                    CostType::RootMeanSquaredError() => self
                        .0
                        .cost_root_mean_squared_error_sens::<$linear_solver>(py, times, data),
                }
            }

            #[pyo3(signature = (times))]
            fn solve<'py>(
                &mut self,
                py: Python<'py>,
                times: PyReadonlyArray1<'py, f64>,
            ) -> Result<Bound<'py, PyArray2<f64>>, PyDiffsolError> {
                Diffsol::solve::<$linear_solver>(&mut self.0, py, times)
            }
        }
    };
}

create_diffsol_class!(
    DiffsolDense,
    diffsol::NalgebraMat<f64>,
    diffsol::NalgebraLU<f64>
);
create_diffsol_class!(
    DiffsolSparse,
    diffsol::FaerSparseMat<f64>,
    diffsol::FaerSparseLU<f64>
);

#[pymodule]
fn pybop_diffsol(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DiffsolDense>()?;
    m.add_class::<DiffsolSparse>()?;
    m.add_class::<Config>()?;
    m.add_class::<CostType>()?;
    Ok(())
}
