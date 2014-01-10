"""Database init module.

Contains configurable settings for the database tool, and initialises the 
database itself.

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./paf-tools.db')
<<<<<<< HEAD
Base = declarative_base()
Base.metadata.create_all(engine)
=======
tables.Base.metadata.create_all(engine)
>>>>>>> 68cb7fd6645460ca432f2cda8dd486d032737887
Session = sessionmaker(bind=engine)
