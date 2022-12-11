def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split()
        if len(temp_line) == 1:
            instructions.append(temp_line)
        else:
            instructions.append((temp_line[0], int(temp_line[1])))
    return instructions

def part1(instructions):
    X_register_value = 1
    relevant_values = []
    turn_count = 0
    lit_pixels = []
    for elem in instructions:
        if elem[0] == "noop":    
            activate_pixels(lit_pixels, X_register_value, turn_count)
            turn_count += 1
            if is_relevant_turn(turn_count):
                relevant_values.append(X_register_value * turn_count)
        elif elem[0] == "addx":
            
            activate_pixels(lit_pixels, X_register_value, turn_count)
            
            turn_count += 1
            if is_relevant_turn(turn_count):
                relevant_values.append(X_register_value * turn_count)
            
            activate_pixels(lit_pixels, X_register_value, turn_count)
            
            turn_count += 1
            if is_relevant_turn(turn_count):
                relevant_values.append(X_register_value * turn_count)
            X_register_value += elem[1]
    print(sum(relevant_values))
    print_lit_pixels(lit_pixels)
    return 0

def activate_pixels(lit_pixels, X_register_value, turn_count):
    if is_sprite_active(X_register_value, turn_count):
        lit_pixels.append("█")
    else:
        lit_pixels.append(" ")

def part2(instructions):
    pass

def is_relevant_turn(turn_count):
    if (turn_count + 20) % 40 == 0:
        return True
    else:
        return False

def is_sprite_active(X_register_value, turn_count):
    sprite_positions = (X_register_value - 1, X_register_value, X_register_value + 1)
    modified_turn_count = turn_count % 40
    if modified_turn_count in sprite_positions:
        return True
    else:
        return False

def print_lit_pixels(lit_pixels):
    for i in range(len(lit_pixels)):
        print(lit_pixels[i], end ="")
        if (i + 1) % 40 == 0:
            print("")
main()