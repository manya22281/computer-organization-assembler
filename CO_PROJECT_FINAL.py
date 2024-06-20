import sys
with open("code.txt", "r") as f:
  code_text = f.readlines()
#sys.stdin = code_text

# Dividing the instructions into various types
typeA = {'add': '00000','sub': '00001','mul': '00110','xor': '01010','or': '01011','and': '01100'}

typeB = {'rs': '01000', 'ls': '01001', 'mov_i': '00010'}

typeC = {'div': '00111', 'not': '01101', 'cmp': '01110', 'mov_r': '00011'}

typeD = {'ld': '00100', 'st': '00101'}

typeE = {'jmp': '01111', 'jlt': '10000', 'jgt': '10001', 'je': '10010'}

typeF = {'hlt': '10011'}

instructions = [
  'add', 'sub', 'mul', 'xor', 'or', 'and', 'rs', 'ls', 'mov', 'div', 'not',
  'cmp', 'ld', 'st', 'jmp', 'jlt', 'jgt', 'je', 'hlt', 'var'
]

register = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']

bin_rep_reg = {
  "R0": ["000", 0],
  "R1": ["001", 0],
  "R2": ["010", 0],
  "R3": ["011", 0],
  "R4": ["100", 0],
  "R5": ["101", 0],
  "R6": ["110", 0],
  "R7": ["111", 0]
}

var_dict = {}

labels = {}

line_dict = {}

code_line = []

bin_file = []

def pre_type():
  var_temp = []

  address = 0
  linenumber = 0
  halt = False
  variable_end = False

  for line in code_text:
    print(line)
    linenumber += 1

    if line == "\n":
      continue

    wrds = line.split()
    if halt == True:
      print(
        str(linenumber) +
        ": Syntax Error: hlt instuction must be given in the end.")
      quit()

    if variable_end == True and wrds[0] == "var":
      print(
        str(linenumber) +
        ": Syntax Error: All variables must be declared at the beginning")
      quit()

    if wrds[0] == "var":
      if len(wrds) != 2:
        print(str(linenumber) + ": Syntax Error: Illegal instruction")
        quit()

      for i in wrds[1]:
        if i.isalnum() == False and i != '_':
          print(str(linenumber) + ": Syntax Error: Illegal variable name")
          quit()

      if wrds[1] in var_temp:
        print(
          str(linenumber) +
          ": Syntax Error: 2 or more variables cannot have the same name.")
        quit()

      elif wrds[1] in labels.keys():
        print(
          str(linenumber) +
          ": Syntax Error: Variables and labels can't have the same name.")
        quit()

      elif wrds[1] in instructions:
        print(
          str(linenumber) +
          ": Syntax Error: Mnemonic of the instructions cannot be used as variables"
        )
        quit()

      else:
        var_temp.append(wrds[1])

    elif wrds[0][-1] == ":":
      variable_end = True

      for i in wrds[0][:-1]:
        if i.isalnum() == False and i != '_':
          print(str(linenumber) + ": Syntax Error: Illegal variable name")
          quit()

      if wrds[0][:-1] in var_temp:
        print(
          str(linenumber) +
          ": Syntax Error: Variables and labels can't have the same name.")
        quit()

      elif wrds[0][:-1] in labels.keys():
        print(
          str(linenumber) +
          ": Syntax Error: 2 or more labels cannot have the same name.")
        quit()

      elif wrds[0][:-1] in instructions:
        print(
          str(linenumber) +
          ": Syntax Error: Mnemonic of the instructions cannot be used as labels"
        )
        quit()

      else:
        labels[wrds[0][:-1]] = address
        if (line[-1] == "\n"):
          line_dict[address] = line[len(wrds[0]) + 1:-1]
        else:
          line_dict[address] = line[len(wrds[0]) + 1:]

      if len(wrds) > 1 and wrds[1] == 'hlt':
        variable_end = True
        halt = True

      address += 1

    else:
      if wrds[0] == "hlt":
        variable_end = True
        halt = True

      variable_end = True
      if (line[-1] == "\n"):
        line_dict[address] = line[:-1]
      else:
        line_dict[address] = line

      address += 1

    if wrds[0] != "var":
      code_line.append(linenumber)

  if halt == False:
    print(
      str(linenumber) + ": Syntax Error: The last instruction should be hlt.")
    quit()

  for v in var_temp:
    var_dict[v] = [address, 0]
    address += 1

  if (address > 257):
    print("Error: Number of instructions exceed 256")
    quit()


def type_A(instructions, wrds):
  op = typeA[instructions]
  if ((wrds[1][0] == 'R' and wrds[2][0] == 'R' and wrds[3][0] == 'R') == 0):
    print(
      str(code_line[a]) +
      ": Invalid Syntax: Type Instruction cannot be interpretted")
    sys.exit()
  r1 = int(wrds[1][1])
  bin_rep_reg_r1 = '{0:03b}'.format(r1)

  r2 = int(wrds[2][1])
  bin_rep_reg_r2 = '{0:03b}'.format(r2)

  r3 = int(wrds[3][1])
  bin_rep_reg_r3 = '{0:03b}'.format(r3)

  code = op + '00' + bin_rep_reg_r1 + bin_rep_reg_r2 + bin_rep_reg_r3
  bin_file.append(code)


def type_B(instructions, wrds):
  op = typeB[instructions]

  if ((wrds[1][0] == 'R' and wrds[1][1].isdecimal() and wrds[2][0] == '$'
       and wrds[2][1:].isdecimal()) == 0):
    print(
      str(code_line[a]) +
      ': Invalid syntax: Type B instruction cannot be interpreted in this way')
    quit()

  
  if wrds[2][0] == '$':
    immediate = int(wrds[2][1:])
    if immediate < 0 or immediate > 255:
      print(str(code_line[a]) + ": Immediate value out of bounds (0 -> 255)")
      quit()

  r1 = int(wrds[1][1])
  bin_r1 = '{0:03b}'.format(r1)

  imm = int(wrds[2][1:])
  bin_imm = '{0:08b}'.format(imm)

  code = op + bin_r1 + bin_imm

  bin_file.append(code)


def type_C(instructions, wrds):
  op = typeC[instructions]
  if wrds[1] == 'FLAGS':
    print(
      str(code_line[a]) +
      ': Invalid syntax: Type C instruction cannot be interpreted in this way')
    quit()

  if ((wrds[1][0] == 'R' and wrds[1][1].isdecimal() and wrds[2][0] == 'R'
       and (wrds[2][1].isdecimal()) == 0 and wrds[2] != 'FLAGS')):
    print(
      str(code_line[a]) +
      ': Invalid syntax: Type C instruction cannot be interpreted in this way')
    quit()

  r1 = int(wrds[1][1])
  bin_r1 = '{0:03b}'.format(r1)

  if wrds[2] == 'FLAGS':
    r2 = 'FLAGS'

    bin_r2 = '111'

  else:
    r2 = int(wrds[2][1])
    bin_r2 = '{0:03b}'.format(r2)

  code = op + '00000' + bin_r1 + bin_r2

  bin_file.append(code)


def type_D(instructions, wrds):
  op = typeD[instructions]

  if ((wrds[1][0] == 'R' and wrds[1][1].isdecimal()) == 0):
    print(
      str(code_line[a]) +
      ': Invalid syntax: Type D instruction cannot be interpreted in this way')
    quit()

  if (wrds[2] in labels.keys()):
    print(
      str(code_line[a]) +
      ': Syntax Error: Labels cannot be used as variables.')
    quit()

  if (wrds[2] not in var_dict.keys()):
    print(str(code_line[a]) + ': Variable ' + wrds[2] + ' is not defined')
    quit()

  r1 = int(wrds[1][1])
  bin_r1 = '{0:03b}'.format(r1)

  bin_mem = '{0:08b}'.format(var_dict[wrds[2]][0])

  code = op + bin_r1 + bin_mem

  bin_file.append(code)


def type_E(instructions, wrds):
  op = typeE[instructions]

  if (wrds[1] in var_dict.keys()):
    print(
      str(code_line[a]) +
      ': Syntax Error: Variables cannot be used as labels.')
    quit()

  if ((wrds[1] in labels.keys()) == 0):
    print(
      str(code_line[a]) + ': Syntax Error: The label ' + wrds[1] +
      ' is not defined.')
    quit()

  jmploc = labels[wrds[1]]

  bin_mem = '{0:08b}'.format(jmploc)

  code = op + '000' + bin_mem
  bin_file.append(code)


def type_F(instructions):
  op = typeF[instructions]
  code = op + '0' * 11
  bin_file.append(code)


pre_type()

for a in range(len(line_dict.keys())):
  wrds = line_dict[a].split()
  if len(wrds) == 0:
    print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
    quit()

  if wrds[0] in typeA:
    if len(wrds) != 4:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()
    if wrds[1] == "FLAGS" or wrds[2] == "FLAGS" or wrds[3] == "FLAGS":
      print(
        str(code_line[a]) + ": Syntax Error: Illegal use of FLAGS register")
      quit()

    if wrds[1] not in register or wrds[2] not in register or wrds[
        3] not in register:
      print(
        str(code_line[a]) + ": Syntax Error: Register name does not exist.")
      quit()

    instructions = wrds[0]
    type_A(instructions, wrds)

  elif wrds[0] in typeB:
    if len(wrds) != 3:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()

    if wrds[1] == "FLAGS":
      print(
        str(code_line[a]) + ": Syntax Error: Illegal use of FLAGS register")
      quit()

    if wrds[1] not in register:
      print(
        str(code_line[a]) + ": Syntax Error: Register name does not exist.")
      quit()

    instructions = wrds[0]
    type_B(instructions, wrds)

  elif wrds[0] in typeC:
    if len(wrds) != 3:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()

    if wrds[1] == "FLAGS" or wrds[2] == "FLAGS":
      print(
        str(code_line[a]) + ": Syntax Error: Illegal use of FLAGS register")
      quit()

    if wrds[1] not in register or wrds[2] not in register:
      print(
        str(code_line[a]) + ": Syntax Error: Register name does not exist.")
      quit()

    instructions = wrds[0]
    type_C(instructions, wrds)

  elif wrds[0] in typeD:
    if len(wrds) != 3:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()

    if wrds[1] == "FLAGS":
      print(
        str(code_line[a]) + ": Syntax Error: Illegal use of FLAGS register")
      quit()

    if wrds[1] not in register:
      print(
        str(code_line[a]) + ": Syntax Error: Register name does not exist.")
      quit()

    instructions = wrds[0]
    type_D(instructions, wrds)

  elif wrds[0] in typeE:
    if len(wrds) != 2:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()

    instructions = wrds[0]
    a = type_E(instructions, wrds)

  elif wrds[0] in typeF:
    if len(wrds) != 1:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()
    instructions = wrds[0]
    a = type_F(instructions)

  elif wrds[0] == 'mov':
    if len(wrds) != 3:
      print(str(code_line[a]) + ": Syntax Error: Illegal instruction")
      quit()

    if wrds[2][0] == '$':
      if wrds[1] not in register:
        print(
          str(code_line[a]) + ": Syntax Error: Register name does not exist.")
        quit()

      instructions = 'mov_i'
      type_B(instructions, wrds)

    else:
      if (wrds[1] not in register
          and wrds[1] != "FLAGS") or (wrds[2] not in register
                                      and wrds[2] != "FLAGS"):
        print(
          str(code_line[a]) + ": Syntax Error: Register name does not exist.")
        quit()
      instructions = 'mov_r'
      type_C(instructions, wrds)
  else:
    print(str(code_line[a]) + ": " + wrds[0] + ': ' + "Invalid instruction!!")
    quit()

print(*bin_file, sep='\n')

#-----------------------END-------------------------------------
# CONTRIBUTIONS:

# Ayushman(2022128):1.type E and F function
#                   2. error handling
#                   3. flags
#                   4. debug

# Aryaan Bazaz(2022108):1.type A function
#                       2.flags
#                       3.Testing

# Dhruv Verma():1. type B and D functions
                
# Manya Aggarwal():1. type C function
#                  2. Testing

#---------------------------------------------------------------

