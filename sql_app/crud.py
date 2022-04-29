from sqlalchemy.orm import Session
from . import models, schemas


def get_car_by_id(db: Session, id: int):
    return db.query(models.Car).filter(models.Car.id == id).first()


def get_car_by_brand_and_model(db: Session, brand: str, model: str):
    return db.query(models.Car).filter(models.Car.brand == brand, models.Car.model == model).first()


def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()


def delete_car(db: Session, id: int):
    db_car = db.query(models.Car).filter(models.Car.id == id).first()
    db.delete(db_car)
    db.commit()
    return db_car


def create_car(db: Session, car: schemas.CarBase):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
