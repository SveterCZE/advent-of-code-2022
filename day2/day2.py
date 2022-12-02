def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.split()
        if temp_line[1] == "X":
            temp_line[1] = "A"
        elif temp_line[1] == "Y":
            temp_line[1] = "B"
        elif temp_line[1] == "Z":
            temp_line[1] = "C"
        instructions.append(temp_line)
    return instructions

def part1(instructions):
    player_score = 0
    for pair in instructions:
        match_score = calculate_score(pair)
        player_score += match_score
    print(player_score)
    return 0

def part2(instructions):
    player_score = 0
    for pair in instructions:
        pair = update_instruction_part2(pair) 
        match_score = calculate_score(pair)
        player_score += match_score
    print(player_score)
    return 0

def calculate_score(pair):
    selection_score = calculate_selection_score(pair)
    match_score = calculate_match_score(pair)
    return selection_score + match_score

def update_instruction_part2(pair):
    # select strategy
    # Of tie, both are set to be equal
    if pair[1] == "B":
        pair[1] = pair[0]

    # Change to winnging strategy
    elif pair[1] == "C":
        if pair[0] == "A":
            pair[1] = "B"
        elif pair[0] == "B":
            pair[1] = "C"
        elif pair[0] == "C":
            pair[1] = "A"

    # Chage to losing strategy
    elif pair[1] == "A":
        if pair[0] == "A":
            pair[1] = "C"
        elif pair[0] == "B":
            pair[1] = "A"
        elif pair[0] == "C":
            pair[1] = "B"
    return pair

def calculate_selection_score(pair):
    if pair[1] == "A":
        return 1
    if pair[1] == "B":
        return 2
    if pair[1] == "C":
        return 3

def calculate_match_score(pair):
    if pair[0] == pair[1]:
        return 3
    # Player 1 plays "Rock"
    if pair[0] == "A":
        if pair[1] == "B":
            return 6
        elif pair[1] == "C":
            return 0
    
    # Player 1 plays "Paper"
    if pair[0] == "B":
        if pair[1] == "A":
            return 0
        elif pair[1] == "C":
            return 6

    # Player 1 plays "Scissors"
    if pair[0] == "C":
        if pair[1] == "A":
            return 6
        elif pair[1] == "B":
            return 0


main()