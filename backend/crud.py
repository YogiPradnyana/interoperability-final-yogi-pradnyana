from sqlalchemy.orm import Session
import models
import schemas


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Events).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Events(
        title=event.title,
        date=event.date,
        location=event.location,
        quota=event.quota
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


def get_event(db: Session, event_id: int):
    return db.query(models.Events).filter(models.Events.id == event_id).first()


def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Events).filter(
        models.Events.id == event_id).first()

    if db_event:
        db_event.title = event.title
        db_event.date = event.date
        db_event.location = event.location
        db_event.quota = event.quota

        db.commit()
        db.refresh(db_event)

    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Events).filter(
        models.Events.id == event_id).first()

    if db_event:
        db.delete(db_event)
        db.commit()

    return db_event


def get_participants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Participants).offset(skip).limit(limit).all()


def create_participant(db: Session, participant: schemas.ParticipantCreate):

    db_event = get_event(db, event_id=participant.event_id)
    if not db_event:
        return {"error": "Event not found"}

    current_participants = len(db_event.participants)
    if current_participants >= db_event.quota:
        return {"error": "Quota is full"}

    db_participant = models.Participants(
        name=participant.name,
        email=participant.email,
        event_id=participant.event_id
    )

    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    return db_participant
