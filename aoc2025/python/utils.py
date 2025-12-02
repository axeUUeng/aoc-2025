# This file includes code from aoc_utils (MIT License, 2019)
# https://github.com/loganmeetsworld/advent-of-code-utils.git

from bs4 import BeautifulSoup
from colorama import Fore, Style
from pathlib import Path
import os
import requests
import time

PYTHON_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PYTHON_DIR.parent
HEADERS = {"cookie": f"session={os.environ['SESSION_COOKIE']}"}


def day_dir(day):
    target = PROJECT_ROOT / f"day{int(day):02d}"
    target.mkdir(parents=True, exist_ok=True)
    return target


def request_content(year, day, content_type):
    if content_type == 'input':
        url = f"https://adventofcode.com/{year}/day/{day}/input"
    elif content_type == 'problem':
        url = f"https://adventofcode.com/{year}/day/{day}"

    response = requests.get(url, headers=HEADERS)
    handle_error_status(response.status_code)
    return response.text.strip()


def fetch(year, day, content_type):
    content = request_content(year, day, content_type)
    if content_type == 'input':
        return content
    elif content_type == 'problem':
        soup = BeautifulSoup(content, "html.parser")
        return '\n\n\n'.join([a.text for a in soup.select('article')])


def save(year, day, content_type):
    content = fetch(year, day, content_type)
    target_dir = day_dir(day)
    target_path = target_dir / f"{content_type}.txt"
    with target_path.open("w") as text_file:
        text_file.write(content)

    return content


def fetch_and_save(year, day):
    target_dir = day_dir(day)
    input_path = target_dir / "input.txt"

    if input_path.exists():
        print("\n🛷  Found input locally, using saved input 🛷 \n")
        with input_path.open() as file:
            return file.read()
    else:
        print("\n🛷  Input not found, fetching 🛷 \n")
        problem_text = save(year, day, content_type="problem")
        print(f"\n{problem_text}\n")
        return save(year, day, content_type="input")


def submit(answer, level, year, day):
    print(f"\nFor Day {day}, Part {level}, we are submitting answer: {answer}\n")
    data = {"level": str(level), "answer": str(answer)}
    response = requests.post(f"https://adventofcode.com/{year}/day/{day}/answer", headers=HEADERS, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    message = soup.article.text

    if "that's the right answer" in message.lower():
        print(f"\n{Fore.GREEN}Correct! ⭐️{Style.RESET_ALL}")
        star_path = day_dir(day)
        with (star_path / "stars.txt").open("w+") as text_file:
            print("Writing '*' to star file...")
            if level == 1:
                text_file.write('*')
            elif level == 2:
                text_file.write('**')

        if level == 1:
            print("Updated problem with part 2:\n\n")
            print(save(year, day, 'problem'))
    elif "not the right answer" in message.lower():
        print(f"\n{Fore.RED}Wrong answer 🎅🏾🙅🏼‍♀️! For details:\n{Style.RESET_ALL}")
        print(message)
    elif "answer too recently" in message.lower():
        print(f"\n{Fore.YELLOW}You gave an answer too recently{Style.RESET_ALL}")
    elif "already complete it" in message.lower():
        print(f"\n{Fore.YELLOW}You have already solved this. Make sure a local stars.txt file is present that reflects your stars for this problem.{Style.RESET_ALL}")


def test(answer_func, cases):
    all_passed = True

    if not cases:
        print("Livin' on the edge! No test cases defined.")
        return all_passed

    for tc in cases:
        start = time.time()
        answer = answer_func(tc['input'], tc['level'], test=True)
        end = time.time()
        if str(tc['output']) == str(answer):
            print(f"{Fore.GREEN}🎄 Test passed {Style.RESET_ALL}[Part {tc['level']}] Input: '{tc['input']}'; Output: '{tc['output']}'")
        else:
            all_passed = False
            print(f"{Fore.RED}🔥 Test failed {Style.RESET_ALL}[Part {tc['level']}] Input: '{tc['input']}'; Submitted: '{answer}'; Correct: '{tc['output']}'")

        print(f"\n⏰ Test for level {tc['level']} took {float(end - start)} to run.\n")
    return all_passed


def check_stars(day):
    star_path = day_dir(day)
    star_file = star_path / "stars.txt"
    if star_file.exists():
        with star_file.open('r') as file:
            stars = file.read().strip()
            return len(stars)


def handle_error_status(code):
    if code == 404:
        print(f"{Fore.RED}{code}: This day is not available yet!{Style.RESET_ALL}")
        quit()
    elif code == 400:
        print(f"{Fore.RED}{code}: Bad credentials!{Style.RESET_ALL}")
        quit()
    elif code > 400:
        print(f"{Fore.RED}{code}: General error!{Style.RESET_ALL}")
        quit()


def run(answer_func, test_cases=None, year=None, day=None):
    if not year and not day:
        cwd = Path.cwd()
        year, day = cwd.parent.name, cwd.name

    problem_input = fetch_and_save(year, day)

    if test(answer_func, test_cases):
        print("\n🍾 Now looking to submit your answers 🍾\n")
        stars = check_stars(day)
        if not stars:
            level = 1
            start = time.time()
            answer = answer_func(problem_input, level)
            end = time.time()
            print(f"⏰ Part 1 took {float(end - start)} to run.")
            print(f"🙇‍♀️ You are submitting your answer to part 1 of this puzzle. \nDo you want to submit part 1 (y/n)? P1: {answer}")
            submit_answer = input()
            if submit_answer == 'y':
                submit(answer, level, year, day)
        elif stars == 1:
            level = 2
            start = time.time()
            answer = answer_func(problem_input, level)
            end = time.time()
            print(f"⏰ Part 1 took {float(end - start)} to run.")
            print(f"👯‍♀️  It seems we've been here before and you've submitted one answer ⭐️ \nDo you want to submit part 2 (y/n)? P2: {answer}")
            submit_answer = input()
            if submit_answer == 'y':
                submit(answer, level, year, day)
        else:
            print("It seems we've been here before and you've submitted both answers! ⭐️⭐️\n")
    else:
        print("\n🤷‍♀️ You know the rules. Tests don't pass, YOU don't pass.\n")
