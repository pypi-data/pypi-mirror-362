use std::sync::{Arc, Mutex};

use crate::{Config, PyDiffsolError};
use diffsol::{
    error::DiffsolError, matrix::MatrixRef, DefaultDenseMatrix, DiffSl, LinearSolver, Matrix,
    NonLinearOp, NonLinearOpSens, OdeBuilder, OdeEquations, OdeSolverMethod, OdeSolverProblem, Op,
    Vector, VectorHost, VectorRef,
};
use numpy::{
    ndarray::{s, Array1, Array2},
    IntoPyArray, PyArray1, PyArray2, PyArrayMethods, PyReadonlyArray1, PyUntypedArrayMethods,
};
use pyo3::{Bound, Python};
#[cfg(feature = "diffsol-cranelift")]
type CG = diffsol::CraneliftJitModule;
#[cfg(feature = "diffsol-llvm")]
type CG = diffsol::LlvmModule;

pub(crate) struct Diffsol<M>
where
    M: Matrix<T = f64>,
    M::V: VectorHost,
{
    problem: Arc<Mutex<OdeSolverProblem<DiffSl<M, CG>>>>,
    sigma: Option<f64>,
}

impl<M> Diffsol<M>
where
    M: Matrix<T = f64>,
    M::V: VectorHost + DefaultDenseMatrix,
    for<'b> &'b M::V: VectorRef<M::V>,
    for<'b> &'b M: MatrixRef<M>,
{
    pub(crate) fn new(code: &str, config: &Config) -> Result<Self, PyDiffsolError> {
        let problem = OdeBuilder::<M>::new()
            .rtol(config.rtol)
            .atol([config.atol])
            .build_from_diffsl(code)?;
        Ok(Self {
            problem: Arc::new(Mutex::new(problem)),
            sigma: None,
        })
    }

    pub(crate) fn set_params<'py>(
        &mut self,
        params: PyReadonlyArray1<'py, f64>,
        sigma: Option<f64>,
    ) -> Result<(), PyDiffsolError> {
        let mut problem = self
            .problem
            .lock()
            .map_err(|e| PyDiffsolError::new(DiffsolError::Other(e.to_string())))?;
        let params = params.as_array();
        let fparams = M::V::from_slice(params.as_slice().unwrap(), problem.context().clone());
        problem.eqn.set_params(&fparams);
        self.sigma = sigma;
        Ok(())
    }

    pub(crate) fn cost_negative_gaussian_log_likelihood<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<f64, PyDiffsolError> {
        let sigma = self.sigma.ok_or_else(|| {
            PyDiffsolError::new(DiffsolError::Other(
                "Sigma must be set before computing cost".to_string(),
            ))
        })?;
        let f = |out: f64, d: f64| (out - d).powi(2);
        let cost = self.cost::<LS, _>(_py, times, data, f)?;
        Ok(-0.5 * (2.0 * std::f64::consts::PI).ln() - sigma.ln() - 0.5 * cost / (sigma * sigma))
    }
    pub(crate) fn cost_negative_gaussian_log_likelihood_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let sigma = self.sigma.ok_or_else(|| {
            PyDiffsolError::new(DiffsolError::Other(
                "Sigma must be set before computing cost".to_string(),
            ))
        })?;
        let f = |out: f64, d: f64| (out - d).powi(2);
        let (cost, sens) =
            self.cost_sens::<LS, _, _>(_py, times, data, f, |out, d, out_sens, sens| {
                for (s, &os) in sens.iter_mut().zip(out_sens.as_slice().iter()) {
                    *s += 2.0 * (out - d) * os;
                }
            })?;
        let cost =
            -0.5 * (2.0 * std::f64::consts::PI).ln() - sigma.ln() - cost / (2.0 * sigma * sigma);
        unsafe { sens.as_array_mut() }
            .iter_mut()
            .for_each(|s| *s /= -2.0 * sigma * sigma);
        Ok((cost, sens))
    }

    /// Sum of power cost function: `C(x, y) = sum(|x - y|^p`
    pub(crate) fn cost_sum_of_power<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        p: i32,
    ) -> Result<f64, PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).abs().powi(p);
        self.cost::<LS, _>(_py, times, data, f)
    }

    pub(crate) fn cost_sum_of_power_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        p: i32,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).abs().powi(p);
        let fs = |out: f64, d: f64, out_sens: &M::V, sens: &mut Array1<f64>| {
            for (s, &os) in sens.iter_mut().zip(out_sens.as_slice().iter()) {
                *s += (p as f64) * (out - d).abs().powi(p - 1) * os;
            }
        };
        self.cost_sens::<LS, _, _>(_py, times, data, f, fs)
    }

    /// minkowski cost function: `C(x, y) = (sum(|x - y|^p))^(1/p)`
    pub(crate) fn cost_minkowski<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        p: i32,
    ) -> Result<f64, PyDiffsolError> {
        let cost = self.cost_sum_of_power::<LS>(_py, times, data, p)?;
        if cost == 0.0 {
            return Ok(0.0);
        }
        Ok(cost.powf(1.0 / p as f64))
    }
    pub(crate) fn cost_minkowski_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        p: i32,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let (cost, sens) = self.cost_sum_of_power_sens::<LS>(_py, times, data, p)?;
        if cost == 0.0 {
            return Ok((0.0, sens));
        }
        if p == 1 {
            return Ok((cost, sens)); // For p=1, the cost is already the sum of absolute differences
        }
        let pow_cost = cost.powf(1.0 / p as f64);
        unsafe { sens.as_array_mut() }
            .iter_mut()
            .for_each(|s| *s /= p as f64 * cost.powf(1. - 1. / p as f64));
        Ok((pow_cost, sens))
    }

    /// Sum of squared errors cost function: `C(x, y) = (x - y)^2`
    pub(crate) fn cost_sum_squared_error<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<f64, PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).powi(2);
        self.cost::<LS, _>(_py, times, data, f)
    }
    pub(crate) fn cost_sum_squared_error_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).powi(2);
        let fs = |out: f64, d: f64, out_sens: &M::V, sens: &mut Array1<f64>| {
            for (s, &os) in sens.iter_mut().zip(out_sens.as_slice().iter()) {
                *s += 2.0 * (out - d) * os;
            }
        };
        self.cost_sens::<LS, _, _>(_py, times, data, f, fs)
    }

    /// Mean absolute error cost function: `C(x, y) = |x - y|`
    pub(crate) fn cost_mean_absolute_error<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<f64, PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).abs();
        let n = times.shape()[0];
        let cost = self.cost::<LS, _>(_py, times, data, f)?;
        Ok(cost / n as f64) // Normalize by number of data points
    }
    pub(crate) fn cost_mean_absolute_error_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let f = |out: f64, d: f64| (out - d).abs();
        let fs = |out: f64, d: f64, out_sens: &M::V, sens: &mut Array1<f64>| {
            for (s, &os) in sens.iter_mut().zip(out_sens.as_slice().iter()) {
                if out > d {
                    *s += os; // Positive difference
                } else if out < d {
                    *s -= os; // Negative difference
                }
            }
        };
        let n = times.shape()[0];
        let (cost, sens) = self.cost_sens::<LS, _, _>(_py, times, data, f, fs)?;
        unsafe { sens.as_array_mut() }
            .iter_mut()
            .for_each(|s| *s /= n as f64); // Normalize sensitivity by number of data points
        Ok((cost / n as f64, sens)) // Normalize by number of data points
    }

    /// Mean squared error cost function: `C(x, y) = (x - y)^2`
    pub(crate) fn cost_mean_squared_error<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<f64, PyDiffsolError> {
        let n = times.shape()[0];
        let cost = self.cost_sum_squared_error::<LS>(_py, times, data)?;
        Ok(cost / n as f64) // Normalize by number of data points
    }
    pub(crate) fn cost_mean_squared_error_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let n = times.shape()[0] as f64;
        let (cost, sens) = self.cost_sum_squared_error_sens::<LS>(_py, times, data)?;
        unsafe { sens.as_array_mut() }
            .iter_mut()
            .for_each(|s| *s /= n); // Normalize sensitivity by number of data points
        Ok((cost / n, sens)) // Normalize by number of data points
    }

    /// Root mean squared error cost function: `C(x, y) = sqrt(sum((x(p) - y)^2) / n)`
    /// sensitivity is  dC/p = 1/(2*sqrt(sum((x(p) - y)^2)/n)) * sum((x(p) - y)*dx/dp/n)
    pub(crate) fn cost_root_mean_squared_error<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<f64, PyDiffsolError> {
        let cost = self.cost_mean_squared_error::<LS>(_py, times, data)?;
        Ok(cost.sqrt())
    }
    pub(crate) fn cost_root_mean_squared_error_sens<'py, LS: LinearSolver<M>>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let (cost, sens) = self.cost_mean_squared_error_sens::<LS>(_py, times, data)?;
        if cost == 0.0 {
            return Ok((0.0, sens));
        }
        let sqrt_cost = cost.sqrt();
        unsafe { sens.as_array_mut() }
            .iter_mut()
            .for_each(|s| *s /= 2.0 * sqrt_cost); // Normalize sensitivity by 2*sqrt(cost)
        Ok((sqrt_cost, sens))
    }

    pub(crate) fn cost<'py, LS: LinearSolver<M>, F: Fn(f64, f64) -> f64>(
        &mut self,
        _py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        f: F,
    ) -> Result<f64, PyDiffsolError> {
        let problem = self
            .problem
            .lock()
            .map_err(|e| PyDiffsolError::new(DiffsolError::Other(e.to_string())))?;
        let times = times.as_array();
        let data = data.as_array();
        let mut solver = problem.bdf::<LS>()?;
        let nout = if let Some(_out) = problem.eqn.out() {
            problem.eqn.nout()
        } else {
            problem.eqn.nstates()
        };
        if nout != 1 {
            return Err(PyDiffsolError::new(DiffsolError::Other(
                "Cost function only supports single output equations".to_string(),
            )));
        }
        let mut cost = 0.0;
        let mut y_tmp = if problem.eqn.out().is_some() {
            Some(M::V::zeros(nout, problem.context().clone()))
        } else {
            None
        };
        for (&t, &d) in times.iter().zip(data.iter()) {
            while solver.state().t < t {
                solver.step()?;
            }
            let y = solver.interpolate(t)?;
            let out = if let Some(out) = problem.eqn.out() {
                let y_tmp = y_tmp.as_mut().unwrap();
                out.call_inplace(&y, t, y_tmp);
                y_tmp[0]
            } else {
                y[0]
            };
            cost += f(out, d);
        }
        Ok(cost)
    }

    pub(crate) fn cost_sens<
        'py,
        LS: LinearSolver<M>,
        F: Fn(f64, f64) -> f64,
        FS: Fn(f64, f64, &M::V, &mut Array1<f64>),
    >(
        &mut self,
        py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
        data: PyReadonlyArray1<'py, f64>,
        f: F,
        fs: FS,
    ) -> Result<(f64, Bound<'py, PyArray1<f64>>), PyDiffsolError> {
        let problem = self
            .problem
            .lock()
            .map_err(|e| PyDiffsolError::new(DiffsolError::Other(e.to_string())))?;
        let times = times.as_array();
        let data = data.as_array();
        let mut solver = problem.bdf_sens::<LS>()?;
        let nout = if let Some(_out) = problem.eqn.out() {
            problem.eqn.nout()
        } else {
            problem.eqn.nstates()
        };
        let nparams = problem.eqn.nparams();
        if nout != 1 {
            return Err(PyDiffsolError::new(DiffsolError::Other(
                "Cost function only supports single output equations".to_string(),
            )));
        }
        let mut cost = 0.0;
        let mut sens = Array1::zeros(nparams);
        let mut sens_tmp = M::V::zeros(nparams, problem.context().clone());
        let mut tmp = if problem.eqn.out().is_some() {
            Some((
                M::V::zeros(nout, problem.context().clone()),
                M::V::zeros(nparams, problem.context().clone()),
            ))
        } else {
            None
        };
        for (&t, &d) in times.iter().zip(data.iter()) {
            while solver.state().t < t {
                solver.step()?;
            }
            let y = solver.interpolate(t)?;
            let y_sens = solver.interpolate_sens(t)?;
            for (stmp, ys) in sens_tmp.as_mut_slice().iter_mut().zip(y_sens.iter()) {
                *stmp = ys[0];
            }
            let (out_value, out_sens) = if let Some(out) = problem.eqn.out() {
                let (y_tmp, sens_tmp2) = tmp.as_mut().unwrap();
                out.call_inplace(&y, t, y_tmp);
                out.sens_mul_inplace(&y, t, &sens_tmp, sens_tmp2);
                (y_tmp[0], &*sens_tmp2)
            } else {
                (y[0], &sens_tmp)
            };
            cost += f(out_value, d);
            fs(out_value, d, out_sens, &mut sens);
        }
        Ok((cost, sens.into_pyarray(py)))
    }

    pub(crate) fn solve<'py, LS: LinearSolver<M>>(
        &mut self,
        py: Python<'py>,
        times: PyReadonlyArray1<'py, f64>,
    ) -> Result<Bound<'py, PyArray2<f64>>, PyDiffsolError> {
        let problem = self
            .problem
            .lock()
            .map_err(|e| PyDiffsolError::new(DiffsolError::Other(e.to_string())))?;
        let times = times.as_array();
        let mut solver = problem.bdf::<LS>()?;
        let nout = if let Some(_out) = problem.eqn.out() {
            problem.eqn.nout()
        } else {
            problem.eqn.nstates()
        };
        let mut sol = Array2::zeros((nout, times.len()));
        for (i, &t) in times.iter().enumerate() {
            while solver.state().t < t {
                solver.step()?;
            }
            let y = solver.interpolate(t)?;
            let out = if let Some(out) = problem.eqn.out() {
                out.call(&y, t)
            } else {
                y
            };
            sol.slice_mut(s![.., i])
                .iter_mut()
                .zip(out.as_slice().iter())
                .for_each(|(a, b)| *a = *b);
        }
        Ok(sol.into_pyarray(py))
    }
}

// tests
#[cfg(test)]
mod tests {
    use numpy::array;
    use numpy::ToPyArray;

    use super::*;

    #[test]
    fn test_diffsol_new() {
        type M = diffsol::FaerSparseMat<f64>;
        type LS = diffsol::FaerSparseLU<f64>;
        let code = "
            in = [r, k]
            r { 1 } k { 1 }
            u_i { y = 0.1 }
            F_i { (r * y) * (1 - (y / k)) }
        ";
        let config = Config::new();
        let mut diffsol = Diffsol::<M>::new(code, &config).unwrap();
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let times = array![0.0, 1.0].to_pyarray(py);
            let data = array![0.0, 1.0].to_pyarray(py);
            diffsol
                .cost_mean_squared_error_sens::<LS>(py, times.readonly(), data.readonly())
                .unwrap();
        });
    }
}
