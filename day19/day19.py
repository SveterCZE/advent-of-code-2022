import re
import copy

def main():
    instructions  = get_input()
    part1(instructions, 24)
    part2(instructions[:3], 32)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append([int(x) for x in re.findall(r'\d+', line)[1:]])
    return instructions

def part1(instructions, round_count):
    total_score = 0
    for i in range(1, len(instructions) + 1):
        # print("BLUEPRINT ", i)
        states_db = set()
        current_states_list = []
        initial_state = [1,0,0,0,0,0,0,0]
        states_db.add(tuple(initial_state))
        current_states_list.append(initial_state)
        best_geode = run_recursive_simulation(instructions[i - 1], round_count, states_db, current_states_list, 0, determine_maxima(instructions[i - 1]))
        total_score += i * best_geode
    # print("Total score: ")
    print(total_score)
    return 0

def part2(instructions, round_count):
    total_score = 1
    for i in range(1, len(instructions) + 1):
        # print("BLUEPRINT ", i)
        states_db = set()
        current_states_list = []
        initial_state = [1,0,0,0,0,0,0,0]
        states_db.add(tuple(initial_state))
        current_states_list.append(initial_state)
        best_geode = run_recursive_simulation(instructions[i - 1], round_count, states_db, current_states_list, 0, determine_maxima(instructions[i - 1]))
        total_score = total_score * best_geode
        # print("Best geode:", best_geode)
    # print("Total score: ")
    print(total_score)
    return 0

def run_recursive_simulation(instructions, round_count, states_db, current_states_list, rounds_passed, maxima):
    # BASE CASE --- All rounds have passed
    if rounds_passed == round_count:
        best_geode = 0
        for elem in current_states_list:
            if elem[7] > best_geode:
                best_geode = elem[7]
        return best_geode
    else:
        # print("Round: ", rounds_passed)
        rounds_passed += 1
        # current_states_list = prune_the_states_list(current_states_list, rounds_passed)
        # current_states_list = prune_the_states_list_v2(current_states_list)
        new_states_list = []
        for checked_state in current_states_list:
            new_possible_states = generate_new_possible_states(instructions, checked_state, maxima)
            for elem in new_possible_states:
                if tuple(elem) not in states_db:
                    states_db.add(tuple(elem))
                    new_states_list.append(elem)
        return run_recursive_simulation(instructions, round_count, states_db, new_states_list, rounds_passed, maxima)

def generate_new_possible_states(instructions, checked_state, maxima):
    possible_new_states = []
    # Option 1 --- If geode robot can be built, do it and do not build anything else
    # Check if geode robot can be built
    if checked_state[1] >= instructions[4] and checked_state[5] >= instructions[5]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[4]
        newly_created_state[5] -= instructions[5]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[6] += 1
        possible_new_states.append(newly_created_state)
        return possible_new_states
    # Option 2 --- Try building other robots, unless their maximum was reached
    else:
        robot_built = False
        # Check if ore robot can be bulit
        if checked_state[1] >= instructions[0] and checked_state[0] != maxima["ore"]:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[0]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[0] += 1
            possible_new_states.append(newly_created_state)
            robot_built = True
        # Check if clay robot can be built
        if checked_state[1] >= instructions[1] and checked_state[2] != maxima["clay"]:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[1]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[2] += 1
            possible_new_states.append(newly_created_state)
            robot_built = True
        # Check if obsidian robot can be built
        if checked_state[1] >= instructions[2] and checked_state[3] >= instructions[3] and checked_state[4] != maxima["obsidian"]:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[2]
            newly_created_state[3] -= instructions[3]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[4] += 1
            possible_new_states.append(newly_created_state)
            robot_built = True
        # Nothing can be built --- just extract resources
        if robot_built == False:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state = extract_resouces(newly_created_state)
            possible_new_states.append(newly_created_state)
        return possible_new_states

def extract_resouces(newly_created_state):
    if newly_created_state[0] > 0:
        newly_created_state[1] += newly_created_state[0]
    if newly_created_state[2] > 0:
        newly_created_state[3] += newly_created_state[2]
    if newly_created_state[4] > 0:
        newly_created_state[5] += newly_created_state[4]
    if newly_created_state[6] > 0:
        newly_created_state[7] += newly_created_state[6]
    return newly_created_state

def prune_the_states_list(current_states_list, rounds_passed):
    pruned_list = []
    for elem in current_states_list:
        if rounds_passed <= 24:
            if elem[6] != 0:
                pruned_list.append(elem)
        elif rounds_passed > 24:
            if elem[6] < 2:
                pruned_list.append(elem)
    if len(pruned_list) == 0:
        return current_states_list
    else:
        return pruned_list

def prune_the_states_list_v2(current_states_list):
    max_geode_robot = 0
    for elem in current_states_list:
        if elem[6] > max_geode_robot:
            max_geode_robot = elem[6]
    if max_geode_robot == 0:
        return current_states_list
    else:
        pruned_list = []
        for elem in current_states_list:
            if elem[6] != max_geode_robot:
                pruned_list.append(elem)
        return pruned_list

def determine_maxima(checked_instructions):
    maxima = {}
    maxima["ore"] = max(checked_instructions[0], checked_instructions[1], checked_instructions[2], checked_instructions[4])
    maxima["clay"] = checked_instructions[3]
    maxima["obsidian"] = checked_instructions[5]
    return maxima

main()