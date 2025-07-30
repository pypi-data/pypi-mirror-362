//! Memory module for Python
use std::sync::atomic::AtomicPtr;

use embive::interpreter::memory::Memory as _;
use pyo3::prelude::*;

use crate::{error::ProgramError, wrappers::MemoryWrapper};

/// Run a function with a memory scope.
///
/// Useful for passing memory reference to a python function.
pub fn memory_scope<R, F: FnOnce(&Py<Memory>) -> PyResult<R>>(
    memory_wrapper: &mut MemoryWrapper,
    scope: F,
) -> PyResult<R> {
    Python::with_gil(|py| {
        let memory = Memory {
            inner: Some(AtomicPtr::new(memory_wrapper as *mut MemoryWrapper)),
        };

        let memorypy = Py::new(py, memory)?;

        let ret = scope(&memorypy)?;

        // This is done so you can't use the Memory object after the scope, even if object is still held by Python
        memorypy.borrow_mut(py).inner = None;

        Ok(ret)
    })
}

/// Memory used by the interpreted code.
#[pyclass]
pub struct Memory {
    inner: Option<AtomicPtr<MemoryWrapper>>,
}

#[pymethods]
impl Memory {
    /// Load data from memory.
    ///
    /// Arguments:
    /// - `address`: Address to load from.
    /// - `len`: Length of data to load.
    ///
    /// Returns:
    /// - `Vec<u8>`: Data loaded from memory.
    pub fn load(&mut self, address: i32, len: u32) -> PyResult<Vec<u8>> {
        let address = address as u32;
        let inner = self.inner.as_mut().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Tried to access memory out of scope".to_string(),
            )
        })?;

        // Safety: Pointer is valid for as long as the struct is valid, borrow is guarded by pyo3 (this function is mutable).
        let memory = unsafe { &mut **inner.get_mut() };
        let result = memory.load(address, len).map_err(ProgramError::from);

        result.map(|data| data.to_vec()).map_err(|e| e.into())
    }

    /// Store data in memory.
    ///
    /// Arguments:
    /// - `address`: Address to store to.
    /// - `data`: Data to store.
    pub fn store(&mut self, address: i32, data: Vec<u8>) -> PyResult<()> {
        let address = address as u32;
        let inner = self.inner.as_mut().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Tried to access memory out of scope".to_string(),
            )
        })?;

        // Safety: Pointer is valid for as long as the struct is valid, borrow is guarded by pyo3 (this function is mutable).
        let memory = unsafe { &mut **inner.get_mut() };
        let result = memory.store(address, &data).map_err(ProgramError::from);

        result.map_err(|e| e.into())
    }
}
