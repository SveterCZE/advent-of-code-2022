def main():
    root = get_input()
    part1(root)
    part2(root)

def get_input():
    f = open("input.txt", "r")
    # initialise the root
    root = Folder("/", None)
    # set the present working directory to root
    pwd = root
    for line in f:
        instruction_line = line.strip().split()
        # if command is selected
        if instruction_line[0] == "$":
            if instruction_line[1] == "cd":
                if instruction_line[2] == "/":
                    pwd = root
                elif instruction_line[2] == "..":
                    pwd = pwd.parent
                else:
                    pwd = pwd.leaves[instruction_line[2]]
        # if folder / file is selected
        else:
            if instruction_line[0] == "dir":
                # Create a new directory
                new_dir = Folder(instruction_line[1], pwd)
                # Add a link the directory to the parent Folder
                pwd.add_new_item(new_dir)
            else:
                new_file = File(instruction_line[1], pwd, int(instruction_line[0]))
                pwd.add_new_item(new_file)
                pwd.increase_size_new_file(new_file.size)
    return root

def part1(root):
    print(root.find_sum_small_folders(100000))
    return 0

def part2(root):
    space_to_be_deleted = 30000000 - (70000000 - root.size)
    print(root.find_folder_for_deletion(space_to_be_deleted, [root.size]))
    return 0

class Folder:
    def __init__(self, name, parent) -> None:
        self.parent = parent
        self.name = name
        self.leaves = {}
        self.size = 0
    
    def add_new_item(self, new_item):
        self.leaves[new_item.name] = new_item
    
    def increase_size_new_file(self, new_file_size):
        self.size += new_file_size
        if self.parent != None:
            self.parent.increase_size_new_file(new_file_size)
    
    def find_sum_small_folders(self, max_folder_size):
        small_folders_size = 0
        for key, value in self.leaves.items():
            if isinstance(value, Folder):
                if value.size <= max_folder_size:
                    small_folders_size += value.size
                small_folders_size += value.find_sum_small_folders(max_folder_size)
        return small_folders_size
    
    def find_folder_for_deletion(self, space_to_be_deleted, suitable_folder_sizes):
        for key, value in self.leaves.items():
            if isinstance(value, Folder):
                if value.size >= space_to_be_deleted:
                    suitable_folder_sizes.append(value.size)
                value.find_folder_for_deletion(space_to_be_deleted, suitable_folder_sizes)
        suitable_folder_sizes.sort()
        return suitable_folder_sizes[0]

class File:
    def __init__(self, name, parent, file_size) -> None:
        self.name = name
        self.parent = parent
        self.size = file_size

main()