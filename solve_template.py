from aocd import get_data, submit

DAY = 1
YEAR = 2023


def part1(l):
    return None


def part2(l):
    return None


def main():
    data = get_data(day=DAY, year=YEAR)
    lst = data.split("\n")
    p1 = part1(lst)
    if p1:
        submit(p1, part="a", day=DAY, year=YEAR)
    p2 = part2(lst)
    if p2:
        submit(p2, part="b", day=DAY, year=YEAR)


if __name__ == "__main__":
    main()
