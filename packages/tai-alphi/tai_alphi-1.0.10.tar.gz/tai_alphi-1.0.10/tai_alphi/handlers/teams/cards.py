import datetime


class CardTemplate:
    success_icon_url = "https://img.icons8.com/emoji/48/000000/check-mark-emoji.png"
    failed_icon_url = "https://img.icons8.com/emoji/48/000000/cross-mark-emoji.png"

    def __init__(
        self,
        proyecto: str,
        pipeline: str,
        notify_to: list[str],
        date: datetime.date,
        time: datetime.time
    ) -> None:
        
        self.proyecto = proyecto
        self.pipeline = pipeline
        self.date = date.strftime("%a %d de %B, %Y")
        self.time = time.strftime("%H.%M")
        self.notify_to = notify_to

        self._failed = None
        self._logs = None
        self._listed_logs = None
    
    @property
    def failed(self) -> bool:
        return self._failed
    
    @failed.setter
    def failed(self, failed: bool) -> None:
        self._failed = failed

    @property
    def logs(self) -> str:
        return self._logs
    
    @logs.setter
    def logs(self, logs: str) -> None:
        self._logs = logs

    @property
    def listed_logs(self) -> list[dict[str,str]]:
        return self._listed_logs
    
    @listed_logs.setter
    def listed_logs(self, listed_logs: list[dict]) -> None:
        self._listed_logs = listed_logs

    @property
    def status(self) -> dict:
        return {
            "url": self.failed_icon_url if self.failed else self.success_icon_url,
            "text": "**ERROR**" if self.failed else "**SUCCESS**",
            "color": "Attention" if self.failed else "Good",
        }
    
    @property
    def definition(self) -> dict:
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.3",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"**{self.proyecto}**",
                                "wrap": True,
                                "separator": True,
                                "id": "title",
                                "size": "extraLarge",
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": "**Pipeline**", "value": self.pipeline},
                                    {"title": "**Fecha**", "value": self.date},
                                    {"title": "**Hora**", "value": self.time}
                                ],
                                "id": "description",
                                "separator": True,
                            },
                            {
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "width": "150px",
                                        "items": [
                                            {
                                                "type": "ColumnSet",
                                                "columns": [
                                                    {
                                                        "type": "Column",
                                                        "width": "35px",
                                                        "items": [
                                                            {
                                                                "type": "Image",
                                                                "url": self.status["url"],
                                                                "width": "25px",
                                                                "height": "25px",
                                                                "id": "icon",
                                                                "horizontalAlignment": "Center",
                                                            }
                                                        ],
                                                    },
                                                    {
                                                        "type": "Column",
                                                        "width": "70px",
                                                        "items": [
                                                            {
                                                                "type": "TextBlock",
                                                                "text": self.status["text"],
                                                                "color": self.status["color"],
                                                                "wrap": True,
                                                                "id": "status",
                                                                "horizontalAlignment": "Center",
                                                            }
                                                        ],
                                                        "verticalContentAlignment": "Center",
                                                    },
                                                ],
                                            }
                                        ],
                                        "verticalContentAlignment": "Center",
                                    },
                                ],
                            },
                            {
                                "type": "ActionSet",
                                "actions": [
                                    {
                                        "type": "Action.ShowCard",
                                        "title": "Show logs",
                                        "card": {
                                            "type": "AdaptiveCard",
                                            "body": [
                                            {
                                                "type": "TextBlock",
                                                "text": log['record'],
                                                "fontType": 'monospace',
                                                "size": 'small',
                                                "color": log['color'],
                                                "spacing": 'none',
                                                "weight": log['weight'],
                                                "wrap": True,
                                                "id": i
                                            } for i, log in enumerate(self.listed_logs)
                                            ]
                                        }
                                    },
                                ],
                                "id": "action_set2",
                            }
                        ],
                    },
                }
            ],
        }

    def _add_mentions(self, card):
        card["attachments"][0]["content"]["msteams"] = {"entities": []}
        text_mentions = "**Revisión necesaria**: "
        for email in self.notify_to:
            if "@triplealpha.in" not in email:
                continue
            name = email.split("@")[0]
            text_mentions += f" <at>{name}</at>,"
            info = {
                "type": "mention",
                        "text": f"<at>{name}</at>",
                        "mentioned": {
                            "id": email,
                            "name": name
                        }
            }

            card["attachments"][0]["content"]["msteams"]["entities"].append(info)
            
        card["attachments"][0]["content"]["body"].insert(2,
        {
            "type": "TextBlock",
            "text": text_mentions[:-1],
            "size": "Large"
        })

        return card

    def get_card_definition(self):

        c_def = self.definition

        if self.notify_to and self.failed:
           c_def = self._add_mentions(c_def)
           
        return c_def