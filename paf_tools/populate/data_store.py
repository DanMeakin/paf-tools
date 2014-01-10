"""Data Store module.

Defines the PAFData class, which uses the PAFReader class to import data 
from the postcode address files, and then carries out required substitutions 
to turn the "relational" data into one set of non-relational address records.

"""
from paf_tools.structure import *
from paf_tools.populate.files_parser import PAFReader 

class PAFData(object):
    """This class defines the PAFData class.

    This class is used to flatten and clean-up the relational data extracted 
    from the PAF component files.

    """
    def __init__(self, paf_path):
        """Initialise PAFData instance."""
        self.path = paf_path
        self.paf_readers = {filetype: PAFReader(self.path, filetype)
                            for filetype in VALID_FILETYPES}
        self._get_non_address_data()

    def __iter__(self):
        return self

    def __next__(self):
        """Define next method.

        Substitutes the relational keys for the actual values for each 
        relational field in the address PAF.

        """
        raw_entry = next(self.paf_readers['ADDRESS'])
        flattened_entry = self._flatten_address_entry(raw_entry)
        #Define relational entries per address entry:
        return flattened_entry

    def _flatten_address_entry(self, raw_entry):
        """Flatten raw address data.

        Substitutes actual data for the various relational fields contained 
        within raw parsed file data.

        Returns a dictionary containing key/value pairs of the datatype, and 
        the data parsed from the PAF.armando

        """
        paf = self.paf_data
        locality = paf['LOCALITY'].get(raw_entry[2], ('','','','',''))
        building_name = paf['BUILDING_NAME'].get(raw_entry[8], ('',))
        sub_building_name = paf['SUB_BUILDING_NAME'].get(raw_entry[9], ('',))
        organisation = paf['ORGANISATION'].get(raw_entry[11], ('','','',''))
        thoroughfare = paf['THOROUGHFARE'].get(raw_entry[3], ('',))
        th_descriptor = paf['THOROUGHFARE_DESCRIPTOR'].get(raw_entry[4], ('',''))
        dependent_thoroughfare = paf['THOROUGHFARE'].get(raw_entry[5], ('',))
        dep_th_descriptor = paf['THOROUGHFARE_DESCRIPTOR'].get(raw_entry[6], ('',''))
        return {
            'postcode': raw_entry[0],
            'building number': int(raw_entry[7]) if int(raw_entry[7]) else None,
            'concatenation indicator': raw_entry[13] == "Y",
            'po box': raw_entry[16] if raw_entry[16] else None,
            #Relational Substitutions
            'post town': locality[2].title(),
            'dependent locality': locality[3].title(),
            'double dependent locality': locality[4].title(),
            'building name': building_name[0].title(),
            'organisation name': organisation[1].title(),
            'department name': organisation[2].title(),
            'sub-building name': sub_building_name[0].title(),
            'thoroughfare': '{} {}'.format(
                thoroughfare[0],
                th_descriptor[0],
                ).strip().title(),
            'dependent thoroughfare': '{} {}'.format(
                dependent_thoroughfare[0],
                dep_th_descriptor[0],
                ).strip().title(),
            }

    def _get_non_address_data(self):
        """Get non-address data from the PAFReaders.

        Creates a series of dictionaries which contain all the data parsed 
        by the PAFReaders, restructured into dictionary form whereby the 
        key for each datatype is the dictionary key, and the values are 
        stored in tuples.

        """
        self.paf_data = {}
        for filetype in filter(lambda x: x != "ADDRESS", VALID_FILETYPES):
            print("Populating {} data...".format(filetype))
            self.paf_data[filetype] = {
                    entry[0]: entry[1:]
                    for entry in self.paf_readers[filetype]
                    }
            print("{} population complete!".format(filetype))
