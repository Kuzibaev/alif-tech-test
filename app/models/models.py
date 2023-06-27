from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    full_name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)

    reservations = relationship("Reservation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Room(Base):
    number = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, number={self.number}, capacity={self.capacity})>"


class Reservation(Base):
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    room = relationship("Room", back_populates="reservations")
    user = relationship("User", back_populates="reservations", lazy="selectin")

    def __repr__(self):
        return f"<Reservation(id={self.id}, " \
               f"room_id={self.room_id}, " \
               f"user_id={self.user_id}, " \
               f"start_time={self.start_time}, " \
               f"end_time={self.end_time})>"
