def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)


def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = [int(x) for x in list(line.strip())]
        instructions.append(temp_line)
    return instructions

def part1(instructions):
    print(count_outer_edge(instructions) + count_interior(instructions))
    return 0

def count_outer_edge(instructions):
    return (len(instructions[0]) * 2) + ((len(instructions[1]) - 2) * 2)

def count_interior(instructions):
    good_trees_interior = 0
    for i in range(1, len(instructions) - 1):
        for j in range(1, len(instructions[0]) - 1):
            if is_good_tree(instructions, (i, j)):
                good_trees_interior += 1
    return good_trees_interior

def is_good_tree(instructions, tree_coordinate):
    checked_tree_height = instructions[tree_coordinate[0]][tree_coordinate[1]]
    left_ok, right_ok, top_ok, down_ok = True, True, True, True
    # Left
    for i in range (0, tree_coordinate[1]):
        if instructions[tree_coordinate[0]][i] >= checked_tree_height:
            left_ok = False
    # Right
    for i in range(tree_coordinate[1] + 1, len(instructions[1])):
        # print("Right check. Checked tree:", checked_tree_height, "right trees:", instructions[tree_coordinate[0]][i])
        if instructions[tree_coordinate[0]][i] >= checked_tree_height:
            right_ok = False
    # Top
    for i in range(0, tree_coordinate[0]):
        # print("Top check. Checked tree:", checked_tree_height, "top trees:", instructions[i][tree_coordinate[1]])
        if instructions[i][tree_coordinate[1]] >= checked_tree_height:
            top_ok = False

    # Down
    for i in range(tree_coordinate[0] + 1, len(instructions[0])):
        if instructions[i][tree_coordinate[1]] >= checked_tree_height:
            down_ok = False

    return left_ok or right_ok or top_ok or down_ok


def part2(instructions):
    best_scenic_score = 0
    for i in range(1, len(instructions) - 1):
        for j in range(1, len(instructions[0]) - 1):
            scenic_score = calculate_scenic_score(instructions, (i, j))
            if scenic_score > best_scenic_score:
                best_scenic_score = scenic_score
    print(best_scenic_score)
    return 0 

def calculate_scenic_score(instructions, tree_coordinate):

    checked_tree_height = instructions[tree_coordinate[0]][tree_coordinate[1]]
    # Left
    left_list = []
    left_score = 0
    for i in range (0, tree_coordinate[1]):
        left_list.append(instructions[tree_coordinate[0]][i])
    left_list.reverse()
    for elem in left_list:
        left_score += 1
        if elem >= checked_tree_height:
            break

    # Right
    right_list = []
    right_score = 0
    for i in range(tree_coordinate[1] + 1, len(instructions[1])):
        right_list.append(instructions[tree_coordinate[0]][i])
    for elem in right_list:
        right_score += 1
        if elem >= checked_tree_height:
            break

    # Top
    top_list = []
    top_score = 0
    for i in range(0, tree_coordinate[0]):
        top_list.append(instructions[i][tree_coordinate[1]])
    top_list.reverse()
    for elem in top_list:
        top_score += 1
        if elem >= checked_tree_height:
            break

    # Down
    down_list = []
    down_score = 0
    for i in range(tree_coordinate[0] + 1, len(instructions[0])):
        down_list.append(instructions[i][tree_coordinate[1]])
    for elem in down_list:
        down_score += 1
        if elem >= checked_tree_height:
            break

    return left_score * right_score * top_score * down_score




main()