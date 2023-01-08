import copy

def main():
    valve_flow, valve_map = get_input()
    valve_map, distance_map = modify_valve_map(valve_flow, valve_map)
    # part1(valve_flow, valve_map, distance_map)
    # part2(valve_flow, valve_map, distance_map)

def get_input():
    valve_flow = {}
    valve_map = {}
    f = open("sample.txt", "r")
    for line in f:
        temp_line = line.strip().split()
        valve_flow[temp_line[1]] = int(temp_line[4][5:-1])
        valve_map[temp_line[1]] = []
        for elem in temp_line[9:]:
            valve_map[temp_line[1]].append(elem[:2])
    return valve_flow, valve_map

def modify_valve_map(valve_flow, valve_map):
    modified_valve_map = {}
    starting_coordinate = "AA"
    distance_map = {}
    modified_valve_map[starting_coordinate] = set()
    for key, value in valve_flow.items():
        if value != 0:
            modified_valve_map[key] = set()
    visited_places = []
    visited_places.append(starting_coordinate)
    update_map(starting_coordinate, starting_coordinate, visited_places, 0, modified_valve_map, valve_flow, valve_map, distance_map)
    add_complete_distances(distance_map, modified_valve_map, valve_flow)
    print(distance_map)
    return modified_valve_map, distance_map

def part1(valve_flow, valve_map, distance_map):
    # print(valve_map)
    # print(distance_map)
    starting_coordinate = "AA"
    solutions = set()
    for neighbouring_coordinate in valve_map[starting_coordinate]:
        print(neighbouring_coordinate)
        time_elapsed = 0
        released_pressure = 0
        journey = []
        journey.append(starting_coordinate)
        open_valves = set()
        explore_map(valve_flow, valve_map, neighbouring_coordinate, solutions, time_elapsed + 1, open_valves, released_pressure, distance_map)
    print(sorted(solutions))
    return 0

def part2(valve_flow, valve_map):
    pass

def explore_map(valve_flow, valve_map, checked_coordinate, solutions, time_elapsed, open_valves, released_pressure, distance_map):
    if len(solutions) > 100:
        return
    
    # journey.append(checked_coordinate)

    # Check that the example solution is calculated properly
    # if journey[1] != "DD":
    #     return
    # if len(journey) > 2:
    #     if journey[2] != "CC":
    #         return
    # if len(journey) > 3:
    #     if journey[3] != "BB":
    #         return
    # if len(journey) > 4:
    #     if journey[4] != "AA":
    #         return
    # if len(journey) > 5:
    #     if journey[5] != "JJ":
    #         return
    # if len(journey) > 6:
    #     if journey[6] != "AA":
    #         return
    # if len(journey) > 7:
    #     if journey[7] != "DD":
    #         return
    # if len(journey) > 8:
    #     if journey[8] != "EE":
    #         return
    # if len(journey) > 9:
    #     if journey[9] != "HH":
    #         return
    # if len(journey) > 10:
    #     if journey[10] != "EE":
    #         return
    # if len(journey) > 11:
    #     if journey[11] != "DD":
    #         return
    # if len(journey) > 12:
    #     if journey[12] != "CC":
    #         return

    # Alternative 1 --- All valves are open. No need to move forward. Record the result
    if len(open_valves) + 1 == len(valve_map):
            solutions.add(released_pressure)
            return
    # Alternative 2 --- circular move detected.
    # elif len(journey) >= 3 and journey[-4:][0] == journey[-4:][2] and journey[-4:][1] == checked_coordinate:
    #     return
    # Alternative 3 --- time limit exceeded
    if time_elapsed > 30:
            solutions.add(released_pressure)
            return
    # Alternative 4 --- valve is open or is starting value --- explore other valves. Or do not open the small item
    elif checked_coordinate in open_valves or checked_coordinate == "AA" or (checked_coordinate not in open_valves and valve_flow[checked_coordinate] < 5):
        list_of_neigbours = valve_map[checked_coordinate]
        next_steps = []
        for elem in list_of_neigbours:
            if elem in open_valves:
                next_steps.append(elem)
            else:
                next_steps.insert(0, elem)
        for neighbouring_coordinate in next_steps:
            # new_journey = copy.deepcopy(journey)
            # new_open_valves = copy.deepcopy(open_valves)
            # new_journey.append(neighbouring_coordinate)
            journey_time = distance_map[(checked_coordinate, neighbouring_coordinate)]
            explore_map(valve_flow, valve_map, neighbouring_coordinate, solutions, time_elapsed + journey_time, open_valves, released_pressure, distance_map)
    # Alternative 5 --- valve is not open
    if checked_coordinate not in open_valves:
        # Open valve --- create a copy of it
        new_open_valves = copy.deepcopy(open_valves)
        new_open_valves.add(checked_coordinate)
        # Calculate the amount of release pressure until the time lapses
        rounds_of_pressure_release = 30 - time_elapsed - 1
        if rounds_of_pressure_release > 0:
            released_pressure = released_pressure + (rounds_of_pressure_release * valve_flow[checked_coordinate])
        
        list_of_neigbours = valve_map[checked_coordinate]
        next_steps = []
        for elem in list_of_neigbours:
            if elem in open_valves:
                next_steps.append(elem)
            else:
                next_steps.insert(0, elem)
        
        for neighbouring_coordinate in next_steps:
            # new_journey = copy.deepcopy(journey)
            # new_journey.append(neighbouring_coordinate)
            journey_time = distance_map[(checked_coordinate, neighbouring_coordinate)]
            explore_map(valve_flow, valve_map, neighbouring_coordinate, solutions, time_elapsed + journey_time + 1, new_open_valves, released_pressure, distance_map)


def update_map(starting_coordinate, previous_coordinate, visited_places, path_distance, modified_valve_map, valve_flow, valve_map, distance_map):
    for neigbouring_coordinate in valve_map[previous_coordinate]:
        if neigbouring_coordinate not in visited_places:
            updated_journey_path = copy.deepcopy(visited_places)
            updated_journey_path.append(neigbouring_coordinate)
            # Alternative 1 --- the coordinate has a flow
            if valve_flow[neigbouring_coordinate] != 0:
                distance_map[(starting_coordinate, neigbouring_coordinate)] = path_distance + 1
                distance_map[(neigbouring_coordinate, starting_coordinate)] = path_distance + 1
                modified_valve_map[starting_coordinate].add(neigbouring_coordinate)
                modified_valve_map[neigbouring_coordinate].add(starting_coordinate)
                update_map(neigbouring_coordinate, neigbouring_coordinate, updated_journey_path, 0, modified_valve_map, valve_flow, valve_map, distance_map)
            # Alternative 2 --- the coordinate does not have a flow
            else:
                update_map(starting_coordinate, neigbouring_coordinate, updated_journey_path, path_distance + 1, modified_valve_map, valve_flow, valve_map, distance_map)

def add_complete_distances(distance_map, modified_valve_map, valve_flow):
    for starting_coordinate in valve_flow:
        if starting_coordinate != "AA":
            visited_nodes = []
            visited_nodes.append(starting_coordinate)
            add_complete_distances_helper(distance_map, modified_valve_map, valve_flow, starting_coordinate, starting_coordinate, visited_nodes, 0)

def add_complete_distances_helper(distance_map, modified_valve_map, valve_flow, starting_coordinate, previous_coordinate, visited_nodes, distance_travelled):
    for neighbouring_coordinate in modified_valve_map[previous_coordinate]:
        if neighbouring_coordinate not in visited_nodes:
            visited_nodes.append(neighbouring_coordinate)
            nodes_distance = distance_travelled + distance_map[(previous_coordinate, neighbouring_coordinate)]
            distance_map[]


main()