def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input()
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions):
    dwarf_locations = set()
    list_of_strategies = [consider_north_route, consider_south_route, consider_west_route, consider_east_route]
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == "#":
                dwarf_locations.add((i,j))
    for i in range(10):
        # Move dwarfs
        dwarf_locations = move_dwarfs(dwarf_locations, list_of_strategies)
        # Move strategies
        moved_strategy = list_of_strategies.pop(0)
        list_of_strategies.append(moved_strategy)
    empty_spaces = count_empty_spaces(dwarf_locations)
    print(empty_spaces)
    return 0

def part2(instructions):
    dwarf_locations = set()
    list_of_strategies = [consider_north_route, consider_south_route, consider_west_route, consider_east_route]
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == "#":
                dwarf_locations.add((i,j))
    round_counter = 0
    while True:
        new_dwarf_locations = move_dwarfs(dwarf_locations, list_of_strategies)
        moved_strategy = list_of_strategies.pop(0)
        list_of_strategies.append(moved_strategy)
        round_counter += 1
        if new_dwarf_locations == dwarf_locations:
            break
        else: 
            dwarf_locations = new_dwarf_locations
    print(round_counter)
    return 0

def move_dwarfs(dwarf_locations, list_of_strategies):
    proposed_moves = {}
    # PART 1 -- Selected proposed moves
    for checked_dwarf in dwarf_locations:
        neighbouring_tiles = generate_neighbouring_coordinates(checked_dwarf)
        # Check if no other dwarfs are in the neighbouring locations
        if no_neighbouring_dwarfs(dwarf_locations, neighbouring_tiles):
            proposed_moves[checked_dwarf] = [checked_dwarf]
        else:
            movement_proposed_by_strategy = strategy_valid_movement(list_of_strategies, dwarf_locations, neighbouring_tiles)
            # If movement pursuant to one of the strategies is valid, propose it
            if movement_proposed_by_strategy != None:
                add_new_proposed_destination(proposed_moves, movement_proposed_by_strategy, checked_dwarf)
            # If no movemement pursuant to strategies is valid, propose to stay
            else:
                add_new_proposed_destination(proposed_moves, checked_dwarf, checked_dwarf)
    
    # PART 2 -- Remove possible conflicting moves
    permitted_moves = set()
    for key, value in proposed_moves.items():
        if len(value) == 1:
            permitted_moves.add(key)
        else:
            for elem in value:
                permitted_moves.add(elem)
    return permitted_moves

def count_empty_spaces(dwarf_locations):
    min_i = 99999999
    max_i = -99999999
    min_j = 99999999
    max_j = -99999999
    for checked_dwarf in dwarf_locations:
        if checked_dwarf[0] < min_i:
            min_i = checked_dwarf[0]
        if checked_dwarf[0] > max_i:
            max_i = checked_dwarf[0]
        if checked_dwarf[1] < min_j:
            min_j = checked_dwarf[1]
        if checked_dwarf[1] > max_j:
            max_j = checked_dwarf[1]
    empty_space_counter = 0
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            if (i,j) not in dwarf_locations:
                empty_space_counter += 1
    return empty_space_counter


def strategy_valid_movement(list_of_strategies, dwarf_locations, neighbouring_tiles):
    for checked_strategy in list_of_strategies:
        proposed_movement = checked_strategy(dwarf_locations, neighbouring_tiles)
        if proposed_movement != None:
            return proposed_movement
    return None

def add_new_proposed_destination(proposed_moves, currently_proposed_move, checked_dwarf):
    if currently_proposed_move not in proposed_moves:
        proposed_moves[currently_proposed_move] = [checked_dwarf]
    else:
        proposed_moves[currently_proposed_move].append(checked_dwarf)

def no_neighbouring_dwarfs(dwarf_locations, neighbouring_tiles):
    for key, value in neighbouring_tiles.items():
        if value in dwarf_locations:
            return False
    return True

def consider_north_route(dwarf_locations, neighbouring_tiles):
    if neighbouring_tiles["N"] not in dwarf_locations and neighbouring_tiles["NE"] not in dwarf_locations and neighbouring_tiles["NW"] not in dwarf_locations:
        return neighbouring_tiles["N"]
    else:
        return None

def consider_south_route(dwarf_locations, neighbouring_tiles):
    if neighbouring_tiles["S"] not in dwarf_locations and neighbouring_tiles["SE"] not in dwarf_locations and neighbouring_tiles["SW"] not in dwarf_locations:
        return neighbouring_tiles["S"]
    else:
        return None

def consider_west_route(dwarf_locations, neighbouring_tiles):
    if neighbouring_tiles["W"] not in dwarf_locations and neighbouring_tiles["NW"] not in dwarf_locations and neighbouring_tiles["SW"] not in dwarf_locations:
        return neighbouring_tiles["W"]
    else:
        return None

def consider_east_route(dwarf_locations, neighbouring_tiles):
    if neighbouring_tiles["E"] not in dwarf_locations and neighbouring_tiles["NE"] not in dwarf_locations and neighbouring_tiles["SE"] not in dwarf_locations:
        return neighbouring_tiles["E"]
    else:
        return None

def generate_neighbouring_coordinates(checked_dwarf):
    neigbhouring_coordinates = {}
    neigbhouring_coordinates["N"] = (checked_dwarf[0] - 1, checked_dwarf[1])
    neigbhouring_coordinates["S"] = (checked_dwarf[0] + 1, checked_dwarf[1])
    neigbhouring_coordinates["E"] = (checked_dwarf[0], checked_dwarf[1] + 1)
    neigbhouring_coordinates["W"] = (checked_dwarf[0], checked_dwarf[1] - 1)
    neigbhouring_coordinates["NW"] = (checked_dwarf[0] - 1, checked_dwarf[1] - 1)
    neigbhouring_coordinates["NE"] = (checked_dwarf[0] - 1, checked_dwarf[1] + 1)
    neigbhouring_coordinates["SW"] = (checked_dwarf[0] + 1, checked_dwarf[1] - 1)
    neigbhouring_coordinates["SE"] = (checked_dwarf[0] + 1, checked_dwarf[1] + 1)
    return neigbhouring_coordinates

main()