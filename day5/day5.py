from copy import deepcopy

def main():
    initial_containers_stack, instructions = get_input()
    part1(deepcopy(initial_containers_stack), instructions)
    part2(deepcopy(initial_containers_stack), instructions)

def get_input():
    initial_containers_stack = []
    instructions = []
    line_counter = 0
    containers_built = False
    f = open("input.txt", "r")
    for line in f:
        # Determine number of stacks
        if line_counter == 0:
            for i in range(len(list(line.replace(" ", ".").strip())[1::4])):
                initial_containers_stack.append([])
        # Built individual stacks
        if containers_built == False:
            reformatted_list = list(line.replace(" ", ".").strip())[1::4]
            if len(reformatted_list) == 0:
                containers_built = True
            else:
                if reformatted_list[0].isnumeric() == False:
                    for i in range(len(reformatted_list)):
                        if reformatted_list[i] != ".":
                            initial_containers_stack[i].append(reformatted_list[i])
        # Parse moving instructions
        # 0 - Number of moved crates, 1 - Origin, 2 - Destination
        else:
            split_line = line.split()
            instructions.append((int(split_line[1]), int(split_line[3]) - 1, int(split_line[5]) - 1))
        line_counter += 1
    
    # Invert the stacks
    for elem in initial_containers_stack:
        elem.reverse()
    return initial_containers_stack, instructions

def part1(containers_stack, instructions):
    for instruction in instructions:
        make_movement_p1(containers_stack, instruction)
    final_result = find_final_result(containers_stack)
    print(final_result)
    return 0

def part2(containers_stack, instructions):
    for instruction in instructions:
        make_movement_p2(containers_stack, instruction)
    final_result = find_final_result(containers_stack)
    print(final_result)
    return 0

def make_movement_p1(containers_stack, instruction):
    for i in range(instruction[0]):
        containers_stack[instruction[2]].append(containers_stack[instruction[1]].pop())

def make_movement_p2(containers_stack, instruction):
    temp_stack = []
    for i in range(instruction[0]):
        temp_stack.append(containers_stack[instruction[1]].pop())
    temp_stack.reverse()
    for elem in temp_stack:
        containers_stack[instruction[2]].append(elem)

def find_final_result(containers_stack):
    final_result = ""
    for elem in containers_stack:
        final_result += elem[-1]
    return final_result

main()