# A simple example that matches 1:1 the original Rust example.
from pyembive import Program, ProgramState, SyscallResult, transpile

# RISC-V code to be transpiled and executed.
# The default code will execute the syscalls implemented
# bellow, loading values from RAM and adding them.
# Check the available Embive templates for more info.
with open("app.elf", "rb") as f:
    elf = f.read()

# A simple syscall implementation
def syscall_handler(nr, args, memory):
    # Match the syscall number
    if nr == 1:
        # Add two numbers (arg[0] + arg[1])
        return SyscallResult.Ok(args[0] + args[1])
    elif nr == 2:
        # Load from RAM (arg[0])
        return SyscallResult.Ok(int.from_bytes(memory.load(args[0], 4), byteorder='little', signed=True))

    # Not implemented (Error returned to guest)
    return SyscallResult.Err(2)

# Convert RISC-V ELF to Embive binary
data = transpile(elf)

# Create a new program instance with the binary data,
# a memory size of 4096 bytes and instruction limit of 10.
program = Program(data, 4096, 10)

# Run the interpreter, handling all possible states
while True:
    state = program.run()
    if state == ProgramState.Running:
        # Keep running after reaching instruction limit (10)
        pass 
    elif state == ProgramState.Called:
        # Handle syscall if called by guest code (ECALL)
        program.syscall(syscall_handler)
    elif state == ProgramState.Waiting:
        # Interrupt (passing value = 10) if guest is waiting (WFI)
        program.interrupt(10)
    elif state == ProgramState.Halted:
        # Stop if guest code exited (EBREAK)
        break

# Code does "10 + 20" using syscalls (load from ram and add numbers)
# Check the result (Ok(30)) (Registers: A0 = 0, A1 = 30)
assert(program.get_register(10) == 0)
assert(program.get_register(11) == 30)
