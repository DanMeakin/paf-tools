"""Database Populate module.

This module contains functions for populating a database with PAF data.

The data is split across a number of files (as explained elsewhere), and so 
each file must be parsed and the data inserted into the database.

"""
from paf_tools import files_parser, database

#Create a mapping between filetypes and declarative table classes.
FILETYPE_TABLE_MAPPING = {filetype: filetype.title().replace('_', '')
                          for filetype in files_parser.VALID_FILETYPES}

def populate_table(data_generator, table):
    """Populate a table in the database.

    Iterates through the relevant file in the PAF and populates the database 
    with data extracted from that file. By default, the table in question is 
    cleared of all existing data, though this can be overridden.

    Returns the total number of entries added to the table.

    Keyword arguments:
    data_generator - generator created in files_parser which returns PAF 
                     component data one line at a time
    table -          the SQLAlchemy declarative class representing a table in the 
                     database

    """
    session = database.Session()
    count = 0
    print("=== Populating {} table... ===".format(table.__name__))
    for row in data_generator:
        session.add(table(*row))
        count += 1
        #Only commit after 100000 additions
        if not count % 100000:
            session.commit()
            print("{:,d} records added...".format(count))
    else:
        session.commit()
        print("{:,d} total records added.".format(count))
    return count
    
def populate_database(paf_path, erase_existing=True):
    """Populate the entire database from PAF data.

    Iterates through each type of file in the PAF, and creates a data 
    generator for each. Then this is passed with the table class to the 
    populate_table function.

    Keyword arguments:
    paf_path - the full path to the folder containing PAF data
    erase_existing - boolean confirming whether existing database is to be 
                     erased before populating (defaults to True)
    """
    #Check if existing database is to be erased, then do so if true.
    if erase_existing:
        database.erase_database()
    #Iterate through each table type, and populate.
    total_records = 0
    for filetype, table_class_name in FILETYPE_TABLE_MAPPING.items():
        data_generator = files_parser.parse_file(paf_path, filetype)
        table_class = getattr(database.tables, table_class_name)
        total_records += populate_table(data_generator, table_class)
    print("===== {} records written to database. =====".format(total_records))
    return total_records
