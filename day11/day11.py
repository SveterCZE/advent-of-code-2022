def main():
    instructions = get_input()
    part1(instructions, True, 20)
    instructions = get_input()
    part1(instructions, False, 10000)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    temp_moneky = Monkey()
    for line in f:
        temp_line = line.strip().split()
        if len(temp_line) == 0:
            instructions.append(temp_moneky)
            temp_moneky = Monkey()
        elif temp_line[0] == "Starting":
            temp_moneky.list_of_items = [int(x.strip(",")) for x in temp_line[2:]]
        elif temp_line[-2] == "*":
            temp_moneky.operation = "mul"
            try:
                temp_moneky.operation_value = int(temp_line[-1].strip())
            except:
                temp_moneky.operation_value = temp_line[-1].strip()
        elif temp_line[-2] == "+":
            temp_moneky.operation = "plus"
            try:
                temp_moneky.operation_value = int(temp_line[-1].strip())
            except:
                temp_moneky.operation_value = temp_line[-1].strip()
        elif temp_line[0] == "Test:":
            temp_moneky.test_value = int(temp_line[-1].strip())
        elif temp_line[1] == "true:":
            temp_moneky.true_target = int(temp_line[-1])
        elif temp_line[1] == "false:":
            temp_moneky.false_target = int(temp_line[-1])
    
    instructions.append(temp_moneky)
    return instructions

def part1(instructions, division_switch, round_count):
    p2_divisor = find_divisor(instructions)
    for i in range(round_count):
        for checked_monkey in instructions:
            while len(checked_monkey.list_of_items) != 0:
                returned_item, target_monkey = checked_monkey.inspect_item(division_switch, p2_divisor)
                instructions[target_monkey].list_of_items.append(returned_item)
    monkey_results = []
    for checked_monkey in instructions:
        monkey_results.append(checked_monkey.items_inspected)
    monkey_results.sort()
    monkey_business = monkey_results[-1] * monkey_results[-2]
    print(monkey_business)
    return 0

def find_divisor(instructions):
    temp = 1
    for monkey in instructions:
        temp *= monkey.test_value
    return temp

class Monkey():
    def __init__(self):
        self.list_of_items = []
        self.operation = None
        self.operation_value = None
        self.test_value = None
        self.true_target = None
        self.false_target = None
        self.items_inspected = 0
     
    def inspect_item(self, division_switch, p2_divisor):
            # Get the last item
            currently_inspected_item = self.list_of_items.pop(0)
            # Increase inspect items counter
            self.items_inspected += 1
            # Run the numerical operation
            if self.operation == "mul":
                if self.operation_value == "old":
                    worry_level = currently_inspected_item * currently_inspected_item
                else:
                    worry_level = currently_inspected_item * self.operation_value
            elif self.operation == "plus":
                if self.operation_value == "old":
                    worry_level = currently_inspected_item + currently_inspected_item
                else:
                    worry_level = currently_inspected_item + self.operation_value
            if division_switch == True:
                worry_level = worry_level // 3
            
            else:
                worry_level = worry_level % p2_divisor
            
            # return updated item and target monkey
            if worry_level % self.test_value == 0:
                return worry_level, self.true_target
            else:
                return worry_level, self.false_target


main()
