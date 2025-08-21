import json
import os

PROFILES_FILE = os.path.join(os.path.dirname(__file__), "..", "profiles.json")

def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    try:
        with open(PROFILES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

def update_score(username, score):
    profiles = load_profiles()
    profiles[username] = profiles.get(username, 0) + score
    save_profiles(profiles)

def get_score(username):
    profiles = load_profiles()
    return profiles.get(username, 0)
