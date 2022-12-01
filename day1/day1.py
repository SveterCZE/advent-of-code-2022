def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def get_input():
    instructions = []
    temp_figure = 0
    f = open("input.txt", "r")
    for line in f:
        if len(line) == 1:
            instructions.append(temp_figure)
            temp_figure = 0
        else:
            temp_figure += int(line.strip())
    return instructions

def part1(instructions):
    print(max(instructions))
    return 0

def part2(instructions):
    instructions.sort()
    print(sum(instructions[-3:]))
    return 0

main()
