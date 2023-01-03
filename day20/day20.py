def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input()
    part2(instructions)

def get_input():
    instructions = CircularList()
    f = open("input.txt", "r")
    for line in f:
        instructions.add_new_item(int(line))
    instructions.last_inserted_item.next_value = instructions.first_inserted_item
    instructions.first_inserted_item.previous_value = instructions.last_inserted_item
    return instructions

def part1(instructions):
    iterate_over_items_in_list(instructions)
    print(calculate_sum_of_relevant_figures(instructions))
    return 0

def part2(instructions):
    encrypt_input(instructions)
    for i in range(10):
        iterate_over_items_in_list(instructions)
    print(calculate_sum_of_relevant_figures(instructions))
    return 0

def encrypt_input(instructions):
    decryption_key = 811589153
    for i in range(instructions.get_circular_list_length()):
        currently_moved_node = instructions.get_node_by_order(i)
        currently_moved_node.node_value = currently_moved_node.node_value * decryption_key

def calculate_sum_of_relevant_figures(instructions):
    checked_figure = instructions.find_zero_value()
    sum_of_relevant_figures = 0
    for i in range(1,3001):
        checked_figure = checked_figure.next_value
        if i % 1000 == 0:
            sum_of_relevant_figures += checked_figure.get_node_value()
    return sum_of_relevant_figures

def iterate_over_items_in_list(instructions):
    for i in range(instructions.get_circular_list_length()):
        currently_moved_node = instructions.get_node_by_order(i)
        if currently_moved_node.get_node_value() > 0:
            currently_moved_node.move_node_right(currently_moved_node.get_node_value(), instructions.get_circular_list_length())
        elif currently_moved_node.get_node_value() < 0:
            currently_moved_node.move_node_left(currently_moved_node.get_node_value(), instructions.get_circular_list_length())
        else:
            pass

class CircularList:
    def __init__(self):
        self.counter = 0
        self.first_inserted_item = None
        self.last_inserted_item = None

    def add_new_item(self, inserted_value):
        new_node = CircularNode(self.counter, inserted_value, self.last_inserted_item)
        if self.first_inserted_item == None:
            self.first_inserted_item = new_node
        if new_node.previous_value != None:
            new_node.previous_value.next_value = new_node
        self.last_inserted_item = new_node
        self.counter += 1
    
    def get_circular_list_length(self):
        return self.counter
    
    def get_node_by_order(self, searched_node_order):
        currently_checked_node = self.first_inserted_item
        while True:
            if currently_checked_node.get_circular_order() == searched_node_order:
                return currently_checked_node
            else:
                currently_checked_node = currently_checked_node.next_value
    
    def find_zero_value(self):
        currently_checked_node = self.first_inserted_item
        while True:
            if currently_checked_node.get_node_value() == 0:
                return currently_checked_node
            else:
                currently_checked_node = currently_checked_node.next_value

class CircularNode:
    def __init__(self, circular_order, node_value, previous_value):
        self.circular_order = circular_order
        self.node_value = node_value
        self.previous_value = previous_value
        self.next_value = None
    
    def move_node_right(self, move_count, list_len):
        for i in range(move_count % (list_len - 1)):
            left_node = self.previous_value
            node_moving_left = self.next_value
            right_node = self.next_value.next_value

            left_node.next_value = node_moving_left
            node_moving_left.previous_value = left_node

            right_node.previous_value = self
            self.next_value = right_node

            node_moving_left.next_value = self
            self.previous_value = node_moving_left

    def move_node_left(self, move_count, list_len):
        for i in range(abs(move_count) % (list_len - 1)):
            left_node = self.previous_value.previous_value
            node_moving_right = self.previous_value
            right_node = self.next_value

            left_node.next_value = self
            self.previous_value = left_node

            right_node.previous_value = node_moving_right
            node_moving_right.next_value = right_node

            self.next_value = node_moving_right
            node_moving_right.previous_value = self


    def get_circular_order(self):
        return self.circular_order
    
    def get_node_value(self):
        return self.node_value


main()