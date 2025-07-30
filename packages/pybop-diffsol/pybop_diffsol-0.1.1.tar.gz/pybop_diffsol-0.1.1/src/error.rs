use diffsol::error::DiffsolError;
use pyo3::{exceptions::PyValueError, PyErr};

#[derive(Debug)]
pub(crate) struct PyDiffsolError(DiffsolError);

impl PyDiffsolError {
    pub fn new(error: DiffsolError) -> Self {
        Self(error)
    }
}

impl From<PyDiffsolError> for PyErr {
    fn from(error: PyDiffsolError) -> Self {
        PyValueError::new_err(error.0.to_string())
    }
}

impl From<DiffsolError> for PyDiffsolError {
    fn from(other: DiffsolError) -> Self {
        Self(other)
    }
}
