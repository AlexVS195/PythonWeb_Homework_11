from sqlalchemy import Column, Integer, String, Date
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)