from rich.console import Console
from quiz_engine import QuizEngine
from user_profile import UserProfile

def main():
    console = Console()
    console.print("[bold magenta]Welcome to TimeTickQuiz - A Magic Library Adventure![/bold magenta]")
    
    username = console.input("[cyan]Enter your username: [/cyan]").strip()
    profile = UserProfile(username)
    
    console.print("\n[bold]Customize your quiz:[/bold]")
    num_questions = console.input("[cyan]How many questions (1-20)? [/cyan]")
    time_limit = console.input("[cyan]Time per question (10-30 seconds)? [/cyan]")
    category = console.input("[cyan]Category (e.g., animals, history, leave blank for any): [/cyan]").strip()
    difficulty = console.input("[cyan]Difficulty (easy, medium, hard, leave blank for any): [/cyan]").strip().lower()
    q_type = console.input("[cyan]Question type (multiple, boolean, leave blank for any): [/cyan]").strip().lower()
    
    quiz = QuizEngine(num_questions, time_limit, category, difficulty, q_type)
    score = quiz.run_quiz(console)
    
    profile.update_score(score)
    profile.save_profile()
    
    console.print(f"\n[bold yellow]Quiz Complete, {username}! Your score: {score}/{quiz.num_questions}[/bold yellow]")
    if score == quiz.num_questions:
        console.print("[bold green]Perfect score! You’ve earned the Golden Star! 🌟[/bold green]")
    elif score >= quiz.num_questions // 2:
        console.print("[bold blue]Great job! Keep practicing to win the Golden Star! 📚[/bold blue]")
    else:
        console.print("[bold red]Nice try! The books await your return! 📖[/bold red]")

if __name__ == "__main__":
    main()
