import requests
from tabulate import tabulate
from colorama import Fore, Style

API_URL = "https://opentdb.com/api.php?amount=5&type=multiple"

def fetch_questions():
    """Fetch quiz questions from Open Trivia API."""
    response = requests.get(API_URL)
    data = response.json()
    return data.get("results", [])

def run_quiz():
    """Run the interactive quiz."""
    questions = fetch_questions()

    if not questions:
        print(Fore.RED + "No questions fetched. Check your internet or API." + Style.RESET_ALL)
        return

    score = 0
    for idx, q in enumerate(questions, start=1):
        print(f"\nQuestion {idx}: {q['question']}")
        options = q['incorrect_answers'] + [q['correct_answer']]
        # Shuffle to randomize
        import random
        random.shuffle(options)

        table = [[i + 1, opt] for i, opt in enumerate(options)]
        print(tabulate(table, headers=["Option", "Answer"], tablefmt="fancy_grid"))

        try:
            choice = int(input("Choose your answer (1-4): "))
            if options[choice - 1] == q['correct_answer']:
                print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
                score += 1
            else:
                print(Fore.RED + f"Wrong! Correct answer: {q['correct_answer']}" + Style.RESET_ALL)
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid input! Skipping question." + Style.RESET_ALL)

    print(f"\nYour final score: {score}/{len(questions)}")

