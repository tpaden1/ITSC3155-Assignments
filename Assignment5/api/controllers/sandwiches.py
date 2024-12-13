from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create(db: Session, sandwich: schemas.SandwichCreate):
    # Create a new Sandwich instance
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    # Query all sandwiches from the database
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    # Query a single sandwich by its ID
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return db_sandwich


def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    # Query the sandwich to be updated
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    # Update fields with the provided data
    update_data = sandwich.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sandwich, key, value)

    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def delete(db: Session, sandwich_id: int):
    # Query the sandwich to be deleted
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    # Delete the sandwich
    db.delete(db_sandwich)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
