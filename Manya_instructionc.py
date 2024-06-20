def convert_binary_to_decimal(binary):
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + int(bit)
    return decimal


def convert_decimal_to_binary(decimal, num_bits):
    binary = format(decimal, 'b').zfill(num_bits)
    return binary


def convert_registers_to_binary(registers):
    binary = ""
    for reg in registers:
        binary += convert_decimal_to_binary(reg, 16)
    return binary


def convert_flags_to_binary(overflow_flag):
    binary = "00000000"
    binary += convert_decimal_to_binary(overflow_flag, 16)
    return binary


machine_code = [
    "0001100000010100",  # Move R2 to R0
    "0001100100111000",  # Move R3 to R1
    "0001100110011010",  # Move R4 to R2
    "0001100000010100",  # Move R2 to R0
    "0011100000000000",  # Divide R0 by R0 (expecting overflow)
    "0111100000000000"  # Halt
]

R0 = 0
R1 = 1
R2 = 2
R3 = 3
R4 = 4
R5 = 5
R6 = 6
FLAGS = 7

registers = [0] * 7
flags = 0
output = ""

for instruction in machine_code:
    opcode = instruction[:5]
    operands = [instruction[5:8], instruction[8:11]]

   
    if opcode == "00011":  # Move
        reg1 = convert_binary_to_decimal(operands[0])
        reg2 = convert_binary_to_decimal(operands[1])
        registers[reg1] = registers[reg2]
    elif opcode == "00111":  # Divide
        reg3 = convert_binary_to_decimal(operands[0])
        reg4 = convert_binary_to_decimal(operands[1])
        if registers[reg4] == 0:
            flags = 1
            registers[R0] = 0
            registers[R1] = 0
        else:
            flags = 0
            registers[R0] = registers[reg3] // registers[reg4]
            registers[R1] = registers[reg3] % registers[reg4]
    elif opcode == "01101":  # Invert
        reg1 = convert_binary_to_decimal(operands[0])
        reg2 = convert_binary_to_decimal(operands[1])
        registers[reg1] = ~registers[reg2]
    elif opcode == "01110":  # Compare
        reg1 = convert_binary_to_decimal(operands[0])
        reg2 = convert_binary_to_decimal(operands[1])
        if registers[reg1] < registers[reg2]:
            flags = -1
        elif registers[reg1] == registers[reg2]:
            flags = 0
        else:
            flags = 1

    pc_binary = convert_decimal_to_binary(len(output) // 135, 7)
    registers_binary = convert_registers_to_binary(registers)
    flags_binary = convert_flags_to_binary(flags)
    output += pc_binary + " " + " ".join([registers_binary[i:i + 16] for i in range(0, 112, 16)]) + " " + flags_binary + "\n"


print(output)
