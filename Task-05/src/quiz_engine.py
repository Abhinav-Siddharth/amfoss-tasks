import requests
import html
import threading
import time
from rich.console import Console
from utils import get_valid_input, category_mapping

class QuizEngine:
    def __init__(self, num_questions, time_limit, category, difficulty, q_type):
        self.num_questions = get_valid_input(num_questions, 1, 20, 10)
        self.time_limit = get_valid_input(time_limit, 10, 30, 15)
        self.category = category_mapping.get(category.lower(), "") if category else ""
        self.difficulty = difficulty if difficulty in ["easy", "medium", "hard"] else ""
        self.q_type = q_type if q_type in ["multiple", "boolean"] else ""
        self.questions = self.fetch_questions()
        self.score = 0

    def fetch_questions(self):
        url = "https://opentdb.com/api.php?"
        params = {"amount": self.num_questions}
        if self.category: params["category"] = self.category
        if self.difficulty: params["difficulty"] = self.difficulty
        if self.q_type: params["type"] = self.q_type
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data["response_code"] == 0:
                return data["results"]
            else:
                print("Error fetching questions.")
                return []
        except requests.RequestException:
            print("Network error.")
            return []

    def run_quiz(self, console: Console):
        if not self.questions:
            console.print("[bold red]No questions available![/bold red]")
            return 0

        for i, question in enumerate(self.questions, 1):
            console.print(f"\n[bold blue]Question {i}/{self.num_questions}:[/bold blue] {html.unescape(question['question'])}")
            
            if question["type"] == "multiple":
                answers = question["incorrect_answers"] + [question["correct_answer"]]
                answers.sort()
                for idx, ans in enumerate(answers, 1):
                    console.print(f"[cyan]{idx}. {html.unescape(ans)}[/cyan]")
                prompt = f"[cyan]Enter answer (1-{len(answers)}): [/cyan]"
                num_answers = len(answers)
            else:
                console.print("[cyan]1. True\n2. False[/cyan]")
                prompt = "[cyan]Enter answer (1-2): [/cyan]"
                answers = ["True", "False"]
                num_answers = 2

            answer_submitted = [False]
            user_answer = [None]

            def timer():
                start_time = time.time()
                while time.time() - start_time < self.time_limit:
                    if answer_submitted[0]:
                        return
                    time.sleep(0.1)
                if not answer_submitted[0]:
                    console.print("[bold red]Time’s up![/bold red]")
                    answer_submitted[0] = True

            timer_thread = threading.Thread(target=timer)
            timer_thread.start()

            while not answer_submitted[0]:
                try:
                    user_input = console.input(prompt).strip()
                    if user_input:
                        user_answer[0] = user_input
                        answer_submitted[0] = True
                except KeyboardInterrupt:
                    answer_submitted[0] = True

            timer_thread.join()

            correct_answer = question["correct_answer"]
            if user_answer[0] and user_answer[0].isdigit():
                idx = int(user_answer[0]) - 1
                if 0 <= idx < num_answers:
                    selected = answers[idx]
                    if selected == correct_answer:
                        console.print("[bold green]Correct![/bold green]")
                        self.score += 1
                    else:
                        console.print(f"[bold red]Wrong! Correct: {html.unescape(correct_answer)}[/bold red]")
                else:
                    console.print(f"[bold red]Invalid. Correct: {html.unescape(correct_answer)}[/bold red]")
            else:
                console.print(f"[bold red]No answer. Correct: {html.unescape(correct_answer)}[/bold red]")

        return self.score
