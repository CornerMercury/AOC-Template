from time import perf_counter_ns as timer
from os import path, system
from importlib import import_module
from aocd import get_data, exceptions
import argparse
from year import YEAR

def time_single(path, n):
    file = import_module(path)
    day = int(path.split(".")[-2][-2:])
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
    parser = argparse.ArgumentParser(description="Handle script arguments.")
    parser.add_argument("singleDefault", nargs="*", metavar=("DAY", "FILENAME"), help="Time a specific day and file.", default=None)
    parser.add_argument("-a", "--all", metavar="FILENAME", nargs="?", const="",
                        help="Time all days for a given filename.")
    parser.add_argument("-s", "--single", nargs=2, metavar=("DAY", "FILENAME"), 
                        help="Time a specific day and file.")
    parser.add_argument("-c", "--compare", nargs=3, metavar=("DAY", "FILENAME1", "FILENAME2"), 
                        help="Compare two files for a specific day.")
    parser.add_argument("-n", type=int, default=1, help="Number of iterations (default: 1).")
    
    args = parser.parse_args()
    n = args.n
    if args.single or args.singleDefault:
        day, filename = args.single if args.single else args.singleDefault
        path = f"day{int(day):02}.{filename}"
        try:
            dt1, dt2 = time_single(path, n)
            output_times([(str(day), dt1, dt2)])
        except exceptions.PuzzleLockedError:
            print(f"Day {day} is locked")

    elif args.all:
        filename = args.all
        results = []
        for day in range(1, 26):
            system("cls")
            print(f"|{'█' * day}{' ' * (25 - day)}| {day*4}%")
            try:
                times = time_single(f"day{day:02}.{filename}", n)
            except ModuleNotFoundError:
                continue
            except exceptions.PuzzleLockedError:
                continue
            results.append((str(day), *times))

        output_times(results)
        print("Worst days")
        print("‾‾‾‾‾‾‾‾‾‾")
        worst_times = sorted(results, key=lambda x: x[1] + x[2], reverse=True)[
            :3
        ]
        output_times(worst_times)
    elif args.compare:
        day, f1, f2 = args.compare
        try:
            t1 = time_single(f"day{day:02}.{f1}", n)
            t2 = time_single(f"day{day:02}.{f1}", n)
            output_times([(f1, *t1), (f2, *t2)], first_header="filename")
            percent = (sum(t1) / sum(t2)) * 100 - 100
            print(
                f"{f2} is {abs(percent):.2f}% {'faster' if percent > 0 else 'slower'}"
            )
        except exceptions.PuzzleLockedError:
            print(f"Day {day} is locked")


if __name__ == "__main__":
    main()
