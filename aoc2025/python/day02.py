from utils import run
from ocaml_bridge import run_ocaml


def answer_func(problem_input, level, test=False):
    # day 02
    return run_ocaml(2, level, problem_input)


TEST_CASES = [
    { "input": "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
     "level": 1, "output": 1227775554 },
      { "input": "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
     "level": 2, "output": 4174379265 },
]


if __name__ == "__main__":
    run(
        answer_func=answer_func,
        test_cases=TEST_CASES,
        year="2025",
        day="2",
    )
