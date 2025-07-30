import json
from datetime import datetime, timezone
import secrets
import pprint

import requests
from requests import Response
from pydantic import BaseModel, ConfigDict, Field

from common_utils.apis.ticktick.cookies_login import get_authenticated_ticktick_headers
from common_utils.logger import create_logger


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000+0000')

def get_today_due_date() -> str:
    return datetime.today().strftime('%Y-%m-%dT%H:%M:%S.000+0000')

def generate_id() -> str:
    return secrets.token_hex(12)


class TickTickTask(BaseModel):
    id: str = Field(default_factory=generate_id)
    project_id: str
    title: str
    status: int = 0
    priority: int = 0
    progress: int = 0
    deleted: int = 0
    sort_order: int = -3298534883327
    created_time: str = Field(default_factory=current_utc_iso)
    modified_time: str = Field(default_factory=current_utc_iso)
    start_date: str | None = None
    due_date: str | None = None
    creator: int | None = None
    items: list = []
    tags: list = []
    ex_date: list = []
    reminders: list = []
    kind: str | None = None
    project_name: str | None = None  # too much
    column_id: str | None = None
    is_all_day: bool | None = None
    content: str | None = ""
    assignee: str | None = None
    is_floating: bool = False
    time_zone: str = "Europe/Berlin"

    @staticmethod
    def to_camel(field_name: str) -> str:
        """
        Convert a snake_case field name into camelCase.
        E.g. 'checkin_stamp' -> 'checkinStamp'
        """
        parts = field_name.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow"
    )


class TickTickProject(BaseModel):
    id: str
    name: str
    is_owner: bool
    in_all: bool
    group_id: str | None
    muted: bool


    @staticmethod
    def to_camel(field_name: str) -> str:
        """
        Convert a snake_case field name into camelCase.
        E.g. 'checkin_stamp' -> 'checkinStamp'
        """
        parts = field_name.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow"
    )



class TicktickTaskHandler:
    log = create_logger("TickTick Task Handler")
    url_get_tasks = 'https://api.ticktick.com/api/v2/batch/check/0'
    url_get_projects = 'https://api.ticktick.com/api/v2/projects'
    url_create_task = 'https://api.ticktick.com/api/v2/batch/task'

    def __init__(
            self,
            return_pydantic: bool = True,
            always_raise_exceptions: bool = False,
            cookies_path: str | None = None,
            username_env: str = 'TICKTICK_EMAIL',
            password_env: str = 'TICKTICK_PASSWORD',
            headless: bool = True,
            undetected: bool = False,
            download_driver: bool = False,
    ):
        self.headers = get_authenticated_ticktick_headers(
            cookies_path=cookies_path,
            username_env=username_env,
            password_env=password_env,
            headless=headless,
            undetected=undetected,
            download_driver=download_driver,
        )
        self.raise_exceptions = always_raise_exceptions
        self.return_pydantic = return_pydantic
        self.projects = None

    def create_task(self, task: TickTickTask) -> Response:
        payload = {'add': [task.model_dump(by_alias=True, exclude_unset=False)]}
        json_payload = json.dumps(payload)

        response = requests.post(self.url_create_task, data=json_payload, headers=self.headers)
        return response

    def complete_task(self, task_id: str, project_id: str):
        task = {
            'id': task_id,
            'projectId': project_id,
            'status': 2,
        }
        payload = {'update': [task]}
        json_payload = json.dumps(payload)
        response = requests.post(self.url_create_task, data=json_payload, headers=self.headers)
        return response

    def get_all_tasks(self) -> list[TickTickTask] | None:
        """
        Get all TickTick tasks

        Returns:
            List of TickTickTask pydantic BaseModel objects, or dicts
        """
        response = requests.get(url=self.url_get_tasks, headers=self.headers).json()
        tasks_data = response.get('syncTaskBean', {}).get('update', None)
        if tasks_data is None:
            self.log_or_raise_error('Getting Tasks failed')
            return None

        tasks = [TickTickTask(**task_data) for task_data in tasks_data]
        tasks = self.add_project_titles_to_tasks(tasks)

        return tasks

    def get_all_projects(self) -> dict[str, TickTickProject]:
        response = requests.get(url=self.url_get_projects, headers=self.headers).json()
        if response is None:
            self.log_or_raise_error('Getting Projects failed')
            return None

        projects = [TickTickProject(**project_data) for project_data in response]
        projects_map = {project.id: project for project in projects}
        self.projects = projects_map

        return projects_map

    def add_project_titles_to_tasks(self, tasks: list[TickTickTask]) -> list[TickTickTask]:
        if not self.projects:
            return tasks

        for task in tasks:
            try:
                if 'inbox' in task.project_id:
                    task.project_name = 'INBOX'
                else:
                    task.project_name = self.projects[task.project_id].name
            except:
                self.log.warning(f'Project of task {task.title} not found')

        return tasks

    def log_or_raise_error(self, error_msg: str) -> None:
        if self.raise_exceptions:
            raise ValueError(error_msg)
        else:
            self.log.error(error_msg)


if __name__ == '__main__':
    handler = TicktickTaskHandler()
    task = TickTickTask(
        title='TESTABNSDF',
        projectId='6864f1ae8f08304bcb05ecba',
        dueDate=get_today_due_date()
    )
    resp1 = handler.create_task(task=task)
    resp2 = handler.complete_task(task=task)
    handler.get_all_tasks()
