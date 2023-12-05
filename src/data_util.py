import json


def get_data(username) -> dict:
    with open(f"data/{username}.json", "r") as f:
        return json.load(f)



def save_data(username: str, data: dict) -> bool:
    with open(f"data/{username}.json", "r") as f:
        temp = json.load(f)

    try:
        with open(f"data/{username}.json", "r") as f:
            json.dump(data, f, indent=4)
        return True

    except: # Prevent data loss on failure
        with open(f"data/{username}.json", "w") as f:
            json.dump(temp, f, indent=4)
        return False
