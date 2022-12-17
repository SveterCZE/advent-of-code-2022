def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input()
    part2(instructions)

def get_input():
    coordinates = set()
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split(" -> ")
        temp_line_2 = [x.split(",") for x in temp_line]
        instructions.append(temp_line_2)
    for elem in instructions:
        for i in range(len(elem) - 1):
            pair1 = (int(elem[i][0]), int(elem[i][1]))
            pair2 = (int(elem[i+1][0]), int(elem[i+1][1]))
            if pair1[0] == pair2[0]:
                higher = max(pair1[1], pair2[1])
                lower = min(pair1[1], pair2[1])
                for i in range(lower, higher + 1):
                    coordinates.add((pair1[0], i))
            elif pair1[1] == pair2[1]:
                higher = max(pair1[0], pair2[0])
                lower = min(pair1[0], pair2[0])
                for i in range(lower, higher + 1):
                    coordinates.add((i, pair1[1]))
    return coordinates

def part1(barriers):
    sand_count = 0
    lowest_coordinate = find_lowest_coordinate(barriers)
    while True:
        sand_count += 1
        sand_item_coordinate = (500,0)
        falling_into_abbyss = make_sand_fall(sand_item_coordinate, barriers, lowest_coordinate, True)
        if falling_into_abbyss == True:
            break
    print(sand_count - 1)
    return 0

def make_sand_fall(initial_coordinate, barriers, lowest_coordinate, abbyss_check = True):
    checked_coordinate = (initial_coordinate[0], initial_coordinate[1] + 1)
    # Check if falling into abbyss
    if checked_coordinate[1] > lowest_coordinate and abbyss_check == True:
        return True

    if checked_coordinate not in barriers:
        return make_sand_fall(checked_coordinate, barriers, lowest_coordinate, abbyss_check)

    # if the next possible coordinate is bloocked, check alternative to left
    elif checked_coordinate in barriers:
        left_checked_coordinate = (initial_coordinate[0] - 1, initial_coordinate[1] + 1)
        if left_checked_coordinate not in barriers:
            return make_sand_fall(left_checked_coordinate, barriers, lowest_coordinate, abbyss_check)
        else:
            right_checked_coordinate = (initial_coordinate[0] + 1, initial_coordinate[1] + 1)
            if right_checked_coordinate not in barriers:
                return make_sand_fall(right_checked_coordinate, barriers, lowest_coordinate, abbyss_check)
            else:
                barriers.add(initial_coordinate)
                return False

def find_lowest_coordinate(instructions):
    lowest = 0
    for checked_coordinate in instructions:
        if checked_coordinate[1] > lowest:
            lowest = checked_coordinate[1]
    return lowest

def part2(barriers):
    sand_count = 0
    lowest_coordinate = find_lowest_coordinate(barriers)
    floor_level = lowest_coordinate + 2
    generate_floor(floor_level, barriers)
    while True:
        sand_count += 1
        sand_item_coordinate = (500,0)
        make_sand_fall(sand_item_coordinate, barriers, lowest_coordinate, False)
        if sand_item_coordinate in barriers:
            break
    print(sand_count)

def generate_floor(floor_level, barriers):
    for i in range (-20000, 20000):
        barriers.add((i, floor_level))

main()