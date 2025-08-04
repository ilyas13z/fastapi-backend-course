import os

from abstract import AiClient, JsonBinClient
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

file_worker = JsonBinClient(
    os.getenv("API_KEY_JSONBIN"), os.getenv("USER_ID_JSONBIN")
)
description_worker = AiClient(
    os.getenv("API_KEY_LLM"), os.getenv("USER_ID_LLM")
)


class Task(BaseModel):
    name: str
    status: str
    description: str


@app.get("/tasks")
def get_tasks():
    tasks_dict = file_worker.read()
    return tasks_dict


@app.post("/tasks")
def create_task(name: str, status: str):
    tasks_dict = file_worker.read()
    description = description_worker.get_description(name)

    if len(tasks_dict) == 0:
        tasks_dict[0] = [name, status, description]
        task_id = 0
    else:
        task_id = list(tasks_dict.keys())[-1] + 1
        tasks_dict[task_id] = [name, status, description]
    file_worker.write(tasks_dict)
    return {
        "Task id": task_id,
        "Task name": name,
        "Status": status,
        "Description": description,
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    try:
        tasks_dict = file_worker.read()
        if task_id in tasks_dict.keys():
            tasks_dict[task_id] = [task.name, task.status, task.description]
            file_worker.write(tasks_dict)
            return {
                "Task name": task.name,
                "Status": task.status,
                "Description": task.description,
            }
        else:
            raise KeyError
    except KeyError:
        return {"KeyError": "task_id not found"}
    except:
        return {"Error": "Updating went wrong"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        tasks_dict = file_worker.read()
        temp = tasks_dict[task_id]
        del tasks_dict[task_id]
        file_worker.write(tasks_dict)
        return {"Task id": task_id, "Task name": temp[0]}
    except:
        return {"Error": "Deleting went wrong"}
