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
POP = 0b01000110
PUSH = 0b01000101
SP = 7
RET = 0b00010001
CALL = 0b01010000
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.branchtable = {
            HLT: self.handle_hlt,
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            POP: self.handle_pop,
            PUSH: self.handle_push,
            CALL: self.handle_call,
            RET: self.handle_ret,
            ADD: self.handle_add,
            CMP: self.handle_cmp,
            JMP: self.handle_jmp,
            JEQ: self.handle_jeq,
            JNE: self.handle_jne,
        }

        self.reg[SP] = 0
        self.halted = False

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
        elif op == "MUL":
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

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr


    def handle_ldi(self):
        number = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[number] = value
        self.pc += 3
    
    def handle_prn(self):
        number = self.ram_read(self.pc + 1)
        print(self.reg[number])
        self.pc += 2

    def handle_hlt(self):
        self.halted = True
    
    def handle_mul(self):
        num1 = self.ram_read(self.pc + 1)
        # print(f"num1: {num1}")
        num2 = self.ram_read(self.pc + 2)
        # print(f"num2: {num2}")
        self.alu("MUL", num1, num2)
        self.pc += 3

    def handle_pop(self):
        val = self.ram[self.reg[SP]]
        num = self.ram_read(self.pc + 1)
        self.reg[num] = val
        self.reg[SP] += 1

    def handle_push(self):
        self.reg[SP] -= 1
        num = self.ram_read(self.pc + 1)
        val = self.reg[num]
        self.ram[self.reg[SP]] = val

    def handle_call(self):
        ret_ad = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = ret_ad
        num = self.ram_read(self.pc + 1)
        self.pc = self.reg[num]

    def handle_ret(self):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1

    def handle_add(self):
        self.alu("ADD", self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc += 3

    def handle_cmp(self):
        # Write to register
        operand_a = self.reg[self.ram_read(self.pc + 1)]
        # Value to write
        operand_b = self.reg[self.ram_read(self.pc + 2)]
        # = flag to ls8
        self.Flag = 0
        # comparing operand_a and operand_b
        if operand_a == operand_b:
            self.Flag = self.Flag | 1
        elif operand_a > operand_b:
            self.Flag = self.Flag | 2
        else:
            self.Flag = self.Flag | 4
        self.pc += 3

    def handle_jmp(self):
        # Register tells PC where to jump
        operand_a = self.ram_read(self.pc + 1)
        # Jump to pointed operation
        self.pc = self.reg[operand_a]

    def handle_jeq(self):
        # Register tells PC where to jump
        operand_a = self.ram_read(self.pc + 1)
        # Jump to operation pointed in call
        if self.Flag & 0x1 == 1:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def handle_jne(self):
        # Register tells PC where to jump
        operand_a = self.ram_read(self.pc + 1)
        # Jump to operation pointed in call
        if self.Flag & 0x1 == 0:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.halted != True:
            ir = self.ram[self.pc]
            # print(ir)
            val = ir
            op_count = val >> 6
            ir_length = op_count + 1
            self.branchtable[ir]()

            if ir == 0 or None:
                print(f"Cannot execute {self.pc}")
                sys.exit(1)



            # if ir != 80:
            #     self.pc += ir_length


        

