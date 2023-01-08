def main():
    world_map, instructions  = get_input()
    part1(world_map, instructions)
    part2(world_map, instructions)

def get_input():
    world_map = []
    instructions = []
    max_line_len = determine_max_line_len()
    f = open("input.txt", "r")
    instructions_line = False
    for line in f:
        temp_line = line.strip("\n")
        if len(temp_line) == 0:
            instructions_line = True
            continue
        if instructions_line == True:
            last_alpha_position = -1
            for i in range(len(temp_line)):
                if temp_line[i].isalpha():
                    instructions.append(int(temp_line[last_alpha_position + 1:i]))
                    instructions.append(temp_line[i])
                    last_alpha_position = i
            instructions.append(int(temp_line[last_alpha_position + 1:]))
        else:
            list_line = list(temp_line)
            if len(list_line) < max_line_len:
                for i in range(max_line_len - len(list_line)):
                    list_line.append(" ")
            world_map.append(list_line)
    return world_map, instructions

def part1(world_map, instructions):
    coordinate = find_initial_coordinate(world_map)
    direction = "E"
    for movement_instruction in instructions:
        if isinstance(movement_instruction, int):
            coordinate = move_accross_map(direction, movement_instruction, coordinate, world_map)
        else:
            direction = change_movement_direction(direction, movement_instruction)
            print("New direction: ", direction)
    print(coordinate)
    final_result = calculate_final_result(coordinate, direction)
    print(final_result)
    return 0

def part2(world_map, instructions):
    pass

def calculate_final_result(coordinate, direction):
    if direction == "E":
        movement_score = 0
    elif direction == "S":
        movement_score = 1
    elif direction == "W":
        movement_score = 2
    elif direction == "N":
        movement_score = 3
    return (1000 * (coordinate[0] + 1) + 4 * (coordinate[1] + 1) + movement_score)


def move_accross_map(direction, movement_instruction, coordinate, world_map):
    for i in range(movement_instruction):
        next_step_coordinate = make_single_step(direction, coordinate, world_map)
        print("Current coordinate: ", coordinate, "Next coordinate: ", next_step_coordinate)
        if next_step_coordinate == coordinate:
            return coordinate
        else:
            coordinate = next_step_coordinate
    return coordinate

def make_single_step(direction, coordinate, world_map):
    movement_offset = find_movement_offset(direction)
    proposed_new_coordinate = [coordinate[0] + movement_offset[0], coordinate[1] + movement_offset[1]]
    proposed_new_coordinate = check_borders(world_map, proposed_new_coordinate)
    # find the next proposed step, if the next one is empty
    if world_map[proposed_new_coordinate[0]][proposed_new_coordinate[1]] == " ":
        proposed_new_coordinate = find_non_empty_coordinate(proposed_new_coordinate, direction, world_map)
    # The next proposed step is wall
    if world_map[proposed_new_coordinate[0]][proposed_new_coordinate[1]] == "#":
        return coordinate
    else:
        return proposed_new_coordinate

def find_non_empty_coordinate(start_coordinate, direction, world_map):
    movement_offset = find_movement_offset(direction)
    while True:
        proposed_new_coordinate = [start_coordinate[0] + movement_offset[0], start_coordinate[1] + movement_offset[1]]
        proposed_new_coordinate = check_borders(world_map, proposed_new_coordinate)
        if world_map[proposed_new_coordinate[0]][proposed_new_coordinate[1]] != " ":
            return proposed_new_coordinate
        start_coordinate = proposed_new_coordinate

def check_borders(world_map, proposed_new_coordinate):
    if proposed_new_coordinate[0] < 0:
        proposed_new_coordinate[0] = len(world_map) - 1
    if proposed_new_coordinate[1] < 0:
        proposed_new_coordinate[1] = len(world_map[0]) - 1
    if proposed_new_coordinate[0] >= len(world_map):
        proposed_new_coordinate[0] = 0
    if proposed_new_coordinate[1] >= len(world_map[0]):
        proposed_new_coordinate[1] = 0
    return proposed_new_coordinate

def change_movement_direction(direction, movement_instruction):
    if movement_instruction == "L":
        if direction == "W":
            return "S"
        elif direction == "E":
            return "N"
        elif direction == "N":
            return "W"
        elif direction == "S":
            return "E"
    
    elif movement_instruction == "R":
        if direction == "W":
            return "N"
        elif direction == "E":
            return "S"
        elif direction == "N":
            return "E"
        elif direction == "S":
            return "W"

def find_movement_offset(direction):
    if direction == "W":
        return (0, -1)
    elif direction == "E":
        return (0, 1)
    elif direction == "N":
        return (-1, 0)
    elif direction == "S":
        return (1, 0)

def determine_max_line_len():
    max_line_len = 0
    f = open("sample.txt", "r")
    for line in f:
        temp_line = line.strip("\n")
        if len(temp_line) == 0:
            break
        temp_line = line.strip("\n")
        if len(temp_line) > max_line_len:
            max_line_len = len(temp_line)
    return max_line_len

def find_initial_coordinate(world_map):
    for i in range(len(world_map)):
        for j in range(len(world_map[0])):
            if world_map[i][j] == ".":
                return (i,j)

main()