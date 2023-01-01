def main():
    instructions, monkey_values = get_input()
    part1(instructions, monkey_values)
    part2(instructions, monkey_values)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    monkey_values = {}
    instructions = []
    for line in f:
        temp_line = line.strip().split()
        if len(temp_line) == 2:
            monkey_values[temp_line[0][:-1]] = int(temp_line[1])
        else:
            instructions.append((temp_line[0][:-1], temp_line[1], temp_line[2], temp_line[3]))
    return instructions, monkey_values

def part1(instructions, monkey_values):
    while True:
        for checked_instruction in instructions:
            if checked_instruction[1] in monkey_values and checked_instruction[3] in monkey_values:
                if checked_instruction[2] == "+":
                    monkey_values[checked_instruction[0]] = monkey_values[checked_instruction[1]] + monkey_values[checked_instruction[3]]
                elif checked_instruction[2] == "-":
                    monkey_values[checked_instruction[0]] = monkey_values[checked_instruction[1]] - monkey_values[checked_instruction[3]]
                elif checked_instruction[2] == "*":
                    monkey_values[checked_instruction[0]] = monkey_values[checked_instruction[1]] * monkey_values[checked_instruction[3]]
                elif checked_instruction[2] == "/":
                    monkey_values[checked_instruction[0]] = monkey_values[checked_instruction[1]] // monkey_values[checked_instruction[3]]
        if "root" in monkey_values:
            print(monkey_values["root"])
            break
    return 0

def part2(instructions, monkey_values):
    pass

main()