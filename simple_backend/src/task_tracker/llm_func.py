import requests
import os
import json


class LlmWorker:
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{user_id}/ai/run/"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def get_description(self, task_name):
        inputs = [
            { "role": "system", "content": "Ты ассистент для описания повседневных задач в таск трекере" },
            { "role": "user", "content": f"Ты — эксперт по анализу задач. Тебе передают текст задачи. 1. Прочитай её. 2. Составь краткое описание (НЕ МЕНЬШЕ 10 слов и не более 50 слов). 3. Используй язык, на котором написано название задачи. 4. Выведи только описание, без пояснений и лишнего текста. Задача: {task_name}"}
        ]
        input = {"messages": inputs}
        response = requests.post(f"{self.url}@cf/meta/llama-3-8b-instruct", headers=self.headers, json=input)
        return response.json()['result']['response']
