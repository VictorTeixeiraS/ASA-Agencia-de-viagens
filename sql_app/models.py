from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

"""------------------------------------------------------------"""

class AirportsModel(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    city = Column(String, index=True)


"""------------------------------------------------------------"""

class FlightModel(Base):
    __tablename__ = "flights"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    flight_name     = Column(Integer, unique=True, index=True)
    from_airport    = Column(String, index=True)
    to_airport      = Column(String, index=True)
    day_of_flight   = Column(String, index=True)
    price           = Column(Integer, index=True)
    seats           = Column(Integer, index=True)
    

"""------------------------------------------------------------"""

class PurchasesModel(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_token = Column(String, index=True)
    user = Column(String, index=True)
    flight_name = Column(String, index=True)
    passengers = Column(String, index=True)
    number_of_passengers = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    session_key = Column(String, index=True)

class ReservationModel(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_token = Column(String, index=True)
    e_ticket = Column(String, index=True)
    passenger = Column(String, index=True)

"""------------------------------------------------------------"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
"""------------------------------------------------------------"""

class Current_User(Base):
    __tablename__ = "current_user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    session_key = Column(String, index=True)

