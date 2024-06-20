import matplotlib.pyplot as plt
import numpy as np

typeA = {'00000', '00001', '00110', '01010', '01011', '01100'}
typeB = {'01000', '01001', '00010'}
typeC = {'00111', '01101', '01110', '00011'}
typeD = {'00100', '00101'}
typeE = {'01111', '10000', '10001', '10010'}
typeF = {'10011'}

reg_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'FLAGS': 0}

Mem_dict = {}
cycle_list = []
mem_list = []

with open("code.txt", "r") as f:
  code_text = f.readlines()

cntr = 0
halt = False


def registerOutput(pc):
  cycle_list.append(cycle)
  mem_list.append(pc)


def flagReset():
  reg_dict['FLAGS'] = 0


def flagClear():
  pass


halt = True
for line in code_text:
  if (len(line) <= 17 and line[0:15] != '0' * 16):
    if line[0:5] == '10011':
      Mem_dict[cntr] = line
    else:
      Mem_dict[cntr] = line[0:-1]
    cntr = cntr + 1

programcntr = 0

# cycle is for the bonus q
cycle = 0
length = len(line)
while programcntr < len(Mem_dict.keys()):

  line = Mem_dict[programcntr]

  if (length <= 17 and line[0:15] != '0' * 16 and halt):

    opcode = line[0:5]

    if opcode in typeA:
      r1 = int(line[7:10], 2)

      r2 = int(line[10:13], 2)

      r3 = int(line[13:16], 2)

      #add
      if (opcode == '00000'):
        reg_dict[r1] = reg_dict[r2] + reg_dict[r3]

        if reg_dict[r1] > 255:
          reg_dict[r1] %= 256
          reg_dict['FLAGS'] = 8
        else:
          flagReset()
      #subtract
      elif (opcode == '00001'):
        reg_dict[r1] = reg_dict[r2] - reg_dict[r3]

        if reg_dict[r1] < 0:
          reg_dict[r1] %= 256
          reg_dict['FLAGS'] = 8
        else:
          flagReset()
      #multiply
      elif (opcode == '00110'):
        reg_dict[r1] = reg_dict[r2] * reg_dict[r3]

        if reg_dict[r1] > 255:
          reg_dict[r1] %= 256
          reg_dict['FLAGS'] = 8
        else:
          flagReset()

      #XOR
      elif (opcode == '01010'):
        reg_dict[r1] = reg_dict[r2] ^ reg_dict[r3]
        flagReset()

      #OR
      elif (opcode == '01011'):
        reg_dict[r1] = reg_dict[r2] | reg_dict[r3]
        flagReset()

      #AND
      elif (opcode == '01100'):
        reg_dict[r1] = reg_dict[r2] & reg_dict[r3]
        flagReset()

      registerOutput(programcntr)

    elif opcode in typeB:
      r1 = int(line[5:8], 2)

      imm = int(line[8:16], 2)

      #rshift
      if (opcode == '01000'):
        reg_dict[r1] = reg_dict[r1] >> imm
        flagReset()

      #lshift
      elif (opcode == '01001'):
        reg_dict[r1] = reg_dict[r1] << imm
        flagReset()

      #mov i
      elif (opcode == '00010'):
        reg_dict[r1] = imm
        flagReset()

      registerOutput(programcntr)

    elif opcode in typeC:
      r1 = int(line[10:13], 2)

      r2 = int(line[13:16], 2)

      if (r1 == 7):
        r1 = 'FLAGS'
      if (r2 == 7):
        r2 = 'FLAGS'

      #move r
      if (opcode == '00011'):
        reg_dict[r1] = reg_dict[r2]
        flagReset()

      #divide
      elif (opcode == '00111'):
        reg_dict[0] = reg_dict[r1] // reg_dict[r2]
        reg_dict[1] = reg_dict[r1] % reg_dict[r2]
        flagReset()

      #invert
      elif (opcode == '01101'):
        print(reg_dict[r1], reg_dict[r2])
        reg_dict[r1] = ~(reg_dict[r2])
        flagReset()

      #compare
      elif (opcode == '01110'):
        if (reg_dict[r1] < reg_dict[r2]):
          reg_dict['FLAGS'] = 4
        elif (reg_dict[r1] > reg_dict[r2]):
          reg_dict['FLAGS'] = 2
        elif (reg_dict[r1] == reg_dict[r2]):
          reg_dict['FLAGS'] = 1

      registerOutput(programcntr)

    elif opcode in typeD:
      r1 = int(line[5:8], 2)

      mem = int(line[8:16], 2)

      if opcode == '00100':
        reg_dict[r1] = Mem_dict[mem]

      elif opcode == '00101':
        Mem_dict[mem] = '00000000' + '{0:08b}'.format(reg_dict[r1])
      cycle_list.append(cycle)
      mem_list.append(mem)

      flagReset()
      registerOutput(programcntr)

    elif opcode in typeE:

      mem = line[8:16]

      #unconditional jump
      if opcode == '01111':
        programcntr = int(mem, 2) - 1

      #if less than jump
      elif opcode == '10000':
        if reg_dict['FLAGS'] == 4:
          programcntr = int(mem, 2) - 1

      #if greater than jump
      elif opcode == '10001':
        if reg_dict['FLAGS'] == 2:
          programcntr = int(mem, 2) - 1

      #if equal jump
      elif opcode == '10010':
        if reg_dict['FLAGS'] == 1:
          programcntr = int(mem, 2) - 1

      flagReset()
      registerOutput(programcntr)

    elif opcode in typeF:
      flagReset()
      registerOutput(programcntr)
      programcntr = 1000
      halt = False

    programcntr = programcntr + 1
    cycle = cycle + 1

lines = 0

x = np.array(cycle_list)
y = np.array(mem_list)

plt.xlabel("number of cycles")
plt.ylabel("Address of memory")
plt.scatter(x, y, color='orange')
plt.show()
