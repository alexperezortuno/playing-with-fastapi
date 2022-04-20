import uvicorn
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import core.app_logger
from core.logger_formatter import CustomFormatter
from model.cars import ResponseCar
from sql_app import models, schemas, crud
from sql_app.database import engine, SessionLocal
# from starlette.background import BackgroundTask
from starlette_prometheus import metrics, PrometheusMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["PUT", "DELETE", "POST", "GET"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)
formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger('fastApi')
# logger.setLevel(logging.INFO)
#
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)
logger = core.app_logger.get_logger(__name__, formatter)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def write_log_data(request, response):
    logger.info(request.method + ' ' + request.url.path,
                extra={'extra_info': core.app_logger.get_extra_info(request, response)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT', 80)), log_level=os.getenv('LOG_LEVEL', 'info'))


@app.get("/")
def read_root():
    return {"status": "working"}


@app.get("/ping")
async def ping():
    return {"message": "pong!"}


@app.get("/car/{id}")
async def get_car(id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car_by_id(db, id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.get("/cars")
async def get_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars


# @app.post("/cars")
# async def create_car(car: RequestCar) -> ResponseCar:
#     return car
@app.post("/car", response_model=ResponseCar)
async def create_car(car: schemas.CarBase, db: Session = Depends(get_db)):
    db_car = crud.get_car_by_brand_and_model(db, brand=car.brand, model=car.model)
    # BackgroundTask(write_log_data, request, response)

    if db_car:
        raise HTTPException(status_code=400, detail="car already exists")

    try:
        return crud.create_car(db=db, car=car)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/car/{id}")
async def delete_car(id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car_by_id(db, id=id)

    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    try:
        return crud.delete_car(db=db, id=id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
