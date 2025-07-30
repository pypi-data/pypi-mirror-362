from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fastapi.exceptions import HTTPException
from redis.client import Redis

from fastapi_task_manager import TaskGroup
from fastapi_task_manager.schema.task import Task, TaskDetailed, TaskRun

if TYPE_CHECKING:
    from fastapi_task_manager import TaskManager


def get_task_groups(
    task_manager: "TaskManager",
    name: str | None = None,
    tag: str | None = None,
) -> list[TaskGroup]:
    return [
        TaskGroup(
            name=x.name,
            tags=x.tags,
        )
        for x in task_manager.task_groups
        if (name is None or name == x.name) and (tag is None or tag in x.tags)
    ]


def get_tasks(
    task_manager: "TaskManager",
    task_group_name: str | None = None,
    name: str | None = None,
    tag: str | None = None,
) -> list[TaskDetailed]:
    list_to_return = []
    redis_client = Redis(
        host=task_manager.config.redis_host,
        port=task_manager.config.redis_port,
        password=task_manager.config.redis_password,
        db=task_manager.config.redis_db,
    )
    for tg in task_manager.task_groups:
        if task_group_name is not None and task_group_name != tg.name:
            continue
        for t in tg.tasks:
            if (name is not None and name != t.name) or (tag is not None and t.tags is not None and tag not in t.tags):
                continue

            runs = []  # TODO Evaluate redis linked lists
            if redis_client.exists(task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_runs"):
                runs_b = redis_client.get(task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_runs")
                if runs_b is not None:
                    runs = runs_b.decode("utf-8").split("\n")

            durations_second = []  # TODO Evaluate redis linked lists
            if redis_client.exists(task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_durations_second"):
                durations_second_b = redis_client.get(
                    task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_durations_second",
                )
                if durations_second_b is not None:
                    durations_second = durations_second_b.decode("utf-8").split("\n")
            assert len(runs) == len(durations_second), "Runs and durations_second must have the same length"

            next_run = datetime(year=2000, month=1, day=1, tzinfo=timezone.utc)
            if redis_client.exists(task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_next_run"):
                next_run_b = redis_client.get(task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_next_run")
                if next_run_b is not None:
                    next_run = datetime.fromtimestamp(float(next_run_b.decode("utf-8")), tz=timezone.utc)
            list_to_return.append(
                TaskDetailed(
                    name=t.name,
                    description=t.description,
                    tags=t.tags,
                    expression=t.expression,
                    high_priority=t.high_priority,
                    next_run=next_run,
                    is_active=not redis_client.exists(
                        task_manager.config.app_name + "_" + tg.name + "_" + t.name + "_disabled",
                    ),
                    runs=[
                        TaskRun(
                            run_date=datetime.fromtimestamp(float(runs[i]), timezone.utc),
                            durations_second=float(durations_second[i]),
                        )
                        for i in range(len(runs))
                    ],
                ),
            )
    return list_to_return


def disable_task(
    task_manager: "TaskManager",
    task_group_name: str | None = None,
    task_name: str | None = None,
    tag: str | None = None,
):
    task: Task | None = None
    task_group: TaskGroup | None = None
    for tg in task_manager.task_groups:
        if task_group_name is not None and task_group_name != tg.name:
            continue
        for t in tg.tasks:
            if (task_name is not None and task_name != t.name) or (
                tag is not None and t.tags is not None and tag not in t.tags
            ):
                continue
            task = t
            task_group = tg
            break
    if task is None or task_group is None:
        raise HTTPException(status_code=404, detail="Task not found")
    redis_client = Redis(
        host=task_manager.config.redis_host,
        port=task_manager.config.redis_port,
        password=task_manager.config.redis_password,
        db=task_manager.config.redis_db,
    )
    redis_client.set(
        task_manager.config.app_name + "_" + task_group.name + "_" + task.name + "_disabled",
        "1",
        ex=task_manager.config.statistics_redis_expiration,
    )


def enable_task(
    task_manager: "TaskManager",
    task_group_name: str | None = None,
    task_name: str | None = None,
    tag: str | None = None,
):
    task: Task | None = None
    task_group: TaskGroup | None = None
    for tg in task_manager.task_groups:
        if task_group_name is not None and task_group_name != tg.name:
            continue
        for t in tg.tasks:
            if (task_name is not None and task_name != t.name) or (
                tag is not None and t.tags is not None and tag not in t.tags
            ):
                continue
            task = t
            task_group = tg
            break
    if task is None or task_group is None:
        raise HTTPException(status_code=404, detail="Task not found")
    redis_client = Redis(
        host=task_manager.config.redis_host,
        port=task_manager.config.redis_port,
        password=task_manager.config.redis_password,
        db=task_manager.config.redis_db,
    )
    if redis_client.exists(task_manager.config.app_name + "_" + task_group.name + "_" + task.name + "_disabled"):
        redis_client.delete(task_manager.config.app_name + "_" + task_group.name + "_" + task.name + "_disabled")
