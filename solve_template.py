from aocd import get_data, submit

DAY = 1
YEAR = 2023
data = get_data(day=DAY, year=YEAR)


def part1():
    return None


def part2():
    return None


def main():
    p1 = part1()
    if p1:
        submit(p1, part="a", day=DAY, year=YEAR)
    p2 = part2()
    if p2:
        submit(p2, part="b", day=DAY, year=YEAR)


main()
