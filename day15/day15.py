def main():
    instructions = get_input()
    part1(instructions, 2000000)
    part2(instructions)

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

def part2(instructions):
    pass

def check_one_coordinate_pair(coordinate_pair, blocked_coordinates, y_coordinate):
    sensor_coordinates = (coordinate_pair[0], coordinate_pair[1])
    beacon_coordinates = (coordinate_pair[2], coordinate_pair[3])
    manhattan_distance = abs(sensor_coordinates[0] - beacon_coordinates[0]) + abs(sensor_coordinates[1] - beacon_coordinates[1])
    distance_to_y_line = abs(sensor_coordinates[1] - y_coordinate)
    side_steps_on_y_line = manhattan_distance - distance_to_y_line
    if side_steps_on_y_line >= 0:
        blocked_coordinates.add(sensor_coordinates[0])
        if side_steps_on_y_line > 0:
            for i in range(sensor_coordinates[0] - side_steps_on_y_line, sensor_coordinates[0]):
                blocked_coordinates.add(i)
            for j in range(sensor_coordinates[0] + 1, sensor_coordinates[0] + side_steps_on_y_line):
                blocked_coordinates.add(j)

main()