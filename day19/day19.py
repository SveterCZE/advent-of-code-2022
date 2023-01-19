import re
import copy

def main():
    instructions  = get_input()
    part1(instructions, 24)
    part2(instructions, 32)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append([int(x) for x in re.findall(r'\d+', line)[1:]])
    return instructions

def part1(instructions, round_count):
    total_score = 0
    for i in range(1, len(instructions) + 1):
        print("BLUEPRINT ", i)
        states_db = set()
        current_states_list = []
        initial_state = [1,0,0,0,0,0,0,0]
        states_db.add(tuple(initial_state))
        current_states_list.append(initial_state)
        best_geode = run_recursive_simulation(instructions[i - 1], round_count, states_db, current_states_list, 0)
        total_score += i * best_geode  
    print("Total score: ")
    print(total_score)
    return 0

def part2(instructions, round_count):
    pass

def run_recursive_simulation(instructions, round_count, states_db, current_states_list, rounds_passed):
    # BASE CASE --- All rounds have passed
    if rounds_passed == round_count:
        best_geode = 0
        for elem in current_states_list:
            if elem[7] > best_geode:
                best_geode = elem[7]
        return best_geode
    else:
        print("Round: ", rounds_passed)
        rounds_passed += 1
        current_states_list = prune_the_states_list(current_states_list)
        new_states_list = []
        for checked_state in current_states_list:
            new_possible_states = generate_new_possible_states(instructions, checked_state)
            for elem in new_possible_states:
                if tuple(elem) not in states_db:
                    states_db.add(tuple(elem))
                    new_states_list.append(elem)
        return run_recursive_simulation(instructions, round_count, states_db, new_states_list, rounds_passed)

def generate_new_possible_states(instructions, checked_state):
    possible_new_states = []
    # Check if ore robot can be bulit
    if checked_state[1] >= instructions[0]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[0]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[0] += 1
        possible_new_states.append(newly_created_state)
    # Check if clay robot can be built
    if checked_state[1] >= instructions[1]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[1]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[2] += 1
        possible_new_states.append(newly_created_state)
    # Check if obsidian robot can be built
    if checked_state[1] >= instructions[2] and checked_state[3] >= instructions[3]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[2]
        newly_created_state[3] -= instructions[3]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[4] += 1
        possible_new_states.append(newly_created_state)
    # Check if geode robot can be built
    if checked_state[1] >= instructions[4] and checked_state[5] >= instructions[5]:
        newly_created_state = copy.deepcopy(checked_state)
        newly_created_state[1] -= instructions[4]
        newly_created_state[5] -= instructions[5]
        newly_created_state = extract_resouces(newly_created_state)
        newly_created_state[6] += 1
        possible_new_states.append(newly_created_state)
    # Nothing can be built
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

def prune_the_states_list(current_states_list):
    pruned_list = []
    for elem in current_states_list:
        if elem[6] != 0:
            pruned_list.append(elem)
    if len(pruned_list) == 0:
        return current_states_list
    else:
        return pruned_list

main()