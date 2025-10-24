from pydantic import BaseModel
from datetime import date
from typing import List


class EventBase(BaseModel):
    title: str
    date: date
    location: str
    quota: int


class EventCreate(EventBase):
    pass


class ParticipantBase(BaseModel):
    name: str
    email: str
    event_id: int


class ParticipantCreate(ParticipantBase):
    pass


class Participant(ParticipantBase):
    id: int

    class Config:
        orm_mode = True


class Event(EventBase):
    id: int

    participants: List[Participant] = []

    class Config:
        orm_mode = True
