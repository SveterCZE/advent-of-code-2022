def main():
    start, finish, list_of_hurricanes, initial_map_of_world = get_input()
    step_count, hurricanes = part1(start, finish, list_of_hurricanes, initial_map_of_world)
    print(step_count)
    start, finish, list_of_hurricanes, initial_map_of_world = get_input()
    part2(start, finish, list_of_hurricanes, initial_map_of_world)

def get_input():
    list_of_hurricanes = []
    initial_map_of_world = []
    possible_directions = [">", "<", "^", "v"]
    f = open("input.txt", "r")
    for line in f:
        initial_map_of_world.append(list(line.strip()))
    # Create a list of hurricanes
    for i in range(len(initial_map_of_world)):
        for j in range(len(initial_map_of_world[0])):
            if initial_map_of_world[i][j] in possible_directions:
                new_hurricane = Hurricane(initial_map_of_world, i, j)
                list_of_hurricanes.append(new_hurricane)
    # Find start and finish coordinates
    start = None
    finish = None
    for i in range(len(initial_map_of_world)):
        for j in range(len(initial_map_of_world[0])):
            if initial_map_of_world[i][j] == ".":
                if start == None:
                    start = (i,j)
                finish = (i,j)
    return start, finish, list_of_hurricanes, initial_map_of_world

def part1(start, finish, list_of_hurricanes, initial_map_of_world):
    step_count = 0
    player_coordinates = set()
    player_coordinates.add(start)
    while True:
        step_count += 1
        # Make one step with all hurricanes and record their position
        hurricane_coordinates = set()
        for hurricane in list_of_hurricanes:
            hurricane.move_one_step()
            hurricane_coordinates.add(hurricane.give_current_coordinate())
        # Make player moves
        new_player_coordinates = set()
        for checked_position in player_coordinates:
            # Add a position for a non-moving crew
            new_player_coordinates.add(checked_position)
            neigbouring_positions = generate_neighbouring_positions(checked_position)
            for neighbouring_position in neigbouring_positions:
                if is_valid_position(neighbouring_position, start, finish, initial_map_of_world):
                    new_player_coordinates.add(neighbouring_position)
        # Check for surviving crews
        surviving_crews = set()
        for checked_crew_position in new_player_coordinates:
            if checked_crew_position not in hurricane_coordinates:
                surviving_crews.add(checked_crew_position)
        # Check for victory
        if finish in surviving_crews:
            break
        player_coordinates = surviving_crews
    return step_count, list_of_hurricanes

def part2(start, finish, list_of_hurricanes, initial_map_of_world):
    first_leg_step_count, list_of_hurricanes = part1(start, finish, list_of_hurricanes, initial_map_of_world)
    second_legs_step_count, list_of_hurricanes = part1(finish, start, list_of_hurricanes, initial_map_of_world)
    third_leg_step_count, list_of_hurricanes = part1(start, finish, list_of_hurricanes, initial_map_of_world)
    print(first_leg_step_count + second_legs_step_count + third_leg_step_count)
    return 0

def generate_neighbouring_positions(checked_position):
    up_position = (checked_position[0] - 1, checked_position[1])
    down_position = (checked_position[0] + 1, checked_position[1])
    left_position = (checked_position[0], checked_position[1] - 1)
    right_position = (checked_position[0], checked_position[1] + 1)
    return [up_position, down_position, left_position, right_position]

def is_valid_position(checked_position, start, finish, initial_map_of_world):
    if checked_position == start:
        return True
    elif checked_position == finish:
        return True
    elif checked_position[0] <= 0:
        return False
    elif checked_position[1] <= 0:
        return False
    elif checked_position[0] >= len(initial_map_of_world):
        return False
    elif checked_position[1] >= len(initial_map_of_world[1]):
        return False
    elif initial_map_of_world[checked_position[0]][checked_position[1]] == "#":
        return False
    else:
        return True

class Hurricane:
    def __init__(self, world_map, i_coordinate, j_coordinate):
        self.i_coordinate = i_coordinate
        self.j_coordinate = j_coordinate
        self.movement_direction = world_map[i_coordinate][j_coordinate]
        self.world_map = world_map
    
    def give_current_coordinate(self):
        return (self.i_coordinate, self.j_coordinate)
    
    def move_one_step(self):
        if self.movement_direction == ">":
            temp_j_coordinate = self.j_coordinate + 1
            if temp_j_coordinate == len(self.world_map[0]) - 1:
                temp_j_coordinate = 1
            self.j_coordinate = temp_j_coordinate

        elif self.movement_direction == "<":
            temp_j_coordinate = self.j_coordinate - 1
            if temp_j_coordinate == 0:
                temp_j_coordinate = len(self.world_map[0]) - 2
            self.j_coordinate = temp_j_coordinate

        elif self.movement_direction == "^":
            temp_i_coordinate = self.i_coordinate - 1
            if temp_i_coordinate == 0:
                temp_i_coordinate = len(self.world_map) - 2
            self.i_coordinate = temp_i_coordinate

        elif self.movement_direction == "v":
            temp_i_coordinate = self.i_coordinate + 1
            if temp_i_coordinate == len(self.world_map) - 1:
                temp_i_coordinate = 1
            self.i_coordinate = temp_i_coordinate

main()