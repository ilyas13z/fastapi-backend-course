import json


def read_tasks():
    with open("tasks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        data = {int(i): data[i] for i in data.keys()}
    return data


def write_tasks(data):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
