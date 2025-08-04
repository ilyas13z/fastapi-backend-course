import json
from abc import ABC, abstractmethod

import requests


class BaseHTTPClient(ABC):
    @abstractmethod
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.url = None


class Worker(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


class AiClient(BaseHTTPClient):
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.url = (
            f"https://api.cloudflare.com/client/v4/accounts/{user_id}/ai/run/"
        )

    def get_description(self, task_name):
        with open("prompt.json", "r", encoding="utf-8") as f:
            inputs = json.load(f)["prompt_settings"]
        inputs[1]["content"] += f" {task_name}"

        input = {"messages": inputs}
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(
            f"{self.url}@cf/meta/llama-3-8b-instruct",
            headers=headers,
            json=input,
        )
        return response.json()["result"]["response"]


class JsonBinClient(BaseHTTPClient, Worker):
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.url = f"https://api.jsonbin.io/v3/b/{user_id}"

    def read(self):
        url = self.url + "/latest"
        headers = {
            "X-Master-Key": self.api_key,
            "X-Bin-Meta": "false",
        }

        req = requests.get(url, json=None, headers=headers)
        data = json.loads(req.text)
        data = {int(i): data[i] for i in data.keys()}
        return data

    def write(self, data):
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
        }

        requests.put(self.url, json=data, headers=headers)


class JsonFileWorker(Worker):
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            data = {int(i): data[i] for i in data.keys()}
        return data

    def write(self, data):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
