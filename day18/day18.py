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
    pass

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

main()