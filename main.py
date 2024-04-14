from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime, timedelta
import crud, models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db=db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db=db, contact_id=contact_id)
    return db_contact

@app.get("/contacts/search/", response_model=list[schemas.Contact])
def search_contacts(name: str = Query(None), last_name: str = Query(None), email: str = Query(None), db: Session = Depends(get_db)):
    if name:
        return crud.search_contacts_by_name(db=db, name=name)
    elif last_name:
        return crud.search_contacts_by_last_name(db=db, last_name=last_name)
    elif email:
        return crud.search_contacts_by_email(db=db, email=email)
    else:
        return crud.get_contacts(db=db)

@app.get("/contacts/birthdays/", response_model=list[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    return crud.get_birthdays_in_range(db=db, start_date=today, end_date=next_week)