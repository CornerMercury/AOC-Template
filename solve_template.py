from aocd import get_data, submit
from year import YEAR

def part1(data):
    l = data.split("\n")
    return None


def part2(data):
    l = data.split("\n")
    return None


def main():
    day = int(__file__.split("\\")[-2][-2:])
    data = get_data(day=day, year=YEAR)
    p1 = part1(data)
    if p1:
        submit(p1, part="a", day=day, year=YEAR)
    p2 = part2(data)
    if p2:
        submit(p2, part="b", day=day, year=YEAR)


if __name__ == "__main__":
    main()
