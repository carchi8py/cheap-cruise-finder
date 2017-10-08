from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class CruiseLine(Base):
    __tablename__ = 'cruiseline'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

class Ship(Base):
    __tablename__ = 'ship'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

class Port(Base):
    __tablename__ = "port"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

class Cruise(Base):
    __tablename__ = 'curise'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    line_id = Column(Integer, ForeignKey('cruiseline.id'))
    line = relationship(CruiseLine)
    ship_id = Column(Integer, ForeignKey('ship.id'))
    ship = relationship(Ship)
    destination = Column(String(256))
    departs_id = Column(Integer, ForeignKey('port.id'))
    departs = relationship(Port)
    nights = Column(Integer)
    price = Column(Integer)

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
