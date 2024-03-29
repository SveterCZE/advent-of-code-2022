import re
import copy
import time

def main():
    instructions  = get_input()
    st = time.time()
    part1(instructions, 24)
    pt1 = time.time()
    print('Execution time, part 1:', pt1 - st, 'seconds')
    part2(instructions[:3], 32)
    pt2 = time.time()
    print('Execution time, part 2:', pt2 - pt1, 'seconds')

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append([int(x) for x in re.findall(r'\d+', line)[1:]])
    return instructions

def part1(instructions, round_count):
    total_score = 0
    for i in range(1, len(instructions) + 1):
        states_db = set()
        current_states_list = []
        initial_state = [1,0,0,0,0,0,0,0, False, False, False]
        states_db.add(tuple(initial_state))
        current_states_list.append(initial_state)
        best_geode = run_recursive_simulation(instructions[i - 1], round_count, states_db, current_states_list, 0, determine_maxima(instructions[i - 1]))
        total_score += i * best_geode
    print(total_score)
    return 0

def part2(instructions, round_count):
    total_score = 1
    for i in range(1, len(instructions) + 1):
        states_db = set()
        current_states_list = []
        initial_state = [1,0,0,0,0,0,0,0, False, False, False]
        states_db.add(tuple(initial_state))
        current_states_list.append(initial_state)
        best_geode = run_recursive_simulation(instructions[i - 1], round_count, states_db, current_states_list, 0, determine_maxima(instructions[i - 1]))
        total_score = total_score * best_geode
    print(total_score)
    return 0

def run_recursive_simulation(instructions, round_count, states_db, current_states_list, rounds_passed, maxima):
    # BASE CASE --- All rounds have passed
    if rounds_passed == round_count:
        return find_best_geode(current_states_list)
    else:
        rounds_passed += 1
        remaining_rounds = round_count - rounds_passed
        current_states_list = prune_badly_performing_states(current_states_list, remaining_rounds)
        # Optimisation 1 --- If two rounds remain, do no build new stuff
        new_states_list = []
        for checked_state in current_states_list:
            new_possible_states = generate_new_possible_states(instructions, checked_state, maxima, remaining_rounds)
            for elem in new_possible_states:
                if tuple(elem[:8]) not in states_db:
                    states_db.add(tuple(elem[:8]))
                    new_states_list.append(elem)
        return run_recursive_simulation(instructions, round_count, states_db, new_states_list, rounds_passed, maxima)

def generate_new_possible_states(instructions, checked_state, maxima, remaining_rounds):
    possible_new_states = []
    # Option 1 --- If geode robot can be built, do it and do not build anything else
    # Check if geode robot can be built
    if checked_state[1] >= instructions[4] and checked_state[5] >= instructions[5]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[4]
        newly_created_state[5] -= instructions[5]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[6] += 1
        newly_created_state[8] = False
        newly_created_state[9] = False
        newly_created_state[10] = False
        reduce_excessive_resources(newly_created_state, maxima, remaining_rounds)
        possible_new_states.append(newly_created_state)
        return possible_new_states
    # Option 2 --- Try building other robots, unless their maximum was reached
    else:
        # Check if ore robot can be bulit
        if checked_state[1] >= instructions[0] and checked_state[0] != maxima["ore"] and remaining_rounds > 2 and checked_state[8] == False:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[0]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[0] += 1
            checked_state[8] = True
            newly_created_state[8] = False
            newly_created_state[9] = False
            newly_created_state[10] = False
            reduce_excessive_resources(newly_created_state, maxima, remaining_rounds)
            possible_new_states.append(newly_created_state)
        # Check if clay robot can be built
        if checked_state[1] >= instructions[1] and checked_state[2] != maxima["clay"] and remaining_rounds > 2 and checked_state[9] == False:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[1]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[2] += 1
            checked_state[9] = True
            newly_created_state[8] = False
            newly_created_state[9] = False
            newly_created_state[10] = False
            reduce_excessive_resources(newly_created_state, maxima, remaining_rounds)
            possible_new_states.append(newly_created_state)
        # Check if obsidian robot can be built
        if checked_state[1] >= instructions[2] and checked_state[3] >= instructions[3] and checked_state[4] != maxima["obsidian"] and remaining_rounds > 2 and checked_state[10] == False:
            newly_created_state = copy.deepcopy(checked_state)
            newly_created_state[1] -= instructions[2]
            newly_created_state[3] -= instructions[3]
            newly_created_state = extract_resouces(newly_created_state)
            newly_created_state[4] += 1
            checked_state[10] = True
            newly_created_state[8] = False
            newly_created_state[9] = False
            newly_created_state[10] = False
            reduce_excessive_resources(newly_created_state, maxima, remaining_rounds)
            possible_new_states.append(newly_created_state)
        # Nothing can be built --- just extract resources
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state = extract_resouces(newly_created_state)
        reduce_excessive_resources(newly_created_state, maxima, remaining_rounds)
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

def prune_badly_performing_states(current_states_list, remaining_rounds):
    best_geode_count = find_best_geode(current_states_list)
    viable_states = []
    for checked_state in current_states_list:
        possible_max_geodes = checked_state[7] + (checked_state[6] * remaining_rounds) + (remaining_rounds*(remaining_rounds + 1))//2
        if possible_max_geodes < best_geode_count:
            pass
        else:
            viable_states.append(checked_state)
    return viable_states

def reduce_excessive_resources(newly_created_state, maxima, remaining_rounds):
    newly_created_state[1] = min(newly_created_state[1], maxima["ore"] + (maxima["ore"] - newly_created_state[0]) * remaining_rounds)
    newly_created_state[3] = min(newly_created_state[3], maxima["clay"] + (maxima["clay"] - newly_created_state[2]) * remaining_rounds)
    newly_created_state[5] = min(newly_created_state[5], maxima["obsidian"] + (maxima["obsidian"] - newly_created_state[4]) * remaining_rounds)
    return newly_created_state

def determine_maxima(checked_instructions):
    maxima = {}
    maxima["ore"] = max(checked_instructions[0], checked_instructions[1], checked_instructions[2], checked_instructions[4])
    maxima["clay"] = checked_instructions[3]
    maxima["obsidian"] = checked_instructions[5]
    return maxima

def find_best_geode(current_states_list):
    best_geode = 0
    for elem in current_states_list:
        if elem[7] > best_geode:
            best_geode = elem[7]
    return best_geode

main()