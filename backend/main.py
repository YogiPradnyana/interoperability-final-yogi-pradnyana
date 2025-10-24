from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, SessionLocal

ADMIN_TOKEN = "inirahasiaadmin123"

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
security_scheme = HTTPBearer()

origins = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


@app.get("/")
def read_root():
    return {"message": "Koneksi ke database berhasil dan tabel telah dibuat!"}


@app.post("/events/", response_model=schemas.Event, dependencies=[Depends(get_current_admin)])
def create_new_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.get("/events/", response_model=list[schemas.Event])
def read_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db=db, skip=skip, limit=limit)
    return events


@app.get("/events/{event_id}", response_model=schemas.Event)
def read_single_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.put("/events/{event_id}", response_model=schemas.Event, dependencies=[Depends(get_current_admin)])
def update_single_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.update_event(db=db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.delete("/events/{event_id}", response_model=schemas.Event, dependencies=[Depends(get_current_admin)])
def delete_single_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.delete_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.post("/register/", response_model=schemas.Participant)
def register_participant(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):

    db_participant = crud.create_participant(db=db, participant=participant)

    if isinstance(db_participant, dict) and "error" in db_participant:
        if db_participant["error"] == "Event not found":
            raise HTTPException(status_code=404, detail="Event not found")
        if db_participant["error"] == "Quota is full":
            raise HTTPException(
                status_code=400, detail="Quota for this event is full")

    return db_participant


@app.get("/participants/", response_model=List[schemas.Participant])
def read_all_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    participants = crud.get_participants(db=db, skip=skip, limit=limit)
    return participants
