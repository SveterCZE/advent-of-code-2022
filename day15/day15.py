def main():
    instructions = get_input()
    part1(instructions, 2000000)
    part2(instructions, 4000000)

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        temp_line = line.strip().split()
        instructions.append((int(temp_line[2][2:-1]), int(temp_line[3][2:-1]), int(temp_line[8][2:-1]), int(temp_line[9][2:])))
    return instructions

def part1(instructions, y_coordinate):
    blocked_coordinates = set()
    for coordinate_pair in instructions:
        check_one_coordinate_pair(coordinate_pair, blocked_coordinates, y_coordinate)
    print(len(blocked_coordinates))
    return 0

def part2(instructions, border):
    coordinate_distance_pairs = calculate_coordinate_distance_pair(instructions)
    for coordinate_distance_pair in coordinate_distance_pairs:
        empty_space = check_edges(coordinate_distance_pair, coordinate_distance_pairs, border)
        if empty_space != False:
            print((empty_space[0] * 4000000) + empty_space[1])
            break
    return 0

def check_edges(checked_coordinate, coordinate_distance_pairs, border):
    # initialise the edge coordinates
    left_coordinate = (checked_coordinate[0][0] - checked_coordinate[1]) - 1, checked_coordinate[0][1]
    right_coordinate = (checked_coordinate[0][0] + checked_coordinate[1]) + 1, checked_coordinate[0][1]
    top_coordinate = checked_coordinate[0][0], (checked_coordinate[0][1] - checked_coordinate[1]) - 1
    bottom_coordinate = checked_coordinate[0][0], (checked_coordinate[0][1] + checked_coordinate[1]) + 1
    
    # left to top
    checked_coordinate = left_coordinate
    while True:
        if checked_coordinate == top_coordinate:
            break
        if is_in_borders(checked_coordinate, border):
            if covered_by_other_sensors(checked_coordinate, coordinate_distance_pairs) == False:
                return checked_coordinate
        checked_coordinate = checked_coordinate[0] + 1, checked_coordinate[1] - 1
    
    # top to right
    checked_coordinate = top_coordinate
    while True:
        if checked_coordinate == right_coordinate:
            break
        if is_in_borders(checked_coordinate, border):
            if covered_by_other_sensors(checked_coordinate, coordinate_distance_pairs) == False:
                return checked_coordinate
        checked_coordinate = checked_coordinate[0] + 1, checked_coordinate[1] + 1

    # right to bottom
    checked_coordinate = right_coordinate
    while True:
        if checked_coordinate == bottom_coordinate:
            break
        if is_in_borders(checked_coordinate, border):
            if covered_by_other_sensors(checked_coordinate, coordinate_distance_pairs) == False:
                return checked_coordinate
        checked_coordinate = checked_coordinate[0] - 1, checked_coordinate[1] + 1

    # bottom to left
    checked_coordinate = bottom_coordinate
    while True:
        if checked_coordinate == left_coordinate:
            break
        if is_in_borders(checked_coordinate, border):
            if covered_by_other_sensors(checked_coordinate, coordinate_distance_pairs) == False:
                return checked_coordinate
        checked_coordinate = checked_coordinate[0] - 1, checked_coordinate[1] - 1
    return False

def is_in_borders(checked_coordinate, border):
    if checked_coordinate[0] < 0 or checked_coordinate[1] < 0 or checked_coordinate[0] > border or checked_coordinate[1] > border:
        return False
    return True
    
def covered_by_other_sensors(checked_coordinate, coordinate_distance_pairs):
    for possible_scanner in coordinate_distance_pairs:
        manhattan_distance = abs(checked_coordinate[0] - possible_scanner[0][0]) + abs(checked_coordinate[1] - possible_scanner[0][1])
        if manhattan_distance <= possible_scanner[1]:
            return True
    return False

def check_one_coordinate_pair(coordinate_pair, blocked_coordinates, y_coordinate):
    sensor_coordinates = (coordinate_pair[0], coordinate_pair[1])
    beacon_coordinates = (coordinate_pair[2], coordinate_pair[3])
    manhattan_distance = abs(sensor_coordinates[0] - beacon_coordinates[0]) + abs(sensor_coordinates[1] - beacon_coordinates[1])
    distance_to_y_line = abs(sensor_coordinates[1] - y_coordinate)
    side_steps_on_y_line = manhattan_distance - distance_to_y_line
    if side_steps_on_y_line >= 0:
        blocked_coordinates = blocked_coordinates.update({*range(sensor_coordinates[0] - side_steps_on_y_line, sensor_coordinates[0] + side_steps_on_y_line)})

def calculate_coordinate_distance_pair(instructions):
    coordinate_distance_pairs = [] 
    for coordinate_pair in instructions:
        sensor_coordinates = (coordinate_pair[0], coordinate_pair[1])
        beacon_coordinates = (coordinate_pair[2], coordinate_pair[3])
        manhattan_distance = abs(sensor_coordinates[0] - beacon_coordinates[0]) + abs(sensor_coordinates[1] - beacon_coordinates[1])
        coordinate_distance_pairs.append((sensor_coordinates, manhattan_distance))
    return coordinate_distance_pairs

main()