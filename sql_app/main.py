# uvicorn main:app --reload
from typing import Optional
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
import send
from database import SessionLocal, engine

from logger import logger

app = FastAPI()

logger.info("Aplicação iniciada...")
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Efetuar login e recuperar chave de sessao
@app.post('/Login' ,response_model=schemas.Current_user_create)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email=user.email
    users = crud.check_login(db, email=user.email, password=user.password) 
    if users is None:
        raise HTTPException(status_code=404, detail="Wrong user or password")
    else:
        db_user = crud.get_current_user_by_email(db, email=email)
        if db_user:
            crud.delete_current_user(db=db, user=user.email)
        login = crud.create_current_user(db, user=user.email)
        return login

# Efetuar logout
@app.post('/Logout/{email}')
def logout(email: str ,db: Session = Depends(get_db)):
    logout = crud.logout(db, email) 
    return logout

# Retorna Lista de todos os aeroportos oferecidos pela companhia
@app.get("/list_of_all_airports/")
def list_of_all_airports(db: Session = Depends(get_db)):
    airports = crud.get_airports(db=db)
    if airports is None:
        raise HTTPException(status_code=404, detail="Airports not found")
    return airports

# Retorna lista dos aeroportos pela cidade
@app.get('/list_of_airports_by_city/{citys}', response_model=[])
def list_airport_by_city(citys: str, db: Session = Depends(get_db)):
    airport = crud.get_airport_by_city(db, citys=citys)
    if airport is None:
        raise HTTPException(status_code=404, detail="Airports not found")
    return airport

# Retorna lista dos voos pela data
@app.get("/list_of_flights_by_day/{day}", response_model=[])
def list_flights_by_day(day_of_flight: str, db: Session = Depends(get_db)):
    db_flights_day = crud.get_flights_by_day(db, day_of_flight=day_of_flight)
    if db_flights_day is None:
        raise HTTPException(status_code=404, detail="Flights not found")
    return db_flights_day

# Retorna lista dos voos pelo numero de passageiros, ordenado pelo preço
@app.get("/flight_by_number_of_passengers/{number_of_passengers}", response_model=[])
def list_flights_by_number_of_passengers(number_of_passengers: int, db: Session = Depends(get_db)):
    db_flights_passengers = crud.get_flights_by_prices_and_passengers(db, number_of_passengers=number_of_passengers)
    if db_flights_passengers is None:
        raise HTTPException(status_code=404, detail="Flights not found")
    return db_flights_passengers


# Efetua a compra verificando se a chave de sessao é valida, atualiza os voos e retorna o etickted
@app.post("/purchases/", response_model=schemas.total_purchase)
def make_purchase(purchase: schemas.PurchaseSchema, db: Session = Depends(get_db)):
    db_user= db.query(models.Current_User).filter(models.Current_User.session_key == purchase.session_key).first()
    if db_user == None:
        raise HTTPException(status_code=400, detail="Wrong session_key")
    else:
        db_flight_seat= db.query(models.FlightModel).filter(models.FlightModel.flight_name == purchase.flight_name).first()
        if db_flight_seat is None:
            raise HTTPException(status_code=400, detail="Wrong Flight name")
        else:
            if db_flight_seat.seats < purchase.number_of_passengers:
                raise HTTPException(status_code=400, detail="Not enough seats")
            else:
#                send.publish_ticket_purchase(purchase.dict())
                compra = crud.create_purchase(db,user=purchase,email=db_user.email)
                return compra

@app.get("/reservation/{reservation_token}", response_model=[])
def get_etickets(reservation_token: str, db: Session = Depends(get_db)):
    reservations = crud.get_reservation(db, reservation_token=reservation_token)
    if reservations is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservations

@app.post("/e_ticket/{passenger_name}", response_model=schemas.ReservationSchema)
async def update_passenger_name(eticket: str, passenger_name: str, db: Session = Depends(get_db)):
    update = crud.update_passenger_name(db,eticket,passenger_name)
    return update


"""------------------------------------------------------------"""
"Creates"
"""------------------------------------------------------------"""

# create users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# create flights
@app.post("/flights/", response_model=schemas.FlightDay)
def create_flight(user: schemas.FlightDay, db: Session = Depends(get_db)):
    return crud.create_flight(db=db, user=user)

# create airport
@app.post("/airport/", response_model=schemas.AirportSchema)
def create_airport(user: schemas.AirportSchema, db: Session = Depends(get_db)):
    return crud.create_airport(db=db, user=user)

"""------------------------------------------------------------"""
"Get all"
"""------------------------------------------------------------"""

# return list of all flights
@app.get("/flights/")
def read_flights(db: Session = Depends(get_db)):
    users = db.query(models.FlightModel).limit(100).all()
    return users

# return list of  all flights
@app.get("/active_users/")
def read_active_users(db: Session = Depends(get_db)):
    users = db.query(models.Current_User).limit(100).all()
    return users

# return list of  all users
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).limit(100).all()
    return users


# return list of all purchases
@app.get("/purchases/")
def list_of_all_purchases(db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db=db)
    return purchases

