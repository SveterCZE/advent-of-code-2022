def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    coordinates = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split(",")
        coordinates.append((int(temp_line[0]), int(temp_line[1]), int(temp_line[2])))
    return coordinates

def part1(instructions):
    edge_count = len(instructions) * 6
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            cube_A = instructions[i]
            cube_B = instructions[j]
            if do_cubes_touch(cube_A, cube_B):
                edge_count -= 2
    print(edge_count)

def part2(instructions):
    min_x, min_y, min_z, max_x, max_y, max_z = find_borders(instructions)
    outer_fill = set()
    fill_area(outer_fill, instructions, min_x, min_y, min_z, max_x, max_y, max_z)
    external_area = count_external_area(instructions, outer_fill)
    print(external_area)
    return 0

def count_external_area(instructions, outer_fill):
    area = 0
    for outer_elem in outer_fill:
        for inner_elem in instructions:
            if do_cubes_touch(outer_elem, inner_elem):
                area += 1
    return area

def fill_area(outer_fill, instructions, min_x, min_y, min_z, max_x, max_y, max_z):
    initial_coordinate = (min_x, min_y, min_z)
    list_of_coordinates = []
    list_of_coordinates.append(initial_coordinate)
    while len(list_of_coordinates) != 0:
        checked_coordinate = list_of_coordinates.pop()
        outer_fill.add(checked_coordinate)
        valid_neighbouring_coordinates = generate_valid_neighbours(checked_coordinate, instructions, min_x, min_y, min_z, max_x, max_y, max_z)
        for elem in valid_neighbouring_coordinates:
            if elem not in outer_fill:
                list_of_coordinates.append(elem)
    return 0

def generate_valid_neighbours(checked_coordinate, instructions, min_x, min_y, min_z, max_x, max_y, max_z):
    initial_neighbours = []
    initial_neighbours.append((checked_coordinate[0] + 1, checked_coordinate[1], checked_coordinate[2]))
    initial_neighbours.append((checked_coordinate[0] - 1, checked_coordinate[1], checked_coordinate[2]))
    initial_neighbours.append((checked_coordinate[0], checked_coordinate[1] + 1, checked_coordinate[2]))
    initial_neighbours.append((checked_coordinate[0], checked_coordinate[1] - 1, checked_coordinate[2]))
    initial_neighbours.append((checked_coordinate[0], checked_coordinate[1], checked_coordinate[2] + 1))
    initial_neighbours.append((checked_coordinate[0], checked_coordinate[1], checked_coordinate[2] - 1))
    pass1 = []
    for elem in initial_neighbours:
        if elem not in instructions:
            pass1.append(elem)
    valid_neigbours = []
    for elem in pass1:
        if check_out_of_bounds(elem, min_x, min_y, min_z, max_x, max_y, max_z):
            valid_neigbours.append(elem)
    return valid_neigbours

def find_borders(instructions):
    min_x = 99999999
    min_y = 99999999
    min_z = 99999999
    max_x = -99999999
    max_y = -99999999
    max_z = -99999999
    
    for elem in instructions:
        if elem[0] < min_x:
            min_x = elem[0]
        if elem[0] > max_x:
            max_x = elem[0]
        if elem[1] < min_y:
            min_y = elem[1]
        if elem[1] > max_y:
            max_y = elem[1]
        if elem[2] < min_z:
            min_z = elem[2]
        if elem[2] > max_z:
            max_z = elem[2]
    return min_x - 1, min_y - 1, min_z - 1, max_x + 2, max_y + 2, max_z + 2

def do_cubes_touch(cube_A, cube_B):
    if cube_A[0] == cube_B[0] and cube_A[1] == cube_B[1]:
        if abs(cube_A[2] - cube_B[2]) == 1:
            return True
    if cube_A[0] == cube_B[0] and cube_A[2] == cube_B[2]:
        if abs(cube_A[1] - cube_B[1]) == 1:
            return True
    if cube_A[1] == cube_B[1] and cube_A[2] == cube_B[2]:
        if abs(cube_A[0] - cube_B[0]) == 1:
            return True
    return False

def check_out_of_bounds(checked_coordinate, min_x, min_y, min_z, max_x, max_y, max_z):
    if checked_coordinate[0] < min_x:
        return False
    if checked_coordinate[0] > max_x:
        return False
    if checked_coordinate[1] < min_y:
        return False
    if checked_coordinate[1] > max_y:
        return False
    if checked_coordinate[2] < min_z:
        return False
    if checked_coordinate[2] > max_z:
        return False
    return True

main()