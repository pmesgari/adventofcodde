import os
import argparse
import subprocess

def run_solution(year, day, test=False):
    input_file = 'test.txt' if test else 'in.txt'
    solution_file = f"{year}/day{day}.py"

    if not os.path.exists(solution_file):
        print(f"Solution file not found: {solution_file}")
        return

    # Run the solution with input redirection
    result = subprocess.run(
        ["python3", solution_file],
        stdin=open(input_file, "r"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(result.stdout, end='')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solution.")
    parser.add_argument("year", type=str, help="Year of the challenge (e.g., 2024)")
    parser.add_argument("day", type=str, help="Day of the challenge (e.g., 1)")
    parser.add_argument("--test", action="store_true", help="Run in test mode (use test.txt as input)")

    args = parser.parse_args()

    run_solution(args.year, args.day, test=args.test)
