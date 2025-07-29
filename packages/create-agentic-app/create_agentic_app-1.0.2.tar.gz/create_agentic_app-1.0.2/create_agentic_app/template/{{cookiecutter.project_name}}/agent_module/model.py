from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class APIContext:
    intent: str
    endpoint: str
    method: str
    id: str
    title: str
    author: str


class Query(BaseModel):
    query: str
