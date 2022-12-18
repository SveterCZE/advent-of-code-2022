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
    while True:
        left_list = checked_pair[0]
        right_list = checked_pair[1]

        # Base case /// 
        # If the left list runs out of items first, the inputs are in the right order. 
        # If the right list runs out of items first, the inputs are not in the right order.

        if len(left_list) == 0:
            return True
        elif len(right_list) == 0:
            return False

        left_item = left_list[0]
        right_item = right_list[0]

        # Alternative 1 --- both are integers
        if isinstance(left_item, int) and isinstance(right_item, int):
            if left_item < right_item:
                return True
            elif left_item > right_item:
                return False
            else:
                new_left_list = left_list[1:]
                new_right_list = right_list[1:]
                new_checked_pair = [new_left_list, new_right_list]
                if (len(new_left_list) != 0 and len(new_right_list) != 0):
                    pair_valid = check_pair_valid(new_checked_pair)
                    if pair_valid != None:
                        return pair_valid
        
        # Alternative 2 --- one is list and one is integer
        elif (isinstance(left_item, list) and isinstance(right_item, int)) or (isinstance(left_item, int) and isinstance(right_item, list)):
            if isinstance(right_item, int):
                right_item_value = right_item
                right_item = [right_item_value]
            elif isinstance(left_item, int):
                left_item_value = left_item
                left_item = [left_item_value]
        
        # Alternative 3 --- both are lists
        if isinstance(left_item, list) and isinstance(right_item, list):
            new_checked_pair = [left_item, right_item]
            pair_valid = check_pair_valid(new_checked_pair)
            if pair_valid != None:
                return pair_valid

        # Alternative 4 --- Continue checking next item
        new_left_list = left_list[1:]
        new_right_list = right_list[1:]
        checked_pair = [new_left_list, new_right_list]

def part2(instructions):
    pass

main()