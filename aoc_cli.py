#!/usr/bin/env python
import argparse
import os
from pathlib import Path
import sys

# The OCaml/Python project itself lives in the nested aoc2025/ directory
ROOT = Path(__file__).resolve().parent / "aoc2025"
BIN_DIR = ROOT / "bin"
PY_DIR = ROOT / "python"


OCAML_TEMPLATE = """\
let part1 input =
  (* TODO: implement part 1 *)
  String.length input |> string_of_int

let part2 input =
  (* TODO: implement part 2 *)
  (String.length input * 2) |> string_of_int

let solve level input =
  match level with
  | 1 -> part1 input
  | 2 -> part2 input
  | _ -> failwith "Unknown part"

let read_all_stdin () =
  let buf = Buffer.create 1024 in
  (try
     while true do
       Buffer.add_string buf (input_line stdin);
       Buffer.add_char buf '\\n'
     done
   with End_of_file -> ());
  Buffer.contents buf

let () =
  if Array.length Sys.argv < 2 then
    failwith "Usage: dayXX <level>";
  let level = int_of_string Sys.argv.(1) in
  let input = read_all_stdin () in
  solve level input |> print_endline
"""

PYTHON_DAY_TEMPLATE = """\
from utils import run
from ocaml_bridge import run_ocaml


def answer_func(problem_input, level, test=False):
    # day {day:02d}
    return run_ocaml({day}, level, problem_input)


TEST_CASES = [
    # {{ "input": "example", "level": 1, "output": "expected" }},
]


if __name__ == "__main__":
    run(
        answer_func=answer_func,
        test_cases=TEST_CASES,
        year="{year}",
        day="{day}",
    )
"""


def day_str(day: int) -> str:
    return f"day{day:02d}"


def maybe_create_file(path: Path, content: str):
    if path.exists():
        print(f"Skipping existing {path}")
        return False
    path.write_text(content, encoding="utf-8")
    print(f"Created {path}")
    return True


def append_dune_stanza(day: int):
    dune_file = BIN_DIR / "dune"
    name = day_str(day)

    if not dune_file.exists():
        print(f"ERROR: {dune_file} does not exist", file=sys.stderr)
        sys.exit(1)

    content = dune_file.read_text(encoding="utf-8")
    if name in content:
        print(f"Skipping dune stanza for {name}; already present")
        return

    stanza = f"""

(executable
 (name {name})
 (public_name {name})
 (libraries))
"""
    dune_file.write_text(content + stanza, encoding="utf-8")
    print(f"Updated {dune_file} with executable {name}")


def init_day(day: int, year: int):
    name = day_str(day)

    # Paths
    ocaml_file = BIN_DIR / f"{name}.ml"
    py_file = PY_DIR / f"{name}.py"
    day_dir = ROOT / name

    # 1) OCaml solver file
    maybe_create_file(ocaml_file, OCAML_TEMPLATE)

    # 2) Update bin/dune
    append_dune_stanza(day)

    # 3) Python runner
    maybe_create_file(
        py_file,
        PYTHON_DAY_TEMPLATE.format(day=day, year=year),
    )

    # 4) Day folder (fetch will populate files later)
    day_dir.mkdir(exist_ok=True)
    print(f"Ensuring {day_dir} exists (no files created)")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aoc_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init", help="initialize a new AoC day")
    init_p.add_argument("day", type=int, help="day number, e.g. 3")
    init_p.add_argument(
        "--year",
        type=int,
        default=2025,
        help="AoC year (default: 2025)",
    )

    args = parser.parse_args(argv)

    if args.command == "init":
        init_day(args.day, args.year)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
