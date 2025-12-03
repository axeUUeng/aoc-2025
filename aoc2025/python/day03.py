from utils import run
from ocaml_bridge import run_ocaml


def answer_func(problem_input, level, test=False):
    # day 03
    return run_ocaml(3, level, problem_input)


TEST_CASES = [
    { "input": "987654321111111\n811111111111119\n234234234234278\n818181911112111\n", "level": 1,
     "output": 357 },
       { "input": "987654321111111\n811111111111119\n234234234234278\n818181911112111\n", "level": 2,
     "output": 3121910778619 },
]


if __name__ == "__main__":
    run(
        answer_func=answer_func,
        test_cases=TEST_CASES,
        year="2025",
        day="3",
    )
