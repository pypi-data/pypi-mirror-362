//! Embive Python bindings
mod error;
mod memory;
mod wrappers;

use std::num::NonZeroI32;

use embive::{interpreter::State, transpiler::transpile_elf_vec};
use memory::{memory_scope, Memory};
use pyo3::{prelude::*, types::PyFunction};

use error::ProgramError;
use wrappers::{InterpreterWrapper, MemoryWrapper};

/// State of the program.
#[pyclass(eq, eq_int)]
#[derive(PartialEq)]
pub enum ProgramState {
    /// Interpreter running. Call `run` to continue running.
    Running,
    /// Interpreter was called (syscall). Optionally call `syscall` to handle the syscall and then `run` to continue running.
    Called,
    /// Interpreter waiting interrupt. Optionally call `interrupt` to trigger an interrupt and then `run` to continue running.
    Waiting,
    /// Interpreter halted. Call `reset` and then `run` to run again.
    Halted,
}

impl From<State> for ProgramState {
    fn from(state: State) -> Self {
        match state {
            State::Running => ProgramState::Running,
            State::Called => ProgramState::Called,
            State::Waiting => ProgramState::Waiting,
            State::Halted => ProgramState::Halted,
        }
    }
}

/// Syscall Result
#[pyclass]
#[derive(Clone, Copy)]
pub enum SyscallResult {
    /// Syscall was successful.
    ///
    /// This is a 32-bit integer that indicates the result.
    Ok(i32),
    /// Syscall failed.
    ///
    /// This is a non-zero 32-bit integer that indicates the error.
    Err(NonZeroI32),
}

/// Transpile RISC-V ELF to Embive binary
///
/// Arguments:
/// - `elf`: ELF file bytes to transpile.
///
/// Returns:
/// - Transpiled binary bytes.
#[pyfunction]
fn transpile(elf: &[u8]) -> PyResult<Vec<u8>> {
    let ret = transpile_elf_vec(elf).map_err(ProgramError::from);
    ret.map_err(|e| e.into())
}

/// Embive Program
#[pyclass]
struct Program {
    interpreter: InterpreterWrapper,
}

#[pymethods]
impl Program {
    /// Create a new program with the given code and RAM size.
    ///
    /// The code should already be in the embive format. Use the `transpile` function to convert from RISC-V.
    ///
    /// Arguments:
    /// - `code`: Code bytes to run.
    /// - `ram_size`: Size of the RAM in bytes.
    /// - `instruction_limit`: Instruction limit for the interpreter (0 = no limit).
    #[new]
    fn new(code: Vec<u8>, ram_size: usize, instruction_limit: u32) -> Self {
        let memory = MemoryWrapper::new(code, ram_size);
        let interpreter = InterpreterWrapper::new(memory, instruction_limit);
        Program { interpreter }
    }

    /// Fetch current instruction
    ///
    /// Returns:
    /// - Current instruction (as raw 32-bit integer).
    fn fetch(&mut self) -> PyResult<u32> {
        let result: Result<u32, ProgramError> = self
            .interpreter
            .with_interpreter_mut(|interpreter| interpreter.fetch())
            .map(|instruction| instruction.into())
            .map_err(ProgramError::from);

        result.map_err(|e| e.into())
    }

    /// Run the program
    ///
    /// Returns:
    /// - `ProgramState`: Current state of the program (Check `ProgramState`).
    fn run(&mut self) -> PyResult<ProgramState> {
        let state = self
            .interpreter
            .with_interpreter_mut(|interpreter| interpreter.run())
            .map(ProgramState::from)
            .map_err(ProgramError::from);

        state.map_err(|e| e.into())
    }

    /// Reset the program.
    fn reset(&mut self) -> PyResult<()> {
        self.interpreter
            .with_interpreter_mut(|interpreter| interpreter.reset());
        Ok(())
    }

    /// Trigger an interrupt.
    /// 
    /// Arguments:
    /// - `value`: 32-bit signed integer value to be passed to the interrupt handler.
    fn interrupt(&mut self, value: i32) -> PyResult<()> {
        let result = self
            .interpreter
            .with_interpreter_mut(|interpreter| interpreter.interrupt(value))
            .map_err(ProgramError::from);

        result.map_err(|e| e.into())
    }

    /// Handle a syscall.
    ///
    /// Arguments:
    /// - `syscall_fn`: Python function to call for the syscall.
    ///     - Example: `def syscall(nr: int, args: List[int], memory: MemoryPy) -> SyscallResult`
    fn syscall(&mut self, syscall_fn: Bound<'_, PyFunction>) -> PyResult<()> {
        let result = self.interpreter.with_interpreter_mut(|interpreter| {
            interpreter.syscall(&mut |nr,
                                      args,
                                      memory|
             -> Result<Result<i32, NonZeroI32>, ProgramError> {
                let syscall_scope = |memory: &Py<Memory>| {
                    let ret = syscall_fn.call1((nr, args, memory))?;

                    let result: SyscallResult = ret.extract()?;

                    match result {
                        SyscallResult::Ok(value) => Ok(Ok(value)),
                        SyscallResult::Err(value) => Ok(Err(value)),
                    }
                };

                memory_scope(memory, syscall_scope).map_err(ProgramError::from)
            })
        });

        result.map_err(|e| e.into())
    }

    /// Get register value
    ///
    /// Arguments:
    /// - `index`: Register index (0-31).
    ///
    /// Returns:
    /// - 32-bit signed register value.
    fn get_register(&mut self, index: u8) -> PyResult<i32> {
        let result = self
            .interpreter
            .with_interpreter_mut(|interpreter| interpreter.registers.cpu.get(index))
            .map_err(ProgramError::from);

        result.map_err(|e| e.into())
    }

    /// Set register value
    ///
    /// Arguments:
    /// - `index`: Register index (0-31).
    /// - `value`: 32-bit signed value to set.
    fn set_register(&mut self, index: u8, value: i32) -> PyResult<()> {
        let result = self.interpreter.with_interpreter_mut(|interpreter| {
            *interpreter.registers.cpu.get_mut(index)? = value;
            Ok::<(), ProgramError>(())
        });

        result.map_err(|e| e.into())
    }

    /// Get Program Counter
    ///
    /// Returns:
    /// - Current 32-bit program counter (PC) value.
    fn get_pc(&mut self) -> PyResult<u32> {
        let result = self
            .interpreter
            .with_interpreter_mut(|interpreter| interpreter.program_counter);

        Ok(result)
    }

    /// Set Program Counter
    ///
    /// Arguments:
    /// - `pc`: 32-bit program counter (PC) value to set.
    fn set_pc(&mut self, pc: u32) -> PyResult<()> {
        self.interpreter
            .with_interpreter_mut(|interpreter| interpreter.program_counter = pc);
        Ok(())
    }
}

/// Embive Python module
/// 
/// This module provides the Python bindings for the Embive interpreter and transpiler.
#[pymodule]
fn pyembive(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(transpile))?;
    m.add_class::<ProgramState>()?;
    m.add_class::<SyscallResult>()?;
    m.add_class::<Program>()?;

    Ok(())
}
