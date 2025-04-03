from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine

# Initialize SQLAlchemy
engine = create_engine('sqlite:///movies.db', echo=True)
Base = declarative_base()

# Define Movies Model
class Movies(Base):
    __tablename__ = 'movies'  # Table names should be lowercase by convention

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String)
    rating = Column(Integer)
    ranking = Column(Integer)
    review = Column(String)
    img_url = Column(String)

# Create Tables
Base.metadata.create_all(engine)

# Create a Database Session
Session = sessionmaker(bind=engine)
session = Session()