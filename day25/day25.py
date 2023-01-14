def main():
    instructions  = get_input()
    part1(instructions)

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions):
    snafu_sum = 0
    for snafu in instructions:
        snafu.reverse()
        snafu_sum += convert_snafu_to_decimal(snafu)
    snafu_sum = 2022
    print(convert_decimal_to_snafu(snafu_sum))
    return 0

def convert_snafu_to_decimal(snafu):
    decimal_figure = 0
    for i in range(len(snafu)):
        if snafu[i] == "0":
            pass
        elif snafu[i] == "1":
            decimal_figure += pow(5, i)
        elif snafu[i] == "2":
            decimal_figure += (pow(5, i) * 2)
        elif snafu[i] == "-":
            decimal_figure -= pow(5, i)
        elif snafu[i] == "=":
            decimal_figure -= (pow(5, i) * 2)
    return decimal_figure

def convert_decimal_to_snafu(snafu_sum):
    converted_snafu = []
    counter = 1
    while True:
        snafu_sum_mod = snafu_sum % 5
        if snafu_sum_mod == 1:
            converted_snafu.append("1")
        elif snafu_sum_mod == 2:
            converted_snafu.append("2")
        elif snafu_sum_mod == 3:
            converted_snafu.append("=")
        elif snafu_sum_mod == 4:
            converted_snafu.append("-")
        elif snafu_sum_mod == 5:
            converted_snafu.append("0")
        # snafu_sum -= snafu_sum_mod
        snafu_sum = snafu_sum // 5
        counter += 1

main()