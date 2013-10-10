"""Database init module.

Contains configurable settings for the database tool, and initialises the 
database itself.

"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from paf_tools.database import tables

engine = create_engine('sqlite:////home/daniel/PAF/database.db')
tables.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

#############################
# Database helper functions #
#############################

def erase_database():
    """Erase contents of database and start over."""
    metadata = MetaData(engine)
    metadata.reflect()
    metadata.drop_all()
    tables.Base.metadata.create_all(engine)
    return None
