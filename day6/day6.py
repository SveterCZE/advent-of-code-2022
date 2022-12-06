def main():
    instructions = get_input()
    part1(instructions, 4)
    part1(instructions, 14)

def get_input():
    f = open("input.txt", "r")
    for line in f:
        return line.strip()

def part1(instructions, segment_length):
    for i in range(len(instructions)):
        if len(set(instructions[i:i+segment_length])) == segment_length:
            print(i+segment_length)
            break
    return 0

main()