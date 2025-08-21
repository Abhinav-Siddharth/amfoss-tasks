import threading
import time
from colorama import Fore, Style

def timed_input(prompt, timeout):
    answer = [None]

    def get_input():
        answer[0] = input(prompt)

    def countdown():
        for remaining in range(timeout, 0, -1):
            print(Fore.YELLOW + f"Time left: {remaining}s" + Style.RESET_ALL)
            time.sleep(1)

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()

    input_thread.join(timeout)
    if input_thread.is_alive():
        print(Fore.RED + "Time's up!" + Style.RESET_ALL)
        return None
    return answer[0]
