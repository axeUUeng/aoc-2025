from utils import run
from ocaml_bridge import run_ocaml


def answer_func(problem_input, level, test=False):
    # day 02
    return run_ocaml(2, level, problem_input)


TEST_CASES = [
    # { "input": "example", "level": 1, "output": "expected" },
]


if __name__ == "__main__":
    run(
        answer_func=answer_func,
        test_cases=TEST_CASES,
        year="2025",
        day="2",
    )
