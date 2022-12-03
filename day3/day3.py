def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input_p2()
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        line_len_half = int(len(line.strip())/2)
        instructions.append([(line.strip()[:line_len_half]), (line.strip()[line_len_half:])])
    return instructions

def get_input_p2():
    instructions = []
    f = open("input.txt", "r")
    triplet = []
    for line in f:
        if len(triplet) == 3:
            instructions.append(triplet)
            triplet = []
            triplet.append(line.strip())
        else:
            triplet.append(line.strip())
    instructions.append(triplet)
    return instructions

def part1(instructions):
    all_matches = []
    for pair in instructions:
        pair_matches = find_pair_matches(pair)
        for elem in pair_matches:
            all_matches.append(elem)
    overlap_values = count_overlap_values(all_matches)
    print(overlap_values)
    return 0

def part2(instructions):
    matching_values = 0
    for triplet in instructions:
        triplet_overlap = set()
        for elem in triplet[0]:
            if elem in triplet[1] and elem in triplet[2]:
                triplet_overlap.add(elem)
        matching_values += count_overlap_values(triplet_overlap)
    print(matching_values)
    return 0

def find_pair_matches(pair):
    pair_matches = set()
    for elem in pair[0]:
        if elem in pair[1]:
            pair_matches.add(elem)
    return pair_matches

def count_overlap_values(all_matches):
    overlap_values = 0
    for elem in all_matches:
        if elem.islower():
            overlap_values += ord(elem) - 96
        else:
            overlap_values += ord(elem) - 38
    return overlap_values

main()

