// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
//! Optional Python bindings for the AGESA search and `agesafetch` CLI.
use std::env;
use std::fmt::{self, Display, Formatter};

use linux_memutils::agesa::{AgesaVersion, SearchError};
use pyo3::create_exception;
use pyo3::exceptions::{PyOSError, PySystemExit};
use pyo3::prelude::*;

use crate::run_cli;

create_exception!(
    agesafetch,
    DevMemOpenError,
    PyOSError,
    "Raised when the `/dev/mem` file could not be opened."
);
create_exception!(
    agesafetch,
    IomemReadError,
    PyOSError,
    "Raised when the `/dev/iomem` file could not be read."
);
create_exception!(
    agesafetch,
    ByteReadError,
    PyOSError,
    "Raised when a byte in `/dev/mem` could not be read."
);

struct PySearchError(SearchError);

impl From<PySearchError> for PyErr {
    fn from(error: PySearchError) -> Self {
        match error.0 {
            SearchError::DevMemUnopenable(source) => {
                DevMemOpenError::new_err(format!("Could not open `/dev/mem`: {source}"))
            }
            SearchError::IomemUnreadable(source) => {
                IomemReadError::new_err(format!("Could not read `/proc/iomem`: {source}"))
            }
            SearchError::ByteUnreadable(source) => {
                ByteReadError::new_err(format!("Could not read byte in `/dev/mem`: {source}"))
            }
        }
    }
}

impl From<SearchError> for PySearchError {
    fn from(error: SearchError) -> Self {
        Self(error)
    }
}

/// An AGESA version found in physical memory.
#[pyclass(name = "AGESAVersion", module = "agesafetch", get_all, str)]
struct PyAgesaVersion {
    /// The complete version string (may include trailing whitespace).
    version_string: String,
    /// The absolute start address of this version in physical memory.
    absolute_address: usize,
}

#[pymethods]
impl PyAgesaVersion {
    #[new]
    fn new(version_string: String, absolute_address: usize) -> Self {
        PyAgesaVersion {
            version_string,
            absolute_address,
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "AGESAVersion('{}', absolute_address={})",
            self.version_string, self.absolute_address
        )
    }
}

impl Display for PyAgesaVersion {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} (at {:#018x})",
            self.version_string, self.absolute_address
        )
    }
}

impl From<AgesaVersion> for PyAgesaVersion {
    fn from(found_version: AgesaVersion) -> Self {
        Self {
            version_string: found_version.version_string,
            absolute_address: found_version.absolute_address,
        }
    }
}

/// Search for the `AGESA`_ version in physical memory.
///
/// .. note::
///    This requires *elevated privileges* in order to obtain a memory
///    map from `/proc/iomem` and read physical memory from `/dev/mem`.
///
/// .. _`AGESA`: https://en.wikipedia.org/wiki/AGESA
///
/// :return: An :class:`AGESAVersion` instance or ``None``
#[pyfunction]
fn find_agesa_version() -> Result<Option<PyAgesaVersion>, PySearchError> {
    let maybe_found_version = linux_memutils::agesa::find_agesa_version()?;
    Ok(maybe_found_version.map(PyAgesaVersion::from))
}

/// An entrypoint providing the `agesafetch` CLI to the Python package.
///
/// For details, see:
///   * https://github.com/PyO3/maturin/issues/368
///   * https://www.maturin.rs/bindings#both-binary-and-library
#[pyfunction]
fn run_py() -> PyResult<()> {
    let args = env::args_os().skip(1).collect();
    let exit_code = run_cli(args);
    Err(PySystemExit::new_err(exit_code as u8))
}

#[pymodule]
fn agesafetch(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyAgesaVersion>()?;
    m.add_function(wrap_pyfunction!(find_agesa_version, m)?)?;
    m.add_wrapped(wrap_pyfunction!(run_py))?;

    m.add("DevMemOpenError", py.get_type::<DevMemOpenError>())?;
    m.add("IomemReadError", py.get_type::<IomemReadError>())?;
    m.add("ByteReadError", py.get_type::<ByteReadError>())?;

    Ok(())
}
