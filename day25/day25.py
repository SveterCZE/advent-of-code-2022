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
    snafu_conversion_table_to_decimal = create_snafu_conversion_table_to_decimal()
    snafu_conversion_table_to_snafu = create_snafu_conversion_table_to_snafu()
    for elem in instructions:
        elem.reverse()
    snafu_sum = instructions[0]
    for i in range(1, len(instructions)):
        snafu_sum = sum_two_snafus(snafu_sum, instructions[i], snafu_conversion_table_to_decimal, snafu_conversion_table_to_snafu)
    snafu_sum.reverse()
    snafu_converted = ""
    for elem in snafu_sum:
        snafu_converted+= elem
    print(snafu_converted)
    return 0

def sum_two_snafus(snafu1, snafu2, snafu_conversion_table_to_decimal, snafu_conversion_table_to_snafu):
    new_snafu_sum = []
    if len(snafu1) > len(snafu2):
        long_snafu = snafu1
        short_snafu = snafu2
    else:
        long_snafu = snafu2
        short_snafu = snafu1
    for i in range(len(long_snafu)):
        new_snafu_sum.append("0")
    for i in range(len(long_snafu)):
        carry_over = 0
        # Sum two snafus from the same position and add carry-overs from previous calculations
        try:
            two_snafus_sum = snafu_conversion_table_to_decimal[long_snafu[i]] + snafu_conversion_table_to_decimal[short_snafu[i]] + snafu_conversion_table_to_decimal[new_snafu_sum[i]]
        except:
            two_snafus_sum = snafu_conversion_table_to_decimal[long_snafu[i]] + snafu_conversion_table_to_decimal[new_snafu_sum[i]]
        # Calculate carry overs, if any
        if two_snafus_sum == 3:
            carry_over = 1
            two_snafus_sum = -2
        elif two_snafus_sum == 4:
            carry_over = 1
            two_snafus_sum = -1
        elif two_snafus_sum == 5:
            carry_over = 1
            two_snafus_sum = 0
        elif two_snafus_sum == -3:
            carry_over = -1
            two_snafus_sum = 2
        elif two_snafus_sum == -4:
            carry_over = -1
            two_snafus_sum = 1
        elif two_snafus_sum == -5:
            carry_over = -1
            two_snafus_sum = 0
        # Insert the sum of snafus into the snafu sum calculator
        new_snafu_sum[i] = snafu_conversion_table_to_snafu[two_snafus_sum]
        # Insert the carry-over, if relevant
        if carry_over != 0:
            try:
                new_snafu_sum[i+1] = snafu_conversion_table_to_snafu[carry_over]
            except:
                new_snafu_sum.append(snafu_conversion_table_to_snafu[carry_over])
    return new_snafu_sum

def create_snafu_conversion_table_to_decimal():
    snafu_convesion_table = {}
    snafu_convesion_table["0"] = 0
    snafu_convesion_table["1"] = 1
    snafu_convesion_table["2"] = 2
    snafu_convesion_table["-"] = -1
    snafu_convesion_table["="] = -2
    return snafu_convesion_table

def create_snafu_conversion_table_to_snafu():
    snafu_convesion_table = {}
    snafu_convesion_table[0] = "0"
    snafu_convesion_table[1] = "1"
    snafu_convesion_table[2] = "2"
    snafu_convesion_table[-1] = "-"
    snafu_convesion_table[-2] = "="
    return snafu_convesion_table

# def convert_snafu_to_decimal(snafu):
#     decimal_figure = 0
#     for i in range(len(snafu)):
#         if snafu[i] == "0":
#             pass
#         elif snafu[i] == "1":
#             decimal_figure += pow(5, i)
#         elif snafu[i] == "2":
#             decimal_figure += (pow(5, i) * 2)
#         elif snafu[i] == "-":
#             decimal_figure -= pow(5, i)
#         elif snafu[i] == "=":
#             decimal_figure -= (pow(5, i) * 2)
#     return decimal_figure

main()