from time import perf_counter_ns as timer
from os import path, system
from importlib import import_module
from aocd import get_data, exceptions

YEAR = 2023


def get_filename(days=[i for i in range(1, 26)]):
    name = "_"
    while name not in " ." and not any(
        path.exists(f"day{day:02}/{name}") for day in days
    ):
        name = input("Enter filename to time: ")

    if not all(path.exists(f"day{day:02}/{name}") for day in days):
        choice = input("Not all days have that file, continue (y/n)? ")[0].lower()
        if choice != "y":
            name = get_filename(days)

    return name.split(".")[0]


def time_single(path, day, n=10):
    file = import_module(path)
    data = get_data(day=day, year=YEAR)

    dt1 = dt2 = 0
    for _ in range(n):
        start = timer()
        file.part1(data)
        dt1 += timer() - start

        start = timer()
        file.part2(data)
        dt2 += timer() - start

    return dt1 // n, dt2 // n


def output_times(lst):
    day_totals = list(map(lambda x: (x[0], x[1] + x[2]), lst))
    total_time = sum(map(lambda x: x[1], day_totals)) / 1000**3
    ns_to_ms = 1000**2

    print()
    print(" day | part1 (ms) | part2 (ms) | total (ms) ")
    print("-----+------------+------------+------------")
    for day, dt1, dt2 in lst:
        total = (dt1 + dt2) / ns_to_ms
        dt1 = dt1 / ns_to_ms
        dt2 = dt2 / ns_to_ms
        print(f" {day:<3} | {dt1:<10.3f} | {dt2:<10.3f} | {total:<10.3f} ")

    print()
    print(f"Total time: {total_time:.3f}s")
    print()


def main():
    inp = ""
    while inp != "q":
        inp = input("Time all, Time single or quit (a/s/q): ")[0].lower()
        match inp:
            case "s":
                day = "0"
                while not (day.isnumeric()) or not (1 <= int(day) <= 25):
                    day = input("Enter day to time: ")
                day = int(day)
                path = f"day{day:02}.{get_filename([day])}"
                try:
                    dt1, dt2 = time_single(path, day)
                    output_times([(day, dt1, dt2)])
                except exceptions.PuzzleLockedError:
                    print(f"Day {day} is locked")

            case "a":
                filename = get_filename()
                results = []
                for day in range(1, 26):
                    system("cls")
                    print(f"|{'█' * day}{' ' * (25 - day)}| {day*4}%")
                    try:
                        times = time_single(f"day{day:02}.{filename}", day)
                    except ModuleNotFoundError:
                        continue
                    except exceptions.PuzzleLockedError:
                        continue
                    results.append((day, *times))

                output_times(results)
                print("Worst days")
                print("‾‾‾‾‾‾‾‾‾‾")
                worst_times = sorted(results, key=lambda x: x[0] + x[1], reverse=True)[
                    :3
                ]
                output_times(worst_times)


if __name__ == "__main__":
    main()
