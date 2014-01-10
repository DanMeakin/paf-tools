"""Database init module.

Contains configurable settings for the database tool, and initialises the 
database itself.

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./paf-tools.db')
Session = sessionmaker(bind=engine)
