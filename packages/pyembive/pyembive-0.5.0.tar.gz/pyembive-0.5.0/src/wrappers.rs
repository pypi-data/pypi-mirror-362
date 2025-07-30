//! Wrapper module for Embive interpreter and memory.
use embive::interpreter::{
    memory::{Memory, SliceMemory},
    Interpreter,
};
use ouroboros::self_referencing;
use pyo3::prelude::*;

#[self_referencing]
struct MemoryInner {
    code: Vec<u8>,
    ram: Vec<u8>,
    #[borrows(code, mut ram)]
    #[not_covariant]
    memory: SliceMemory<'this>,
}

#[pyclass]
pub struct MemoryWrapper(MemoryInner);

impl MemoryWrapper {
    pub fn new(code: Vec<u8>, ram_size: usize) -> Self {
        let ram = vec![0; ram_size];
        let memory = MemoryInner::new(code, ram, |code, ram| SliceMemory::new(code, ram));
        MemoryWrapper(memory)
    }
}

impl Memory for MemoryWrapper {
    fn load(&mut self, address: u32, len: u32) -> Result<&[u8], embive::interpreter::Error> {
        self.0.with_memory_mut(|memory| memory.load(address, len))
    }

    fn store(&mut self, address: u32, data: &[u8]) -> Result<(), embive::interpreter::Error> {
        self.0.with_memory_mut(|memory| memory.store(address, data))
    }
}

#[self_referencing]
struct InterpreterInner {
    memory: MemoryWrapper,
    #[borrows(mut memory)]
    #[not_covariant]
    interpreter: Interpreter<'this, MemoryWrapper>,
}

pub struct InterpreterWrapper(InterpreterInner);

impl InterpreterWrapper {
    pub fn new(memory: MemoryWrapper, instruction_limit: u32) -> Self {
        let interpreter = InterpreterInner::new(memory, |memory| {
            Interpreter::new(
                memory,
                instruction_limit,
            )
        });
        InterpreterWrapper(interpreter)
    }

    pub fn with_interpreter_mut<F, R>(&mut self, f: F) -> R
    where
        F: FnOnce(&mut Interpreter<'_, MemoryWrapper>) -> R,
    {
        self.0.with_interpreter_mut(f)
    }
}
