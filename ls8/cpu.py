"""CPU functionality."""

import sys

# - [ ] Inventory what is here
# - [ ] Implement the `CPU` constructor
# - [ ] Add RAM functions `ram_read()` and `ram_write()`
# - [ ] Implement the core of `run()`
# - [ ] Implement the `HLT` instruction handler
# - [ ] Add the `LDI` instruction
# - [ ] Add the `PRN` instruction

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1

        except:
            print("can't read file")
            sys.exit(2)

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        running = True
        while running:
            # if self.ram[self.pc] == ldi:
            #     self.reg[int(str(self.ram[self.pc + 1]), 2)] = self.ram[self.pc + 2]
            #     self.pc += 3
            # elif self.ram[self.pc] == PRN:
            #     print(self.reg[int(str(self.ram[self.pc + 1]), 2)])
            #     self.pc += 2
            # elif self.ram[self.pc] == MUL:
            #     self.alu(self.ram[self.pc], self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            #     self.pc += 3
            # elif self.ram[self.pc] == HLT:
            #     self.pc = 0
            #     running = False
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif opcode == MUL:
                self.alu(opcode, operand_a, operand_b)
                self.pc += 3
            elif opcode == HLT:
                sys.exit(0)
            else:
                print(f"Did not work")
                sys.exit(1)

        

