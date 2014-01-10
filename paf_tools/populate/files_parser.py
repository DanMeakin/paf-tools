"""Parser module.

Contains tools for parsing the various PAF Mainfile component files.

The Address File is the main source tying together the other components, 
containing each address within the UK through reference to the other 
component files.

Each line in the Address File is 88 characters long, and is constructed 
as follows:-

FIELD NAME                  LEVEL   DATA TYPE       SIZE
--------------------------------------------------------
Postcode                    1
  Outward Code              2       Alphanumeric    4 
  Inward Code               2       Alphanumeric    3 
Address Key                 1       Numeric         8 
Locality Key                1       Numeric         6
Thoroughfare Key            1       Numeric         8 *
Thoroughfare Descriptor Key 1       Numeric         4 *
Dependent Thoroughfare Key  1       Numeric         8 *
Dep. Thoroughfare Desc. Key 1       Numeric         4 *
Building Number             1       Numeric         4 *
Building Name Key           1       Numeric         8 *
Sub Building Name Key       1       Numeric         8 *
Number of Households        1       Numeric         4 ¹
Organisation Key            1       Numeric         8 ²
Postcode Type               1       Alphanumeric    1 ²
Concatenation Indicator     1       Alphanumeric    1 ³
Delivery Point Suffix       1       Alphanumeric    2
Small User Org. Indicator   1       Alphanumeric    1 °
PO Box Number               1       Alphanumeric    6

* - If 0, there is no entry of this type present.
¹ - If 0 or 1, indicates one household at address. If greater than 1, this 
    indicates the number of households present.
² - If 0, there is no Organisation present. Refers to a record in Org. file 
    for Small & Large User. Refer to Postcode type to determine type of 
    user, whether S or L.
³ - Either 'Y' or space. If 'Y', indicates that Building Number and Sub 
    Building Name should appear concatenated on same address line.
° - Either 'Y' or space. If 'Y', indicates that a Small User Organisation is 
    present at the address.

--------------------------------------------------------

The other component files consist of entries in the format:-

    <KEY><VALUE>

with no whitespace between the key and value.

"""
import os
from paf_tools.structure import *

class PAFReader(object):
    """This class defines the PAFReader class.

    The class is used to read data from the postcode address file component 
    files to allow this data to be used for whatever purpose is required.

    Details of the structure of the PAF component files is found in 
    structure.py, and each filetype is defined by two separate variables:

        * <filetype>_FILENAME, which defines the filename(s) containing the 
          PAF data; and
        * <filetype>_COMPONENTS, which defines the structure of each line 
          of the relevant file in the form of a list of integers, each 
          representing the length of one field of data.

    """
    def __init__(self, path, filetype):
        """Initialise PAFReader instance."""
        self.path = path
        self.filetype = filetype
        self.filedata = self.open_component_file()

    def __iter__(self):
        self.filedata = self.open_component_file()
        return self

    def __next__(self):
        """Define next method.
    
        Reads the specified PAF component file line by line and passes 
        each line into the line parser.
    
        Yields a tuple containing split address information.
    
        """
        return next(self.filedata)

    def open_component_file(self):
        """Open the PAF component file for reading."""
        filelist = [os.path.join(self.path, x) 
                    for x in self._filetype_data("filename")]
        for entry in filelist:
            with open(entry, errors='replace') as paf_file:
                for line in paf_file:
                    #Skip headers and footers.
                    parsed_line = self._parse_line(line)
                    if (parsed_line[0] and 
                        not (parsed_line[0] == "0" * len(parsed_line[0]) or 
                             parsed_line[0] == "9" * len(parsed_line[0]))):
                        yield parsed_line


    def _parse_line(self, line):
        """Parse line of Address File.
    
        Splits the input address_line into separate components, and returns a 
        tuple containing these components.
    
        """
        #Calculate indices at which splits occur.
        splits_indices = [0]
        for x in self._filetype_data("components"):
            splits_indices.append(x + splits_indices[-1]) 
        split_line = (line[splits_indices[x]:splits_indices[x+1]].strip()
                      for x in range(len(splits_indices)-1))
        return tuple(split_line)

    @property
    def filetype(self):
        """Return filetype value."""
        return self.__filetype

    @filetype.setter
    def filetype(self, filetype):
        """Set the filetype for this PAFReader.
        
        Validate parameters against available filetypes. Used to ensure 
        that filetype parameter contents are valid.
    
        Keyword arguments:
        filetype - the input filetype value to validate against
    
        """
        filetype = filetype.upper()
        if filetype not in VALID_FILETYPES:
            raise ValueError("Error! Invalid filetype specified. (Must be one "
                             "of {}.)".format(', '.join(VALID_FILETYPES)))
        self.__filetype = filetype

    def _validate_datatype(self, datatype):
        """Validate parameters against available datatypes.
    
        Used to ensure that datatype parameters passed to parsing functions 
        are valid. Returns True if datatype is valid, else returns False.
    
        Keyword arguments:
        datatype - the input datatype value to validate against
    
        """
        return datatype in VALID_DATATYPES
    
    def _filetype_data(self, datatype):
        """Obtain specified data for a given filetype.
    
        Each filetype is defined by a filename, and the (ordered) length of 
        the components of each line. This function returns the requested data 
        for the specified filetype.
    
        Keyword arguments:
        filetype - the type of file to obtain data for
        datatype - the type of data required (filename or components)
    
        """
        filetype, data = self.filetype.upper(), datatype.upper()
        #Check for validity of filetype and data input.
        if not self._validate_datatype(data):
            raise ValueError("Invalid datatype specified.")
        output_data = globals()["{}_{}".format(filetype, data)]
        if isinstance(output_data, str):
            output_data = [output_data]
        return output_data

