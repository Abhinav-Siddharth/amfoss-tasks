import requests
from tabulate import tabulate
from colorama import Fore, Style
import random
import threading
import time
from user_profile import update_score, get_score

def timed_input(prompt, timeout):
    answer = [None]

    def get_input():
        answer[0] = input(prompt)

    def countdown():
        for remaining in range(timeout, 0, -1):
            print(Fore.YELLOW + f"\rTime left: {remaining}s " + Style.RESET_ALL, end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 20 + "\r", end="", flush=True)  # Clear line after timeout

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()

    input_thread.join(timeout)
    if input_thread.is_alive():
        print(Fore.RED + "\nTime's up!" + Style.RESET_ALL)
        return None
    return answer[0]

def fetch_questions(amount=5, category=None, difficulty=None, q_type=None):
    url = f"https://opentdb.com/api.php?amount={amount}"
    if category:
        url += f"&category={category}"
    if difficulty:
        url += f"&difficulty={difficulty}"
    if q_type:
        url += f"&type={q_type}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

CATEGORY_MAP = {
    "general": None,
    "books": 10,
    "film": 11,
    "music": 12,
    "sports": 21,
    "animals": 27,
}

TYPE_MAP = {
    "multiple": "multiple",
    "boolean": "boolean"
}

def run_quiz():
    username = input("Enter your username: ").strip()
    past_score = get_score(username)
    if past_score:
        print(f"Welcome back, {username}! Your total past score is: {past_score}")
    else:
        print(f"Hello {username}, get ready for your first quiz!")

    while True:
        try:
            total_qs = int(input("How many questions? (1-20): "))
            if 1 <= total_qs <= 20:
                break
        except ValueError:
            pass
        print("Enter a valid number between 1 and 20.")

    while True:
        try:
            time_limit = int(input("Time per question in seconds (10-30): "))
            if 10 <= time_limit <= 30:
                break
        except ValueError:
            pass
        print("Enter a valid number between 10 and 30.")

    print("Categories:", ", ".join(CATEGORY_MAP.keys()))
    category_choice = input("Choose category: ").lower()
    category = CATEGORY_MAP.get(category_choice, None)

    print("Difficulty: easy, medium, hard")
    difficulty = input("Choose difficulty: ").lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = None

    print("Question type: multiple (MCQ), boolean (True/False)")
    q_type_input = input("Choose type: ").lower()
    q_type = TYPE_MAP.get(q_type_input, None)

    print("\nStarting quiz...\n")
    score = 0
    questions = fetch_questions(amount=total_qs, category=category, difficulty=difficulty, q_type=q_type)

    for q in questions:
        print(Fore.BLUE + q["question"] + Style.RESET_ALL)
        options = q.get("incorrect_answers", []) + [q.get("correct_answer")]
        random.shuffle(options)
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")

        ans = timed_input(f"Your answer (number): ", timeout=time_limit)
        if ans is None:
            print(Fore.RED + f"Skipped! Correct answer: {q['correct_answer']}" + Style.RESET_ALL)
        else:
            try:
                ans_idx = int(ans)
                if options[ans_idx - 1] == q.get("correct_answer"):
                    print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
                    score += 1
                else:
                    print(Fore.RED + f"Wrong! Answer: {q.get('correct_answer')}" + Style.RESET_ALL)
            except:
                print(Fore.RED + f"Invalid input! Correct answer: {q.get('correct_answer')}" + Style.RESET_ALL)
        print()

    print(f"Your score this round: {score}/{total_qs}")
    update_score(username, score)
    total_score = get_score(username)
    print(f"Your total cumulative score: {total_score}")
