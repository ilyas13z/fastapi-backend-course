from json_func import read_tasks, write_tasks

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    name: str
    status: str


@app.get("/tasks")
def get_tasks():
    tasks_dict = read_tasks()
    return tasks_dict

@app.post("/tasks")
def create_task(task: str):
    task = task.split()
    tasks_dict = read_tasks()

    if len(tasks_dict) == 0:
        tasks_dict[0] = [task[0], task[1]]
        task_id = 0
    else:
        task_id = list(tasks_dict.keys())[-1] + 1
        tasks_dict[task_id] = [task[0], task[1]]
    write_tasks(tasks_dict)
    return {"Task id": task_id, "Task name": task[0], "Task status": task[1]}

    

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    try:
        tasks_dict = read_tasks()
        if task_id in tasks_dict.keys():
            tasks_dict[task_id] = [task.name, task.status]
            write_tasks(tasks_dict)
            return {"Task name": task.name, "Task status": task.status}
        else:
            raise KeyError
    except KeyError:
        return {"KeyError": "task_id not found"}
    except:
        return {"Error": "Updating went wrong"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        tasks_dict = read_tasks()
        temp = tasks_dict[task_id]
        del tasks_dict[task_id]
        write_tasks(tasks_dict)
        return {"Task id": task_id, "Task name": temp[0], "Task status": temp[1]}
    except:
        return {"Error": "Deleting went wrong"}
