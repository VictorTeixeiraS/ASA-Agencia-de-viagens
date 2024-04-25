from pydantic import BaseModel

"""------------------------------------------------------------"""

class AirportSchema(BaseModel):    
    name: str
    city: str

    class Config:
       from_attributes = True

class AirportSearch(BaseModel):    
    city: str
    class Config:
        from_attributes = True


"""------------------------------------------------------------"""

class FlightSchema(BaseModel):  
    from_airport: str
    to_airport: str
    price: int
    seats: int

    class Config:
        from_attributes = True

class FlightDay(FlightSchema):
    day_of_flight: str
    class Config:
        from_attributes = True


class return_flight (FlightSchema):
    flight_name: str
    class Config:
        from_attributes = True


"""------------------------------------------------------------"""

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
       from_attributes = True

class Current_user_create(BaseModel):
    email: str
    session_key: str

"""------------------------------------------------------------"""

class PurchaseSchema(BaseModel):  
    flight_name: str
    passengers: str
    number_of_passengers: int
    session_key: str
    class Config:
        from_attributes = True

class updateSchema(PurchaseSchema):
    flight_name: str
    number_of_passengers: int
    class Config:
        from_attributes = True

class total_purchase(PurchaseSchema):
    reservation_token: str 
    total_price: int
    class Config:
        from_attributes = True

class ReservationSchema(BaseModel):  
    e_ticket: str
    passenger_name: str
    class Config:
        from_attributes = True
"""------------------------------------------------------------"""
