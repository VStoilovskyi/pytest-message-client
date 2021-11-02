import dataclasses
import datetime
from typing import Any, List

from _pytest.reports import TestReport
from slack_sdk import WebClient

from pytest_message.listeners.listiner import Listener


__all__ = ['SlackListener']


@dataclasses.dataclass
class Status:
    total: int
    passed: int
    failed: int
    skipped: int


DIVIDER = {
    "type": "divider"
}


class SlackListener(Listener):
    def __init__(self, token: str, chat: str):
        self.state = []
        self._client = self.configure(token)
        self._chat = chat

    @staticmethod
    def configure(token: str) -> WebClient:
        return WebClient(token=token)

    def update(self, data: Any) -> None:
        self.state.append(data)

    def finish(self) -> None:
        title = f'Test report result - {datetime.datetime.now().ctime()}'
        blocks = [self._get_heading_block(title)]
        for func_name, report in self.state:
            blocks.extend(self._prepare_test_report_block(func_name, report))
            blocks.append(DIVIDER)

        self._client.chat_postMessage(channel=self._chat, text=title, blocks=blocks)

    @staticmethod
    def _get_heading_block(heading: str) -> dict:
        return {
                   "type": "header",
                   "text": {
                       "type": "plain_text",
                       "text": heading
                   }
               }

    def _prepare_test_report_block(self, func_name: str, reports: List[TestReport]) -> List[dict]:
        status, errors = self._get_test_info(reports)

        out = [self._create_testfunc_header_block(status, func_name)]
        out.extend(self._create_testfunc_report_blocks(errors))

        return out

    @staticmethod
    def _get_test_info(reports: List[TestReport]):
        total = len(reports)
        passed = 0
        failed = 0
        skipped = 0
        errors = []

        for report in reports:
            if report.outcome == 'skipped':
                skipped += 1
            elif report.outcome == 'passed':
                passed += 1
            elif report.outcome == 'failed':
                failed += 1
                errors.append(report.longrepr.reprcrash.message)

        return Status(total, passed, failed, skipped), errors

    def _create_testfunc_header_block(self, status: Status, header) -> dict:

        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{header}*"
                },
                {
                    "type": "mrkdwn",
                    "text": self._create_testfunc_status_msg(status)
                }
            ]
        }

    @staticmethod
    def _create_testfunc_status_msg(status: Status) -> str:
        if status.total == 1:
            if status.failed:
                return ":red_circle: *Failed*"
            if status.passed:
                return ':large_green_circle: *Passed*'
            if status.skipped:
                return ':white_circle: *Skipped*'
        return f':large_green_circle: *Passed*: {status.passed}\n:red_circle: *Failed*: {status.failed}'

    @staticmethod
    def _create_testfunc_report_blocks(errors: List[str]) -> List[dict]:
        """Creates blocks list for error messages"""
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'```{x}```'
                }
            } for x in errors
        ]
