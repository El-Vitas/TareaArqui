import random


def generate():
    instructions = []
    for i in range(64):
        operation = (random.randint(0, 7))
        inst_A = hex(random.randint(0, 255))[2:].upper()
        inst_B = hex(random.randint(0, 255))[2:].upper()

        inst_A = inst_A if len(inst_A) == 2 else '0' + inst_A
        inst_B = inst_B if len(inst_B) == 2 else '0' + inst_B

        instruction = f"memory[{i}] = 19'h{operation}{inst_A}{inst_B};"
        instructions.append(instruction)
    return instructions


def write_txt(instructions):
    with open("instrucciones.txt", "w") as file:
        for instruction in instructions:
            file.write(instruction + "\n")


instructions = generate()
write_txt(instructions)
print("Archivo creado.")
