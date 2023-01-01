def main():
    instructions, monkey_values = get_input()
    part1(instructions, monkey_values)
    instructions, monkey_values = get_input()
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
        iterate_and_calculate_monkey_values(instructions, monkey_values)
        if "root" in monkey_values:
            print(monkey_values["root"])
            break
    return 0

def part2(instructions, monkey_values):
    # Determine the value which constitute a root
    for elem in instructions:
        if elem[0] == "root":
            root_constituent_1 = elem[1]
            root_constituent_2 = elem[3]
    # Remove the value which is to be guessed
    monkey_values.pop("humn")
    max_length_monkeys = len(monkey_values)
    while True:
        iterate_and_calculate_monkey_values(instructions, monkey_values)
        # if no further solutions can be solved, break
        current_length_monkeys = len(monkey_values)
        if current_length_monkeys == max_length_monkeys:
            break
        else:
            max_length_monkeys = current_length_monkeys
    # Find the other root_constituent
    if root_constituent_1 in monkey_values:
        monkey_values[root_constituent_2] = monkey_values[root_constituent_1]
        added_figure = root_constituent_2
    elif root_constituent_2 in monkey_values:
        monkey_values[root_constituent_1] = monkey_values[root_constituent_2]
        added_figure = root_constituent_1
    # Recursively add the remaining figures
    recursive_caluclator(instructions, monkey_values, added_figure)
    print(int(monkey_values["humn"]))
    return 0

def recursive_caluclator(instructions, monkey_values, added_figure):
    # Base case --- humn figure was calculated
    if "humn" in monkey_values:
        return
    # Recursive case --- find the relevant instruction and calculate other figure
    else:
        for checked_instruction in instructions:
            if checked_instruction[0] == added_figure:
                if checked_instruction[1] in monkey_values:
                    missing_figure = checked_instruction[3]
                    missing_figure_pos = 3
                    available_figures_pos = 1
                else:
                    missing_figure = checked_instruction[1]
                    missing_figure_pos = 1
                    available_figures_pos = 3
                if checked_instruction[2] == "+":
                    missing_figure_value = monkey_values[added_figure] - monkey_values[checked_instruction[available_figures_pos]]
                elif checked_instruction[2] == "-":
                    if missing_figure_pos == 1:
                        missing_figure_value = monkey_values[added_figure] + monkey_values[checked_instruction[available_figures_pos]]
                    elif missing_figure_pos == 3:
                        missing_figure_value = monkey_values[checked_instruction[available_figures_pos]] - monkey_values[added_figure]
                elif checked_instruction[2] == "*":
                    missing_figure_value = monkey_values[added_figure] / monkey_values[checked_instruction[available_figures_pos]]
                elif checked_instruction[2] == "/":
                    if missing_figure_pos == 1:
                        missing_figure_value = monkey_values[added_figure] * monkey_values[checked_instruction[available_figures_pos]]
                    elif missing_figure_pos == 3:
                        missing_figure_value = monkey_values[checked_instruction[available_figures_pos]] / monkey_values[added_figure]
                monkey_values[missing_figure] = missing_figure_value
        recursive_caluclator(instructions, monkey_values, missing_figure)

def iterate_and_calculate_monkey_values(instructions, monkey_values):
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

main()