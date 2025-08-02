import json
import requests
from abc import ABC, abstractmethod


class Worker(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


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


class JsonBinWorker(Worker):
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://api.jsonbin.io/v3/b/688dc3b0f7e7a370d1f21822'
    
    def read(self):
        url = self.url + '/latest'
        headers = {
        'X-Master-Key': self.api_key,
        'X-Bin-Meta': 'false',
        }

        req = requests.get(url, json=None, headers=headers)
        data = json.loads(req.text)
        data = {int(i): data[i] for i in data.keys()}
        return data
    
    def write(self, data):
        headers = {
        'Content-Type': 'application/json',
        'X-Master-Key':  self.api_key,
        }

        requests.put(self.url, json=data, headers=headers)
