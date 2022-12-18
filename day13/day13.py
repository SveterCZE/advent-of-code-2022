import ast

def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    temp_pair = []
    for line in f:
        if len(line.strip()) != 0:
            mod_line = ast.literal_eval(line)
            temp_pair.append(mod_line)
        else:
            instructions.append(temp_pair)
            temp_pair = []
    instructions.append(temp_pair)
    return instructions

def part1(instructions):
    valid_pairs = []
    for i in range(len(instructions)):
        pair_valid = check_pair_valid(instructions[i])
        if pair_valid == True:
            print(instructions[i])
            valid_pairs.append(i + 1)
    print(sum(valid_pairs))
    return 0

def check_pair_valid(checked_pair):
    # Iterate over every i-th item in each packet
    for i in range(len(checked_pair[0])):
        left_item = checked_pair[0][i]
        # If the right list is shorter (i.e. you cannot assign a corrsponding value with ), return False
        try:
            right_item = checked_pair[1][i]
        except:
            return False

        # Alternative 1 --- both are integers
        if isinstance(left_item, int) and isinstance(right_item, int):
            if left_item < right_item:
                return True
            elif left_item > right_item:
                return False
            else:
                pass

        # Alternative 2 --- one is list and one is integer
        if (isinstance(left_item, list) and isinstance(right_item, int)) or (isinstance(left_item, int) and isinstance(right_item, list)):
            if isinstance(right_item, int):
                right_item = [right_item]
            elif isinstance(left_item, int): 
                left_item = [left_item]
        
        # Alternative 3 --- both are lists
        if isinstance(left_item, list) and isinstance(right_item, list):
            new_checked_pair = [left_item, right_item]
            pair_valid = check_pair_valid(new_checked_pair)
            if pair_valid != None:
                return pair_valid

    # Return false if ran through all items, but there are still 
    if isinstance(checked_pair[0], list) and isinstance(checked_pair[1], list):
        if len(checked_pair[0]) < len(checked_pair[1]):
            return True

def part2(instructions):
    pass

main()