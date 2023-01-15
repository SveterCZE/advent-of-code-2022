import copy
import queue

def main():
    valve_flow, valve_map = get_input()
    simplified_distance_map = modify_valve_map(valve_flow, valve_map)
    # part1(valve_flow, simplified_distance_map)
    part2(valve_flow, simplified_distance_map)
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

def part1(valve_flow, simplified_distance_map):
    completed_journeys = []
    jouney_pq = queue.PriorityQueue()
    # Feed the PQ the initial possible options
    for possible_initial_destinations in simplified_distance_map["AA"]:
        steps_taken = possible_initial_destinations[1] + 1
        pressure_release = (30 - steps_taken) * valve_flow[possible_initial_destinations[0]]
        journey = ["AA"]
        journey.append(possible_initial_destinations[0])
        item = [-pressure_release, pressure_release, steps_taken, journey]
        jouney_pq.put(item)
    
    # Explore the remaining options
    while jouney_pq.empty() == False:
        checked_item = jouney_pq.get()
        # Alternative 1 --- time limit exceeded
        if checked_item[2] > 30:
            continue
        # Alternative 2 --- time limit met
        if checked_item[2] == 30:
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
                if steps_taken > 30:
                    completed_journeys.append(new_item)
                else:
                    updated_pressure_release = new_item[1] + ((30 - steps_taken) * valve_flow[next_possible_step[0]])
                    new_item[0] = updated_pressure_release * -1
                    new_item[1] = updated_pressure_release
                    new_item[2] = steps_taken
                    new_item[3].append(next_possible_step[0])
                    jouney_pq.put(new_item)
    
    # Find the best score
    best_score = 0
    best_item = None
    for elem in completed_journeys:
        if elem[1] > best_score:
            best_score = elem[1]
            best_item = elem
    print(best_item[1])
    return 0

def part2(valve_flow, simplified_distance_map):
    best_result = 0
    for possible_initial_destination_player in simplified_distance_map["AA"]:
        for possible_initial_destination_elephant in simplified_distance_map["AA"]:
            if possible_initial_destination_player != possible_initial_destination_elephant:
                print(possible_initial_destination_player, possible_initial_destination_elephant)
                steps_taken_player = possible_initial_destination_player[1] + 1
                pressure_release_player = (26 - steps_taken_player) * valve_flow[possible_initial_destination_player[0]]
                journey_player = ["AA"]
                journey_player.append(possible_initial_destination_player[0])

                step_taken_elephant = possible_initial_destination_elephant[1] + 1
                pressure_release_elephant = (26 - step_taken_elephant) * valve_flow[possible_initial_destination_elephant[0]]
                journey_elephant = ["AA"]
                journey_elephant.append(possible_initial_destination_elephant[0])

                total_pressure_release = pressure_release_player + pressure_release_elephant

                item = [-total_pressure_release, total_pressure_release, steps_taken_player, step_taken_elephant, journey_player, journey_elephant]
                best_solution = run_part2_combination(item, simplified_distance_map, valve_flow)
                print(best_solution)
                if best_solution > best_result:
                    best_result = best_solution
                    print(best_result)
    print(best_result)
    return 0

def run_part2_combination(item, simplified_distance_map, valve_flow):
    completed_journeys = []
    jouney_pq = queue.PriorityQueue()
    jouney_pq.put(item)
    
    # Explore the remaining options
    while jouney_pq.empty() == False:
        # if len(completed_journeys) > 1000000:
        #     break

        checked_item = jouney_pq.get()
        # Alternative 1 --- time limit exceeded for both items
        if checked_item[2] > 26 and checked_item[3] > 26:
            continue
        # Alternative 2 --- time limit met
        if checked_item[2] == 26 and checked_item[3] == 26:
            completed_journeys.append(checked_item)
            continue
        # Alternative 3 --- all valves visited
        if len(simplified_distance_map) == -1 + len(checked_item[4]) + len(checked_item[5]):
            completed_journeys.append(checked_item)
            continue
        # Alternative 4 --- explore next items

        # Alternative 4a --- less steps taken by the player
        if checked_item[2] < checked_item[3]:
            for next_possible_step in simplified_distance_map[checked_item[4][-1]]:
                if next_possible_step[0] not in checked_item[4] and next_possible_step[0] not in checked_item[5]:
                    new_item = copy.deepcopy(checked_item)
                    steps_taken_player = new_item[2] + 1 + next_possible_step[1]
                    if steps_taken_player > 26:
                        new_item[2] = 26
                        jouney_pq.put(new_item)
                    else:
                        updated_pressure_release = new_item[1] + ((26 - steps_taken_player) * valve_flow[next_possible_step[0]])
                        new_item[0] = updated_pressure_release * -1
                        new_item[1] = updated_pressure_release
                        new_item[2] = steps_taken_player
                        new_item[4].append(next_possible_step[0])
                        jouney_pq.put(new_item)

        # Alternative 4b --- less steps taken by the elephant
        elif checked_item[2] > checked_item[3]:
            for next_possible_step in simplified_distance_map[checked_item[5][-1]]:
                if next_possible_step[0] not in checked_item[4] and next_possible_step[0] not in checked_item[5]:
                    new_item = copy.deepcopy(checked_item)
                    steps_taken_elephant = new_item[3] + 1 + next_possible_step[1]
                    if steps_taken_elephant > 26:
                        new_item[3] = 26
                        jouney_pq.put(new_item)
                    else:
                        updated_pressure_release = new_item[1] + ((26 - steps_taken_elephant) * valve_flow[next_possible_step[0]])
                        new_item[0] = updated_pressure_release * -1
                        new_item[1] = updated_pressure_release
                        new_item[3] = steps_taken_elephant
                        new_item[5].append(next_possible_step[0])
                        jouney_pq.put(new_item)

        # Alternative 4c --- less steps taken by the player
        elif checked_item[2] == checked_item[3]:
            for possible_initial_destination_player in simplified_distance_map[checked_item[4][-1]]:
                for possible_initial_destination_elephant in simplified_distance_map[checked_item[5][-1]]:
                    if possible_initial_destination_player[0] != possible_initial_destination_elephant[0]:
                        if possible_initial_destination_player[0] not in checked_item[4] and possible_initial_destination_player[0] not in checked_item[5] and possible_initial_destination_elephant[0] not in checked_item[4] and possible_initial_destination_elephant[0] not in checked_item[5]:

                            new_item = copy.deepcopy(checked_item)
                            
                            steps_taken_player = new_item[2] + 1 + possible_initial_destination_player[1]
                            if steps_taken_player > 26:
                                new_item[2] = 26
                            else:
                                updated_pressure_release = new_item[1] + ((26 - steps_taken_player) * valve_flow[possible_initial_destination_player[0]])
                                new_item[0] = updated_pressure_release * -1
                                new_item[1] = updated_pressure_release
                                new_item[2] = steps_taken_player
                                new_item[4].append(possible_initial_destination_player[0])

                            steps_taken_elephant = new_item[3] + 1 + possible_initial_destination_elephant[1]
                            if steps_taken_elephant > 26:
                                new_item[2] = 26
                            else:
                                updated_pressure_release = new_item[1] + ((26 - steps_taken_elephant) * valve_flow[possible_initial_destination_elephant[0]])
                                new_item[0] = updated_pressure_release * -1
                                new_item[1] = updated_pressure_release
                                new_item[3] = steps_taken_elephant
                                new_item[5].append(possible_initial_destination_elephant[0])
                            
                            jouney_pq.put(new_item)

    # Find the best score
    best_score = 0
    best_item = None
    for elem in completed_journeys:
        if elem[1] > best_score:
            best_score = elem[1]
            best_item = elem
        # if elem[4][1] == "JJ" and elem[4][2] == "BB" and elem[4][3] == "CC" and elem[5][1] == "DD" and elem[5][2] == "HH":
        #     print(elem)
    return(best_item[1])

# def part3(valve_flow, simplified_distance_map):
#     # first run
#     completed_journeys = []
#     jouney_pq = queue.PriorityQueue()
#     # Feed the PQ the initial possible options
#     for possible_initial_destinations in simplified_distance_map["AA"]:
#         steps_taken = possible_initial_destinations[1] + 1
#         pressure_release = (26 - steps_taken) * valve_flow[possible_initial_destinations[0]]
#         journey = ["AA"]
#         journey.append(possible_initial_destinations[0])
#         item = [-pressure_release, pressure_release, steps_taken, journey]
#         jouney_pq.put(item)
    
#     # Explore the remaining options
#     while jouney_pq.empty() == False:
#         checked_item = jouney_pq.get()
#         # Alternative 1 --- time limit exceeded
#         if checked_item[2] > 26:
#             continue
#         # Alternative 2 --- time limit met
#         if checked_item[2] == 26:
#             completed_journeys.append(checked_item)
#             continue
#         # Alternative 3 --- all valves visited
#         if len(simplified_distance_map) == len(checked_item[3]):
#             completed_journeys.append(checked_item)
#             continue
#         # Alternative 4 --- explore next items
#         for next_possible_step in simplified_distance_map[checked_item[3][-1]]:
#             if next_possible_step[0] not in checked_item[3]:
#                 new_item = copy.deepcopy(checked_item)
#                 # Update the step count
#                 steps_taken = new_item[2] + 1 + next_possible_step[1]
#                 # If the result would exceed the permitted step count, add the current journey to completed ones
#                 if steps_taken > 26:
#                     completed_journeys.append(new_item)
#                 else:
#                     updated_pressure_release = new_item[1] + ((26 - steps_taken) * valve_flow[next_possible_step[0]])
#                     new_item[0] = updated_pressure_release * -1
#                     new_item[1] = updated_pressure_release
#                     new_item[2] = steps_taken
#                     new_item[3].append(next_possible_step[0])
#                     jouney_pq.put(new_item)
    
#     # Find the best score - fist run
#     best_score_first_runner = 0
#     best_item_first_runner = None
#     for elem in completed_journeys:
#         if elem[1] > best_score_first_runner:
#             best_score_first_runner = elem[1]
#             best_item_first_runner = elem
#     # print(best_item_first_runner[1])

#     # Run second round
#     completed_journeys = []
#     jouney_pq = queue.PriorityQueue()
#     # Feed the PQ the initial possible options
#     for possible_initial_destinations in simplified_distance_map["AA"]:
#         steps_taken = possible_initial_destinations[1] + 1
#         pressure_release = (26 - steps_taken) * valve_flow[possible_initial_destinations[0]]
#         journey = copy.deepcopy(best_item_first_runner[3])
#         journey.append("AA")
#         journey.append(possible_initial_destinations[0])
#         item = [-pressure_release, pressure_release, steps_taken, journey]
#         jouney_pq.put(item)

#     # Explore the remaining options
#     while jouney_pq.empty() == False:
#         checked_item = jouney_pq.get()
#         # Alternative 1 --- time limit exceeded
#         if checked_item[2] > 26:
#             continue
#         # Alternative 2 --- time limit met
#         if checked_item[2] == 26:
#             completed_journeys.append(checked_item)
#             continue
#         # Alternative 3 --- all valves visited
#         if len(simplified_distance_map) == len(checked_item[3]):
#             completed_journeys.append(checked_item)
#             continue
#         # Alternative 4 --- explore next items
#         for next_possible_step in simplified_distance_map[checked_item[3][-1]]:
#             if next_possible_step[0] not in checked_item[3]:
#                 new_item = copy.deepcopy(checked_item)
#                 # Update the step count
#                 steps_taken = new_item[2] + 1 + next_possible_step[1]
#                 # If the result would exceed the permitted step count, add the current journey to completed ones
#                 if steps_taken > 26:
#                     completed_journeys.append(new_item)
#                 else:
#                     updated_pressure_release = new_item[1] + ((26 - steps_taken) * valve_flow[next_possible_step[0]])
#                     new_item[0] = updated_pressure_release * -1
#                     new_item[1] = updated_pressure_release
#                     new_item[2] = steps_taken
#                     new_item[3].append(next_possible_step[0])
#                     jouney_pq.put(new_item)

#     best_score_second_runner = 0
#     best_item_second_runner = None
#     for elem in completed_journeys:
#         if elem[1] > best_score_second_runner:
#             best_score_second_runner = elem[1]
#             best_item_second_runner = elem
#     # print(best_item_second_runner[1])
#     print(best_score_first_runner + best_score_second_runner)
    # return 0

main()