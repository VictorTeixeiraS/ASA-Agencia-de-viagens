from sqlalchemy.orm import Session

import models, schemas

import random
import string


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_current_user_by_email(db: Session, email: str):
    return db.query(models.Current_User).filter(models.Current_User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_current_user(db: Session, user: str):
    teste1 = get_current_user_by_email(db, email= user)
    db.delete(teste1)
    db.commit()
    return

def create_current_user(db: Session, user: str):
    fake_session_key = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
    db_user = models.Current_User(email = user, session_key=fake_session_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_airport(db: Session, user: schemas.AirportSchema):
    db_airport = models.AirportsModel(name=user.name, city=user.city)
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

def create_flight(db: Session, user: schemas.FlightDay):
    flight_name = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
    db_flight = models.FlightModel(flight_name = flight_name,
                                    from_airport=user.from_airport,
                                   to_airport=user.to_airport, day_of_flight=user.day_of_flight,
                                   price=user.price, seats=user.seats)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def check_login(db: Session, email: str, password: str):
    teste = get_user_by_email(db, email)
    if teste is None:
        return None
    else:
        if teste.password == password:
            return teste
        else:
            return None

def logout(db: Session, email: str):
    db_current_user = db.query(models.Current_User).filter(models.Current_User.email == email).first()
    if db_current_user is None:
        return "Wrong email"
    else:
        db.delete(db_current_user)
        db.commit()
        return "Logout efetuado com sucesso"

def get_airports(db: Session):
    return db.query(models.AirportsModel).limit(100).all()

def get_purchases(db: Session):
    return db.query(models.PurchasesModel).limit(100).all()

def get_airport_by_city(db: Session, citys: str):
    return db.query(models.AirportsModel).filter(models.AirportsModel.city == citys).limit(100).all()

def get_flights_by_day(db: Session, day_of_flight: str):
    return db.query(models.FlightModel).filter(models.FlightModel.day_of_flight == day_of_flight).limit(100).all()

def get_reservation(db: Session, reservation_token: str):
    return db.query(models.ReservationModel).filter(models.ReservationModel.reservation_token == reservation_token).limit(100).all()

def get_flights_by_prices_and_passengers(db: Session, number_of_passengers: int):
    return db.query(models.FlightModel).filter(models.FlightModel.seats >= number_of_passengers).order_by(models.FlightModel.price).limit(100).all()

def create_e_tocken(db: Session, reservation_token: str):
    e_tocken = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
    db_reservation = models.ReservationModel(e_ticket=e_tocken, reservation_token= reservation_token,passenger='')
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_passenger_name(db: Session, e_ticket: str, passenger_name: str):
    eticket = db.query(models.ReservationModel).filter(models.ReservationModel.e_ticket == e_ticket).first()
    if eticket is None:
        return "Wrong eticket"
    else:
        updated_eticket = models.ReservationModel(reservation_token=eticket.reservation_token, e_ticket=eticket.e_ticket,
                                                passenger=passenger_name)
        db.delete(eticket)
        db.add(updated_eticket)
        db.commit()
        db.refresh(updated_eticket)

        return updated_eticket


    
def create_purchase(db: Session, user: schemas.PurchaseSchema, email: str):
    voo = db.query(models.FlightModel).filter(models.FlightModel.flight_name == user.flight_name).first()
    id_voo = voo.id
    reservation_token = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
    if voo is None:
        return "Flight error, please verify"
    else:
        price = voo.price*user.number_of_passengers
        db_purchase = models.PurchasesModel(reservation_token =reservation_token,user = email,
            flight_name=user.flight_name, passengers=user.passengers, 
            number_of_passengers=user.number_of_passengers, 
                session_key=user.session_key, total_price=price)
        db_flight_seats = (voo.seats)-(user.number_of_passengers)
        new_flight = models.FlightModel(flight_name=voo.flight_name, from_airport=voo.from_airport,
                                    to_airport=voo.to_airport, day_of_flight=voo.day_of_flight,
                                    price=voo.price, seats=db_flight_seats)
        old_flight = db.get(models.FlightModel, id_voo)
        i = 0
        while i<user.number_of_passengers:
            create_e_tocken(db, reservation_token)
            i=i+1
        db.delete(old_flight)
        db.commit()
        db.add(new_flight)
        db.add(db_purchase)
        db.commit()
        db.refresh(new_flight)
        db.refresh(db_purchase)

        return db_purchase
