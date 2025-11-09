import json, os

HISTORY_PATH = "data_history.json"

def save_history(results):
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump([], f)
    with open(HISTORY_PATH, "r") as f:
        data = json.load(f)
    data.append(results)
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r") as f:
        return json.load(f)