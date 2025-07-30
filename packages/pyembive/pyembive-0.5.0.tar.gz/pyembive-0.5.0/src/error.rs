//! Error module
use pyo3::{exceptions::PyRuntimeError, prelude::*};
use std::{error::Error, fmt::Display};

#[derive(Debug)]
pub enum ProgramError {
    /// Error in the interpreter.
    Interpreter(embive::interpreter::Error),
    /// Error in the transpiler.
    Transpiler(embive::transpiler::Error),
    /// Error from Python.
    Python(PyErr),
}

impl Display for ProgramError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProgramError::Interpreter(err) => write!(f, "Interpreter error: {}", err),
            ProgramError::Transpiler(err) => write!(f, "Transpiler error: {}", err),
            ProgramError::Python(err) => write!(f, "Python error: {}", err),
        }
    }
}

impl From<embive::interpreter::Error> for ProgramError {
    fn from(err: embive::interpreter::Error) -> Self {
        ProgramError::Interpreter(err)
    }
}

impl From<embive::transpiler::Error> for ProgramError {
    fn from(err: embive::transpiler::Error) -> Self {
        ProgramError::Transpiler(err)
    }
}

impl From<PyErr> for ProgramError {
    fn from(err: PyErr) -> Self {
        ProgramError::Python(err)
    }
}

impl From<ProgramError> for PyErr {
    fn from(val: ProgramError) -> Self {
        PyRuntimeError::new_err(val.to_string())
    }
}

impl Error for ProgramError {}
