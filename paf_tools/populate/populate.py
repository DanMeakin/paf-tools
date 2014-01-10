"""Database Populate module.

This module contains functions for populating a database with PAF data.

The data is split across a number of files (as explained elsewhere), and so 
each file must be parsed and the data inserted into the database.

"""
from paf_tools import database
from paf_tools.database.tables import Address
from paf_tools.populate.data_store import PAFData

def populate_address_data(paf_path, erase_existing=True):
    """Populate address table in the database.

    Uses the PAFData class to extract and clean the data from the postcode 
    address file. This is then saved to the addresses table of the database.

    Returns the total number of entries added to the table.

    Keyword arguments:
    paf_path - the full path to the folder containing PAF data
    erase_existing - boolean confirming whether existing database is to be 
                     erased before populating (defaults to True)

    """
     #Check if existing database is to be erased, then do so if true.
    if erase_existing:
        database.operations.erase_database()
    data_generator = PAFData(paf_path)
    session = database.Session()
    count = 0
    print("=== Populating {} table... ===".format(Address.__name__))
    for row in data_generator:
        session.add(Address(**row))
        count += 1
        #Only commit after 100000 additions
        if not count % 100000:
            session.commit()
            print("{:,d} records added...".format(count))
    else:
        session.commit()
        print("{:,d} total records added.".format(count))
    return count


