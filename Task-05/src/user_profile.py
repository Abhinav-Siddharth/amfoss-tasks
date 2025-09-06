import json
import os

class UserProfile:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.profiles_file = "../profiles.json"
        self.load_profile()

    def load_profile(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r") as f:
                    profiles = json.load(f)
                    self.score = profiles.get(self.username, 0)
            except (json.JSONDecodeError, IOError):
                self.score = 0

    def update_score(self, new_score):
        self.score += new_score

    def save_profile(self):
        profiles = {}
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r") as f:
                    profiles = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        profiles[self.username] = self.score
        try:
            with open(self.profiles_file, "w") as f:
                json.dump(profiles, f, indent=4)
        except IOError:
            print("Error saving profile.")
