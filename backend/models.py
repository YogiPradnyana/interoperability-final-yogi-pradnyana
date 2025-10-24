from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    date = Column(Date)
    location = Column(String(100))
    quota = Column(Integer)

    participants = relationship("Participants", back_populates="event")


class Participants(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Events", back_populates="participants")
