from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import data

app = FastAPI()


class Build(BaseModel):
    build: str


@app.post("/get_tasks")
async def get_tasks(build: Build) -> list[str]:
    build_name = build.build

    if not build_name:
        raise HTTPException(status_code=400, detail="Build name is required")

    build_tasks: list[str] = data.get_build_tasks(build_name)
    return data.topological_sort(build_tasks)
