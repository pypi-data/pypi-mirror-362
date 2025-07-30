import json
import atexit
from collections import deque
from datetime import datetime
from logging import (
    Handler,
    LogRecord,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)
from tai_alphi.config.schemas import TeamsConfig
from tai_alphi.handlers.teams.cards import CardTemplate
from tai_alphi.exceptions.dependencies import optional_dependencies

class TeamsHandler(Handler):

    def __init__(self, webhook: str, teams_config: TeamsConfig) -> None:
        super().__init__()
        self.webhook = webhook
        self.config = teams_config

        self.date = datetime.today()
        self.time = datetime.now()

        self._failed = False
        self._queue = None
        self._colored_queue = None

        atexit.register(self.at_exit)

    @property
    def queue(self) -> deque:
        if not self._queue:
            self._queue = deque(maxlen=10000)
        return self._queue

    @property
    def colored_queue(self) -> deque:
        if not self._colored_queue:
            self._colored_queue = deque(maxlen=10000)
        return self._colored_queue
    
    @property
    def colors(self) -> dict:
        return {
            DEBUG: 'light',
            INFO: 'accent',
            WARNING: 'warning',
            ERROR: 'attention',
            CRITICAL: 'attention'
        }
    
    @property
    def failed(self) -> bool:
        return self._failed
    
    @property
    def card_factory(self) -> CardTemplate:
        return CardTemplate(
            proyecto=self.config.project,
            pipeline=self.config.pipeline,
            notify_to=self.config.notifications,
            date=self.date,
            time=self.time
        )
    
    def emit(self, record: LogRecord) -> None:
        if not self.failed and record.levelno >= 40:
            self._failed = True
        self.queue.append(self.format(record))
        self.colored_queue.append(
            {
                'record': self.format(record).replace('\n', '\n\n'),
                'color': self.colors[record.levelno],
                'weight': 'bolder' if record.levelno==50 else 'default'
            }
        )
    
    def get_queue_contents(self) -> str:
        return "\n\n".join(self.queue)
    
    def at_exit(self) -> None:

        with optional_dependencies():
            import requests as rq

        card = self.card_factory
        card.failed = self.failed
        card.listed_logs = self.colored_queue

        definition = card.get_card_definition()
        payload = json.dumps(definition)

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        rq.post(self.webhook, payload, headers=headers)
