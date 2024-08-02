from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()


class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    desc: Optional[str] = None
    completed: bool = False


tasks = []


@app.post("/task/", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task


@app.get("/task/", response_model=List[Task])
def read_tasks():
    return [t for t in tasks if t.completed == True]


@app.get("/task/{task_id}", response_model=Task)
def read_task(task_id: UUID):

    task = next((t for t in tasks if t.id == task_id), None)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task get id fail")


@app.put("/task/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):

    matching_task = [
        (idx, task) for idx, task in enumerate(tasks) if task.id == task_id
    ]

    if matching_task:
        idx, task = matching_task[0]
        update_task = task.copy(update=task_update.dict(exclude_unset=True))
        tasks[idx] = update_task
        return update_task
    else:
        raise HTTPException(status_code=404, detail="Task update fail")


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: UUID):

    task = next((t for t in tasks if task_id == t.id), None)

    if task is not None:
        tasks.remove(task)
        return task
    raise HTTPException(status_code=404, detail="Task delete fail")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=4000, host="0.0.0.0")
