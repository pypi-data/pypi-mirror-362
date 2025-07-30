use pyo3::prelude::*;

#[pyclass]
pub(crate) struct Config {
    #[pyo3(get, set)]
    pub(crate) rtol: f64,
    #[pyo3(get, set)]
    pub(crate) atol: f64,
}

#[pymethods]
impl Config {
    #[new]
    pub(crate) fn new() -> Self {
        Self {
            rtol: 1e-6,
            atol: 1e-6,
        }
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("Config(rtol={}, atol={})", self.rtol, self.atol))
    }
}
