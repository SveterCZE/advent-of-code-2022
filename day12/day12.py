def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input()
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_list = list(line.strip())
        instructions.append(temp_list)
    return instructions

def part1(instructions):
    start_coord = find_coord(instructions, "S")
    target_coord = find_coord(instructions, "E")
    instructions[target_coord[0]][target_coord[1]] = "z"
    instructions[start_coord[0]][start_coord[1]] = "a"
    currently_explored_coordinates = set()
    currently_explored_coordinates.add(start_coord)
    visited_coordinates = set()
    possible_target_coordinates = set()
    possible_target_coordinates.add(target_coord)
    final_result = go_deeper(instructions, currently_explored_coordinates, visited_coordinates, possible_target_coordinates, 1)
    print(final_result)
    return 0

def part2(instructions):
    old_start_coord = find_coord(instructions, "S")
    instructions[old_start_coord[0]][old_start_coord[1]] = "a"
    start_coord = find_coord(instructions, "E")
    instructions[start_coord[0]][start_coord[1]] = "z"
    possible_target_coordinates = find_possible_target_coordinates(instructions)
    currently_explored_coordinates = set()
    currently_explored_coordinates.add(start_coord)
    visited_coordinates = set()
    final_result = go_deeper(instructions, currently_explored_coordinates, visited_coordinates, possible_target_coordinates, 2)
    print(final_result)
    return 0

def go_deeper(instructions, currently_explored_coordinates, visited_coordinates, possible_target_coordinates, part):
    step_count = 0
    while True:
        for elem in possible_target_coordinates:
            if elem in currently_explored_coordinates:
                return step_count
        future_explored_coordinates = set()
        for checked_coordinate in currently_explored_coordinates:
            # Find valid neighbouring tiles (i.e. they are on the board)
            valid_neighbouring_coordinates = find_valid_neighbouring_coordinates(checked_coordinate, instructions)
            # Find steps which are not steep
            possible_steps = find_possible_steps(checked_coordinate, valid_neighbouring_coordinates, instructions, part)
            for possible_step in possible_steps:
                if possible_step not in visited_coordinates:
                    future_explored_coordinates.add(possible_step)
            # mark current as visited
            visited_coordinates.add(checked_coordinate)
        currently_explored_coordinates = future_explored_coordinates
        step_count += 1

def find_valid_neighbouring_coordinates(checked_coordinate, instructions):
    A = (checked_coordinate[0] + 1, checked_coordinate[1])
    B = (checked_coordinate[0] - 1, checked_coordinate[1])
    C = (checked_coordinate[0], checked_coordinate[1] + 1)
    D = (checked_coordinate[0], checked_coordinate[1] - 1)
    temp_list = [A, B, C, D]
    valid_list = []
    for elem in temp_list:
        if elem[0] < 0 or elem[1] < 0:
            continue
        if elem[0] >= len(instructions) or elem[1] >= len(instructions[1]):
            continue
        valid_list.append(elem)
    return valid_list

def find_possible_steps(checked_coordinate, valid_neighbouring_coordinates, instructions, part):
    possible_steps = []
    checked_coordinate_value = instructions[checked_coordinate[0]][checked_coordinate[1]]
    for neighbouring_coordinate in valid_neighbouring_coordinates:
        neighbour_value = instructions[neighbouring_coordinate[0]][neighbouring_coordinate[1]]
        if part == 1:
            if ord(neighbour_value) - ord(checked_coordinate_value) <= 1:
                possible_steps.append(neighbouring_coordinate)
        if part == 2:
            if ord(checked_coordinate_value) - ord(neighbour_value) <= 1:
                possible_steps.append(neighbouring_coordinate)
    return possible_steps

def find_coord(instructions, target_sign):
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == target_sign:
                return (i,j)

def find_possible_target_coordinates(instructions):
    possible_targets = set()
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == "a":
                possible_targets.add((i,j))
    return possible_targets

main()