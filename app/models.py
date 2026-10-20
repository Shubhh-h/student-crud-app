from sqlalchemy import Column, Integer, String, Date

from .database import Base  # single shared Base (was duplicated before)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    course = Column(String, nullable=True)
    address = Column(String, nullable=True)
    enrollment_date = Column(Date, nullable=True)
