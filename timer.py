from time import perf_counter_ns as timer
from os import path, system
from importlib import import_module
from aocd import get_data, exceptions

YEAR = 2023


def get_day():
    day = "0"
    while not (day.isnumeric()) or not (1 <= int(day) <= 25):
        day = input("Enter day: ")

    return int(day)


def get_filename(days=[i for i in range(1, 26)]):
    name = "_"
    while name not in " ." and not any(
        path.exists(f"day{day:02}/{name}.py") for day in days
    ):
        name = input("Enter filename (without extension): ")

    if not all(path.exists(f"day{day:02}/{name}.py") for day in days):
        choice = input("Not all days have that file, continue (y/n)? ")[0].lower()
        if choice != "y":
            name = get_filename(days)

    return name


def time_single(path, n=100):
    file = import_module(path)
    data = get_data(day=int(path.split(".")[-2][-2:]), year=YEAR)

    dt1 = dt2 = 0
    for _ in range(n):
        start = timer()
        file.part1(data)
        dt1 += timer() - start

        start = timer()
        file.part2(data)
        dt2 += timer() - start

    return dt1 // n, dt2 // n


def output_times(lst, first_header="day"):
    day_totals = list(map(lambda x: (x[0], x[1] + x[2]), lst))
    total_time = sum(map(lambda x: x[1], day_totals)) / 1000**3
    ns_to_ms = 1000**2
    max_header_length = max(
        map(len, [first_header] + list(map(lambda x: str(x[0]), lst)))
    )
    print()
    print(
        f" {first_header.ljust(max_header_length)} | part1 (ms) | part2 (ms) | total (ms) "
    )
    print(f"-{'-' * max_header_length}-+------------+------------+------------")
    for day, dt1, dt2 in lst:
        total = (dt1 + dt2) / ns_to_ms
        dt1 = dt1 / ns_to_ms
        dt2 = dt2 / ns_to_ms
        print(
            f" {day.ljust(max_header_length)} | {dt1:<10.3f} | {dt2:<10.3f} | {total:<10.3f} "
        )

    print()
    print(f"Total time: {total_time:.3f}s")
    print()


def main():
    inp = ""
    while inp != "q":
        inp = input("Time all, time single, compare times or quit (a/s/c/q): ")[
            0
        ].lower()
        match inp:
            case "s":
                day = get_day()
                path = f"day{day:02}.{get_filename([day])}"
                try:
                    dt1, dt2 = time_single(path)
                    output_times([(str(day), dt1, dt2)])
                except exceptions.PuzzleLockedError:
                    print(f"Day {day} is locked")

            case "a":
                filename = get_filename()
                results = []
                for day in range(1, 26):
                    system("cls")
                    print(f"|{'█' * day}{' ' * (25 - day)}| {day*4}%")
                    try:
                        times = time_single(f"day{day:02}.{filename}")
                    except ModuleNotFoundError:
                        continue
                    except exceptions.PuzzleLockedError:
                        continue
                    results.append((str(day), *times))

                output_times(results)
                print("Worst days")
                print("‾‾‾‾‾‾‾‾‾‾")
                worst_times = sorted(results, key=lambda x: x[0] + x[1], reverse=True)[
                    :3
                ]
                output_times(worst_times)
            case "c":
                day = get_day()
                f1 = get_filename([day])
                print("Successfully added file")
                f2 = get_filename([day])
                try:
                    t1 = time_single(f"day{day:02}.{f1}")
                    t2 = time_single(f"day{day:02}.{f1}")
                    output_times([(f1, *t1), (f2, *t2)], first_header="filename")
                    percent = (sum(t1) / sum(t2)) * 100 - 100
                    print(
                        f"{f2} is {abs(percent):.2f}% {'faster' if percent > 0 else 'slower'}"
                    )
                except exceptions.PuzzleLockedError:
                    print(f"Day {day} is locked")


if __name__ == "__main__":
    main()
