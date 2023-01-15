import copy
import queue

def main():
    valve_flow, valve_map = get_input()
    simplified_distance_map = modify_valve_map(valve_flow, valve_map)
    part1(valve_flow, simplified_distance_map, 30)
    part2(valve_flow, simplified_distance_map, 26)
    # part3(valve_flow, simplified_distance_map)

def get_input():
    valve_flow = {}
    valve_map = {}
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split()
        valve_flow[temp_line[1]] = int(temp_line[4][5:-1])
        valve_map[temp_line[1]] = []
        for elem in temp_line[9:]:
            valve_map[temp_line[1]].append(elem[:2])
    return valve_flow, valve_map

def modify_valve_map(valve_flow, valve_map):
    full_distances_map = {}
    for key, value in valve_map.items():
        build_distances_from_node(valve_map, key, full_distances_map)
    simplified_distance_map = simplified_distance_map_creator(full_distances_map, valve_flow)
    return simplified_distance_map

def simplified_distance_map_creator(full_distances_map, valve_flow):
    simplified_distance_map = {}
    for elem in valve_flow:
        if elem == "AA" or valve_flow[elem] != 0:
            simplified_distance_map[elem] = set()
    for checked_valve in simplified_distance_map:
        for next_possible_valve in full_distances_map[checked_valve]:
            if valve_flow[next_possible_valve[0]] != 0:
                simplified_distance_map[checked_valve].add(next_possible_valve)
    return simplified_distance_map

def build_distances_from_node(valve_map, start_node, full_distances_map):
    full_distances_map[start_node] = set()
    counter = 1
    neighbouring_nodes = set(valve_map[start_node])
    visited_nodes = set()
    visited_nodes.add(start_node)
    while len(neighbouring_nodes) > 0:
        new_neighbours = set()
        for neighbouring_node in neighbouring_nodes:
            if neighbouring_node not in visited_nodes:
                full_distances_map[start_node].add((neighbouring_node, counter))
                visited_nodes.add(neighbouring_node)
            for elem in valve_map[neighbouring_node]:
                if elem not in visited_nodes:
                    new_neighbours.add(elem)
        neighbouring_nodes = new_neighbours
        counter += 1
    return full_distances_map

def part1(valve_flow, simplified_distance_map, time_limit):
    # Initialise the priority queue
    completed_journeys, jouney_pq = initialise_the_pq(simplified_distance_map, valve_flow, time_limit)
    # Explore the remaining options
    explore_the_pq(jouney_pq, completed_journeys, simplified_distance_map, valve_flow, time_limit)
    # Find the best score
    print(count_best_score(completed_journeys))
    return 0

def part2(valve_flow, simplified_distance_map, time_limit):
    # Initialise the player priority queue
    completed_journeys_player, jouney_pq = initialise_the_pq(simplified_distance_map, valve_flow, time_limit)
    # Explore the remaining options
    explore_the_pq(jouney_pq, completed_journeys_player, simplified_distance_map, valve_flow, time_limit)
    completed_journeys_player.sort()
    # Reduce the list of completed_journeys --- Extend the list if incorrect solution is being rendered
    completed_journeys_player = completed_journeys_player[:5000]
    # Iterate over journeys completed by the player and analyse potential routes taken by the elephant
    best_completed_journey = 0
    for completed_player_journey in completed_journeys_player:
        completed_journeys_elephant, jouney_pq = initialise_the_pq(simplified_distance_map, valve_flow, time_limit, completed_player_journey[3][1:])
        explore_the_pq(jouney_pq, completed_journeys_elephant, simplified_distance_map, valve_flow, time_limit)
        alternative_best_score = count_best_score(completed_journeys_elephant)
        if alternative_best_score + completed_player_journey[1] > best_completed_journey:
            best_completed_journey = alternative_best_score + completed_player_journey[1]
    print(best_completed_journey)
    return 0

def count_best_score(completed_journeys):
    best_score = 0
    best_item = None
    for elem in completed_journeys:
        if elem[1] > best_score:
            best_score = elem[1]
            best_item = elem
    return best_item[1]

def initialise_the_pq(simplified_distance_map, valve_flow, time_limit, previous_jounrey = None):
    completed_journeys = []
    jouney_pq = queue.PriorityQueue()
    # Feed the PQ the initial possible options
    for possible_initial_destinations in simplified_distance_map["AA"]:
        if previous_jounrey != None and possible_initial_destinations[0] in previous_jounrey:
            continue
        else:
            steps_taken = possible_initial_destinations[1] + 1
            pressure_release = (time_limit - steps_taken) * valve_flow[possible_initial_destinations[0]]
            if previous_jounrey != None:
                journey = copy.deepcopy(previous_jounrey)
            else:
                journey = []
            journey.append("AA")
            journey.append(possible_initial_destinations[0])
            item = [-pressure_release, pressure_release, steps_taken, journey]
            jouney_pq.put(item)
    return completed_journeys, jouney_pq

def explore_the_pq(jouney_pq, completed_journeys, simplified_distance_map, valve_flow, time_limit):
    while jouney_pq.empty() == False:
        checked_item = jouney_pq.get()
        # Alternative 1 --- time limit exceeded
        if checked_item[2] > time_limit:
            continue
        # Alternative 2 --- time limit met
        if checked_item[2] == time_limit:
            completed_journeys.append(checked_item)
            continue
        # Alternative 3 --- all valves visited
        if len(simplified_distance_map) == len(checked_item[3]):
            completed_journeys.append(checked_item)
            continue
        # Alternative 4 --- explore next items
        for next_possible_step in simplified_distance_map[checked_item[3][-1]]:
            if next_possible_step[0] not in checked_item[3]:
                new_item = copy.deepcopy(checked_item)
                # Update the step count
                steps_taken = new_item[2] + 1 + next_possible_step[1]
                # If the result would exceed the permitted step count, add the current journey to completed ones
                if steps_taken > time_limit:
                    completed_journeys.append(new_item)
                else:
                    updated_pressure_release = new_item[1] + ((time_limit - steps_taken) * valve_flow[next_possible_step[0]])
                    new_item[0] = updated_pressure_release * -1
                    new_item[1] = updated_pressure_release
                    new_item[2] = steps_taken
                    new_item[3].append(next_possible_step[0])
                    jouney_pq.put(new_item)

main()