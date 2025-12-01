from utils import run
from ocaml_bridge import run_ocaml

def answer_func(problem_input, level, test=False):
    return run_ocaml(1, level, problem_input)

TEST_CASES = [
    {
        "input": "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n",
        "level": 1,
        "output": 3,
    },
     {
        "input": "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n",
        "level": 2,
        "output": 6,
    },
]

if __name__ == "__main__":
    run(answer_func, test_cases=TEST_CASES, year="2025", day="1")
