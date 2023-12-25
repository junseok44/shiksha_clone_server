import enum
from db.database import engine
from datetime import time, date
from typing import List
from sqlalchemy import String, Float, Enum, Integer, Time, Boolean, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TimeEnum(enum.Enum):
    morning = 'morning'
    lunch = 'lunch'
    dinner = 'dinner'
    all_day = 'all-day'

class DayTypeEnum(enum.Enum):
    weekday = 'weekday'
    saturday = 'saturday'
    sunday = 'sunday'

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    username: Mapped[str] = mapped_column(String(15), default="anonymous", nullable=False)
    isAdmin: Mapped[bool] = mapped_column(Boolean, default=False)
    reviews: Mapped[List['Review']] = relationship('Review', back_populates="writer")

class Cafe(Base):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str] = mapped_column(String(10), nullable=False)
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)
    openCloseTimeTables: Mapped[List['OpenCloseTimeTable']] = relationship("OpenCloseTimeTable", back_populates="cafe")

class OpenCloseTimeTable(Base):
    __tablename__ =  "openCloseTimeTable"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cafeId: Mapped[int] = mapped_column(Integer, ForeignKey('cafe.id'))
    cafe: Mapped[Cafe] = relationship("Cafe", back_populates="openCloseTimeTables")
    dayType: Mapped[DayTypeEnum] = mapped_column(Enum(DayTypeEnum), nullable=False)
    lunchStart: Mapped[time] = mapped_column(Time)
    lunchEnd: Mapped[time] = mapped_column(Time)
    dinnerStart: Mapped[time] = mapped_column(Time)
    dinnerEnd: Mapped[time] = mapped_column(Time)

class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    reviews : Mapped[List['Review']] = relationship("Review", back_populates="menu")

class CafeWithMenu(Base):
    __tablename__ = "CafeWithMenu"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cafeId: Mapped[int] = mapped_column(Integer, ForeignKey('cafe.id'))
    menuId: Mapped[int] = mapped_column(Integer, ForeignKey('menu.id'))

    atDate: Mapped[date] = mapped_column(Date, nullable=False)
    atTime: Mapped[TimeEnum] =  mapped_column(Enum(TimeEnum), nullable=False)

    menu: Mapped[Menu] = relationship("Menu", backref="cafeWithMenu")
    cafe: Mapped[Cafe] = relationship("Cafe", backref="cafeWithMenu")

class Review(Base):
    __tablename__="review"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100),nullable=False)
    rating: Mapped[int] = mapped_column(Integer)    

    menuId: Mapped[int] = mapped_column(Integer, ForeignKey("menu.id"))
    menu: Mapped[Menu] = relationship('Menu', back_populates="reviews")

    writerId: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    writer: Mapped[User] = relationship('User', back_populates="reviews")


Base.metadata.create_all(engine)