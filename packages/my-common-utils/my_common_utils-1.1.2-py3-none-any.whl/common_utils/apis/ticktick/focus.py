import os
import requests
from datetime import datetime
import pytz
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

from common_utils.logger import create_logger
from common_utils.apis.ticktick.cookies_login import get_authenticated_ticktick_headers
from common_utils.time_utils import get_timestamp_from_offset


class TickTickFocusTime(BaseModel):
    id: str
    type: int
    start_time: str | datetime
    end_time: str | datetime
    status: int
    pause_duration: int
    total_duration: int | None = None

    @field_validator("start_time", "end_time", mode="before")  # noqa
    @classmethod
    def _parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    @model_validator(mode="after")
    def _set_timezone_and_duration(self):
        tz_name = os.getenv("LOCAL_TIMEZONE", "Europe/Berlin")
        tz = pytz.timezone(tz_name)
        self.start_time = self.start_time.astimezone(tz)
        self.end_time = self.end_time.astimezone(tz)
        self.total_duration = int((self.end_time - self.start_time).total_seconds() / 60)
        return self

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


class TicktickFocusHandler:
    log = create_logger('TickTick Focus Handler')

    def __init__(
            self,
            cookies_path: str | None = None,
            always_raise_exceptions: bool = False,
            headless: bool = True,
            undetected: bool = False,
            download_driver: bool = False,
            username_env: str = 'TICKTICK_EMAIL',
            password_env: str = 'TICKTICK_PASSWORD',
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

    def get_all_focus_times(
            self,
            to_timestamp: int | None = None,
            days_offset: int | None = None
    ) -> list[TickTickFocusTime] | None:
        if days_offset:
            to_timestamp = get_timestamp_from_offset(days_offset=days_offset)

        timestamp_query_param = f"?to={to_timestamp}" if to_timestamp else ''
        url = f"https://api.ticktick.com/api/v2/pomodoros/timeline{timestamp_query_param}"
        response = requests.get(url, headers=self.headers).json()
        if not isinstance(response, list):
            error_msg = f'No or malformed response to get_all_focus_times: {response}'
            self.log.error(error_msg)
            if self.raise_exceptions:
                raise ValueError(error_msg)
            return None

        focus_times = [TickTickFocusTime(**focus_time_data) for focus_time_data in response]
        return focus_times



if __name__ == '__main__':
    handlers = TicktickFocusHandler()
    focus_times_ = handlers.get_all_focus_times()
    print(focus_times_)