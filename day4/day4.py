def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)


def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        pair1, pair2 = line.strip().split(",")[0].split("-"), line.strip().split(",")[1].split("-") 
        instructions.append([pair1, pair2])
    return instructions

def part1(instructions):
    ovelap_counter = 0
    for elem in instructions:
        if overlaps(elem):
            ovelap_counter += 1
    print(ovelap_counter)
    return 0

def overlaps(checked_pair):
    # Alternative 1 - first fully contains the second
    if int(checked_pair[0][0]) <= int(checked_pair[1][0]) and int(checked_pair[0][1]) >= int(checked_pair[1][1]):
        return True
    # Alternative 2 - second fully contains the first
    elif int(checked_pair[1][0]) <=  int(checked_pair[0][0]) and int(checked_pair[1][1]) >= int(checked_pair[0][1]):
        return True
    else:
        return False

def part2(instructions):
    ovelap_counter = 0
    for elem in instructions:
        if overlaps_p2(elem):
            ovelap_counter += 1
    print(ovelap_counter)
    return 0

def overlaps_p2(checked_pair):
    if int(checked_pair[0][0]) >= int(checked_pair[1][0]) and int(checked_pair[0][0]) <= int(checked_pair[1][1]):
        return True
    elif int(checked_pair[0][1]) >= int(checked_pair[1][0]) and int(checked_pair[0][1]) <= int(checked_pair[1][1]):
        return True
    elif int(checked_pair[1][0]) >= int(checked_pair[0][0]) and int(checked_pair[1][0]) <= int(checked_pair[0][1]):
        return True
    elif int(checked_pair[1][1]) >= int(checked_pair[0][0]) and int(checked_pair[1][1]) <= int(checked_pair[0][1]):
        return True
    else:
        return False

main()