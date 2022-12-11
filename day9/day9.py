def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split()
        instructions.append((temp_line[0], int(temp_line[1])))
    return instructions

def part1(instructions):
    visited_places = set()
    head_coordinate = (0,0)
    tail_coordinate = (0,0)
    visited_places.add(tail_coordinate)
    for elem in instructions:
        head_coordinate, tail_coordinate = make_movement(elem, visited_places, head_coordinate, tail_coordinate)
    print(len(visited_places))
    return 0

def make_movement(movement_instruction, visited_places, head_coordinate, tail_coordinate):
    for i in range(movement_instruction[1]):
        head_coordinate = move_head(head_coordinate, movement_instruction[0])
        is_tail_next = check_tail_next(head_coordinate, tail_coordinate)
        if not is_tail_next:
            tail_coordinate = move_tail(head_coordinate, tail_coordinate)
            visited_places.add(tail_coordinate)
    return head_coordinate, tail_coordinate
        

def move_head(head_coordinate, movement_direction):
    if movement_direction == "R":
        return (head_coordinate[0] + 1, head_coordinate[1])
    elif movement_direction == "L":
        return (head_coordinate[0] - 1, head_coordinate[1])
    elif movement_direction == "U":
        return (head_coordinate[0], head_coordinate[1] + 1)
    elif movement_direction == "D":
        return (head_coordinate[0], head_coordinate[1] - 1)

def check_tail_next(head_coordinate, tail_coordinate):
    if abs(head_coordinate[0] - tail_coordinate[0]) <= 1 and abs(head_coordinate[1] - tail_coordinate[1]) <= 1:
        return True
    else:
        return False

def move_tail(head_coordinate, tail_coordinate):
    # Move across both x and y axis
    if head_coordinate[0] != tail_coordinate[0] and head_coordinate[1] != tail_coordinate[1]:
        potential_solutions = generate_potential_solutions_x_and_y(tail_coordinate)
        for potential_move in potential_solutions:
            if check_tail_next(head_coordinate, potential_move):
                return potential_move
    
    # Move accross x axis
    if head_coordinate[0] != tail_coordinate[0] and head_coordinate[1] == tail_coordinate[1]:
        potential_solutions = generate_potential_solutions_x(tail_coordinate)
        for potential_move in potential_solutions:
            if check_tail_next(head_coordinate, potential_move):
                return potential_move

    # Move accross y axis
    if head_coordinate[0] == tail_coordinate[0] and head_coordinate[1] != tail_coordinate[1]:
        potential_solutions = generate_potential_solutions_y(tail_coordinate)
        for potential_move in potential_solutions:
            if check_tail_next(head_coordinate, potential_move):
                return potential_move


def generate_potential_solutions_x_and_y(tail_coordinate):
    x1 = (tail_coordinate[0] + 1, tail_coordinate[1] + 1)
    x2 = (tail_coordinate[0] + 1, tail_coordinate[1] - 1)
    x3 = (tail_coordinate[0] - 1, tail_coordinate[1] - 1)
    x4 = (tail_coordinate[0] - 1 ,tail_coordinate[1] + 1)
    return[x1, x2, x3, x4]

def generate_potential_solutions_x(tail_coordinate):
    x1 = (tail_coordinate[0] + 1, tail_coordinate[1])
    x2 = (tail_coordinate[0] - 1, tail_coordinate[1])
    return [x1, x2]

def generate_potential_solutions_y(tail_coordinate):
    x1 = (tail_coordinate[0], tail_coordinate[1] + 1)
    x2 = (tail_coordinate[0], tail_coordinate[1] - 1)
    return [x1, x2]

def part2(instructions):
    visited_places = set()
    rope = [(0,0) for x in range(10)]
    visited_places.add(rope[-1])
    for elem in instructions:
        rope = make_full_rope_movement(elem, visited_places, rope)
    print(len(visited_places))
    return 0

def make_full_rope_movement(movement_instruction, visited_places, rope):
    for i in range(movement_instruction[1]):
        new_rope = []
        # Move head
        new_head_coordinate = move_head(rope[0], movement_instruction[0])
        new_rope.append(new_head_coordinate)
        # Move each other part of the tail
        for j in range(1,10):
            # Check if the next knot on the rope is next to the previously moved knot
            is_knot_next = check_tail_next(new_rope[j-1], rope[j])
            if not is_knot_next:
                new_knot_coordinate = move_tail(new_rope[j-1], rope[j])
                new_rope.append(new_knot_coordinate)
            else:
                new_rope.append(rope[j])
        visited_places.add(new_rope[-1])
        rope = new_rope
    return rope

main()
