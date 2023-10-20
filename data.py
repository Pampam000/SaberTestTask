import os

import yaml
from fastapi import HTTPException

builds_path = "builds"


def load_data(file_name: str) -> dict:
    file_path: str = os.path.join(builds_path, file_name)

    if not os.path.exists(file_path):
        raise

    with open(file_path, 'r') as file:
        data: dict = yaml.safe_load(file)
    return data


tasks_data: dict = load_data("tasks.yaml")
builds_data: dict = load_data("builds.yaml")
builds_data = {b['name']: b['tasks'] for b in builds_data['builds']}
tasks_data = {t['name']: t['dependencies'] for t in tasks_data['tasks']}


def get_build_tasks(build_name: str) -> list[str]:
    tasks: list[str] | None = builds_data.get(build_name)

    if tasks is None:
        raise HTTPException(status_code=400,
                            detail=f"Build {build_name} not found")
    return tasks


def topological_sort(tasks: list[str]) -> list[str]:
    visited = set()

    def visit(task_name):
        if task_name in visited:
            return

        for dependency in tasks_data.get(task_name, []):
            visit(dependency)

        visited.add(task_name)

    for task in tasks:
        visit(task)

    return visited
