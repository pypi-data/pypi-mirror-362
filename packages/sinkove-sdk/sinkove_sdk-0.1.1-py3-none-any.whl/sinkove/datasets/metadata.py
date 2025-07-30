from dataclasses import dataclass
from datetime import datetime
import typing
import uuid

State = typing.Literal["PENDING", "STARTED", "READY", "FAILED", "UNKNOWN"]


@dataclass
class Metadata:
    id: uuid.UUID
    state: State
    progress: int
    size: int
    started_at: typing.Optional[datetime]
    finished_at: typing.Optional[datetime]
