import copy

def main():
    tiles, instructions  = get_input()
    part1(tiles, instructions)
    part2(tiles, instructions)

def get_input():
    tiles = create_tiles()
    f = open("input.txt", "r")
    for line in f:
        instructions = list(line.strip())
    return tiles, instructions

def part1(tiles, instructions):
    tile_counter = 0
    highest_point = -1
    instruction_counter = 0
    resting_tiles = set()
    # make individual tiles fall
    for i in range(2022):
        highest_point, instruction_counter = make_tile_fall(tiles, instructions, instruction_counter, highest_point, resting_tiles, tile_counter)
        tile_counter += 1
    print(highest_point + 1)
    return 0

def make_tile_fall(tiles, instructions, instruction_counter, highest_point, resting_tiles, tile_counter):
    # Initialise the tile
    selected_tile = tiles[tile_counter % 5]
    tile_corner_coordinate = (2, highest_point + 4)
    selected_tile = set_tile_start_coordinates(selected_tile, tile_corner_coordinate)
    # Let the tile fall
    while True:
        # Firstly, move it to the side. If movement is not possible, do not move the tile
        movement_instruction = instructions[instruction_counter % len(instructions)]
        instruction_counter += 1
        proposed_new_coordinates = move_tile_based_on_instruction(movement_instruction, selected_tile)
        if proposed_movement_not_conflicting(proposed_new_coordinates, resting_tiles):
            selected_tile = proposed_new_coordinates
        # Secondly, move down by one tile
        proposed_new_coordinates = drop_tile_by_one_level(selected_tile)
        if proposed_movement_does_not_rest(proposed_new_coordinates, resting_tiles):
            selected_tile = proposed_new_coordinates
        else:
            resting_tiles = make_tiles_rest(selected_tile, resting_tiles)
            highest_point = determine_higest_point(selected_tile, highest_point)
            break
    return highest_point, instruction_counter

def part2(tiles, instructions):
    rep_highest_point, rep_tile_counter, rep_instruction_remainder = find_repeating_pattern(tiles, instructions)
    target_tile_numbers = 1000000000000
    repetitions = target_tile_numbers // rep_tile_counter
    repetitions -= 1
    remainder = target_tile_numbers % rep_tile_counter
    repeated_chunk_size = repetitions * rep_highest_point
    
    # Simulate one round plus remaineder
    tile_counter = 0
    highest_point = -1
    instruction_counter = 0
    resting_tiles = set()
    for i in range(rep_tile_counter + remainder):
        highest_point, instruction_counter = make_tile_fall(tiles, instructions, instruction_counter, highest_point, resting_tiles, tile_counter)
        tile_counter += 1
    print(highest_point + repeated_chunk_size + 1)
    return 0


def find_repeating_pattern(tiles, instructions):
    tile_counter = 0
    highest_point = -1
    instruction_counter = 0
    resting_tiles = set()
    # Find the repetition pattern
    while True:
        highest_point, instruction_counter = make_tile_fall(tiles, instructions, instruction_counter, highest_point, resting_tiles, tile_counter)
        tile_counter += 1
        instruction_remainder = instruction_counter % len(instructions)
        if instruction_remainder <= 5 and instruction_counter > 5:
            return highest_point, tile_counter, instruction_remainder

def determine_higest_point(selected_tile, highest_point):
    for elem in selected_tile:
        if elem[1] > highest_point:
            highest_point = elem[1]
    return highest_point

def proposed_movement_does_not_rest(proposed_new_coordinates, resting_tiles):
    for elem in proposed_new_coordinates:
        if elem[1] < 0:
            return False
        elif elem in resting_tiles:
            return False
    return True

def drop_tile_by_one_level(selected_tile):
    dropped_tile = []
    for i in range(len(selected_tile)):
        dropped_tile.append((selected_tile[i][0], selected_tile[i][1] - 1))
    return dropped_tile

def proposed_movement_not_conflicting(proposed_new_coordinates, resting_tiles):
    for elem in proposed_new_coordinates:
        if elem[0] < 0:
            return False
        if elem[0] >= 7:
            return False
        if elem in resting_tiles:
            return False
    return True

def set_tile_start_coordinates(selected_tile, tile_corner_coordinate):
    initialised_tile = []
    for i in range(len(selected_tile)):
        initialised_tile.append((selected_tile[i][0] + tile_corner_coordinate[0], selected_tile[i][1] + tile_corner_coordinate[1]))
    return initialised_tile

def move_tile_based_on_instruction(movement_instruction, selected_tile):
    moved_tile = []
    if movement_instruction == ">":
        for elem in selected_tile:
            moved_tile.append((elem[0] + 1, elem[1]))
    elif movement_instruction == "<":
        for elem in selected_tile:
            moved_tile.append((elem[0] - 1, elem[1]))
    return moved_tile

def make_tiles_rest(selected_tile, resting_tiles):
    for elem in selected_tile:
        resting_tiles.add(elem)
    return resting_tiles

def create_tiles():
    tile1 = [(0,0), (1,0), (2,0), (3,0)]
    tile2 = [(1,0), (0,1), (1,1), (1,2), (2,1)]
    tile3 = [(0,0), (1,0), (2,0), (2,1), (2,2)]
    tile4 = [(0,0), (0,1), (0,2), (0,3)]
    tile5 = [(0,0), (0,1), (1,0), (1,1)]
    list_of_tiles = [tile1, tile2, tile3, tile4, tile5]
    return list_of_tiles

main()