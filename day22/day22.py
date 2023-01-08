import copy

def main():
    world_map, instructions  = get_input()
    part1(world_map, instructions)
    part2(world_map, instructions)

def get_input():
    world_map = []
    instructions = []
    filename = "input.txt"
    max_line_len = determine_max_line_len(filename)
    f = open(filename, "r")
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
            # print("New direction: ", direction)
    # print(coordinate)
    final_result = calculate_final_result(coordinate, direction)
    print(final_result)
    return 0

def part2(world_map, instructions):
    list_of_cubes_sides = split_world_into_cube_sides(world_map)
    direction = "E"
    current_cube = 0
    coordinate = find_initial_coordinate(list_of_cubes_sides[0])
    direction = "E"
    for movement_instruction in instructions:
        if isinstance(movement_instruction, int):
            coordinate, direction, current_cube = move_accross_cube(direction, movement_instruction, coordinate, list_of_cubes_sides, current_cube)
        else:
            direction = change_movement_direction(direction, movement_instruction)
            # print("New direction: ", direction)
    coordinate = map_result_to_full_map(coordinate, current_cube)
    final_result = calculate_final_result(coordinate, direction)
    print(final_result)
    return 0

def move_accross_cube(direction, movement_instruction, coordinate, list_of_cubes_sides, current_cube):
    for i in range(movement_instruction):
        next_step_coordinate, next_step_direction, next_step_current_cube = make_single_step_cube(direction, coordinate, list_of_cubes_sides, current_cube)
        # print("Current coordinate: ", coordinate, "Next coordinate: ", next_step_coordinate)
        if next_step_coordinate == coordinate:
            return coordinate, direction, current_cube
        else:
            coordinate = next_step_coordinate
            current_cube = next_step_current_cube
            direction = next_step_direction
    return coordinate, direction, current_cube

def make_single_step_cube(direction, coordinate, list_of_cubes_sides, current_cube):
    movement_offset = find_movement_offset(direction)
    proposed_new_coordinate = [coordinate[0] + movement_offset[0], coordinate[1] + movement_offset[1]]
    proposed_new_direction = copy.deepcopy(direction)
    proposed_new_cube_side = current_cube
    if is_in_the_cube_side(proposed_new_coordinate) == False:
        proposed_new_coordinate, proposed_new_direction, proposed_new_cube_side = wrap_around_cube(proposed_new_coordinate, direction, current_cube)
    if list_of_cubes_sides[proposed_new_cube_side][proposed_new_coordinate[0]][proposed_new_coordinate[1]] == "#":
        return coordinate, direction, current_cube
    else:
        return proposed_new_coordinate, proposed_new_direction, proposed_new_cube_side

def wrap_around_cube(proposed_new_coordinate, direction, current_cube):
    current_cube += 1
    if current_cube == 1:
        if direction == "N":
            new_direction = "E"
            new_cube_side = 6
            new_coordinate = [proposed_new_coordinate[1], 0]
        elif direction == "E":
            new_direction = "E"
            new_cube_side = 2
            new_coordinate = [proposed_new_coordinate[0], 0]
        elif direction == "S":
            new_direction = "S"
            new_cube_side = 3
            new_coordinate = [0, proposed_new_coordinate[1]]
        elif direction == "W":
            new_direction = "E"
            new_cube_side = 4
            new_coordinate = [49 - proposed_new_coordinate[0], 0]

    elif current_cube == 2:
        if direction == "N":
            new_direction = "N"
            new_cube_side = 6
            new_coordinate = [49, proposed_new_coordinate[1]]
        elif direction == "E":
            new_direction = "W"
            new_cube_side = 5
            new_coordinate = [49 - proposed_new_coordinate[0], 49]
        elif direction == "S":
            new_direction = "W"
            new_cube_side = 3
            new_coordinate = [proposed_new_coordinate[1], 49]
        elif direction == "W":
            new_direction = "W"
            new_cube_side = 1
            new_coordinate = [proposed_new_coordinate[0], 49]

    elif current_cube == 3:
        if direction == "N":
            new_direction = "N"
            new_cube_side = 1
            new_coordinate = [49, proposed_new_coordinate[1]]
        elif direction == "E":
            new_direction = "N"
            new_cube_side = 2
            new_coordinate = [49, proposed_new_coordinate[0]]
        elif direction == "S":
            new_direction = "S"
            new_cube_side = 5
            new_coordinate = [0, proposed_new_coordinate[1]]
        elif direction == "W":
            new_direction = "S"
            new_cube_side = 4
            new_coordinate = [0, proposed_new_coordinate[0]]

    elif current_cube == 4:
        if direction == "N":
            new_direction = "E"
            new_cube_side = 3
            new_coordinate = [proposed_new_coordinate[1], 0]
        elif direction == "E":
            new_direction = "E"
            new_cube_side = 5
            new_coordinate = [proposed_new_coordinate[0], 0]
        elif direction == "S":
            new_direction = "S"
            new_cube_side = 6
            new_coordinate = [0, proposed_new_coordinate[1]]
        elif direction == "W":
            new_direction = "E"
            new_cube_side = 1
            new_coordinate = [49 - proposed_new_coordinate[0], 0]

    elif current_cube == 5:
        if direction == "N":
            new_direction = "N"
            new_cube_side = 3
            new_coordinate = [49, proposed_new_coordinate[1]]
        elif direction == "E":
            new_direction = "W"
            new_cube_side = 2
            new_coordinate = [49 - proposed_new_coordinate[0], 49]
        elif direction == "S":
            new_direction = "W"
            new_cube_side = 6
            new_coordinate = [proposed_new_coordinate[1], 49]
        elif direction == "W":
            new_direction = "W"
            new_cube_side = 4
            new_coordinate = [proposed_new_coordinate[0], 49]

    elif current_cube == 6:
        if direction == "N":
            new_direction = "N"
            new_cube_side = 4
            new_coordinate = [49, proposed_new_coordinate[1]]
        elif direction == "E":
            new_direction = "N"
            new_cube_side = 5
            new_coordinate = [49, proposed_new_coordinate[0]]
        elif direction == "S":
            new_direction = "S"
            new_cube_side = 2
            new_coordinate = [0, proposed_new_coordinate[1]]
        elif direction == "W":
            new_direction = "S"
            new_cube_side = 1
            new_coordinate = [0, proposed_new_coordinate[0]]

    return new_coordinate, new_direction, new_cube_side - 1

def is_in_the_cube_side(proposed_new_coordinate):
    if proposed_new_coordinate[0] < 0:
        return False
    elif proposed_new_coordinate[1] < 0:
        return False
    elif proposed_new_coordinate[0] >= 50:
        return False
    elif proposed_new_coordinate[1] >= 50:
        return False
    return True

def split_world_into_cube_sides(world_map):
    cube_sides = []
    map_height = len(world_map)
    map_width = len(world_map[0])
    # print(map_height, map_width)
    side_dimension = map_height // 4
    for i in range(4):
        for j in range(3):
            start_coordinate = (i * side_dimension, j * side_dimension)
            extracted_cube_side = extract_cube_sides(world_map, start_coordinate, side_dimension)
            cube_sides.append(extracted_cube_side)
    return [cube_sides[1], cube_sides[2], cube_sides[4], cube_sides[6], cube_sides[7], cube_sides[9]]

def extract_cube_sides(world_map, start_coordinate, side_dimension):
    cube_side = []
    for i in range(side_dimension):
        cube_side.append(world_map[start_coordinate[0] + i][start_coordinate[1] : start_coordinate[1] + 50])
    return cube_side

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
        # print("Current coordinate: ", coordinate, "Next coordinate: ", next_step_coordinate)
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

def determine_max_line_len(filename):
    max_line_len = 0
    f = open(filename, "r")
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

def map_result_to_full_map(coordinate, current_cube):
    return (coordinate[0] + 100, coordinate[1])

main()