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

#Define the valid file types for parsing.
VALID_FILETYPES = [
        'ADDRESS', 'BUILDING_NAME', 'LOCALITY', 'MAILSORT', 
        'ORGANISATION', 'SUB_BUILDING_NAME', 'THOROUGHFARE', 
        'THOROUGHFARE_DESCRIPTOR', #'WELSH_ADDRESS'
        ]
#Define the data types available for each filetype.
VALID_DATATYPES = [
        'FILENAME', 'COMPONENTS'
        ]

def validate_filetype(filetype):
    """Validate parameters against available filetypes.

    Used to ensure that filetype parameters passed to parsing functions 
    are valid.

    Keyword arguments:
    filetype - the input filetype value to validate against

    """
    if filetype not in VALID_FILETYPES:
        raise ValueError("Error! Invalid filetype specified. (Must be one "
                         "of {}.)".format(', '.join(VALID_FILETYPES)))
    return None

def validate_datatype(data):
    """Validate parameters against available datatypes.

    Used to ensure that datatype parameters passed to parsing functions 
    are valid.

    Keyword arguments:
    data - the input datatype value to validate against

    """
    if data not in VALID_DATATYPES:
        raise ValueError("Error! Invalid data type specified. (Must be one "
                         "of {}.)".format(', '.join(VALID_DATATYPES)))
    return None

def filetype_data(filetype, data):
    """Obtain specified data for a given filetype.

    Each filetype is defined by a filename, and the (ordered) length of 
    the components of each line. This function returns the requested data 
    for the specified filetype.

    Keyword arguments:
    filetype - the type of file to obtain data for
    data - the type of data required

    """

    filetype, data = filetype.upper(), data.upper()
    #Check for validity of filetype and data input.
    validate_filetype(filetype)
    validate_datatype(data)
    output_data = globals()["{}_{}".format(filetype, data)]
    if isinstance(output_data, str):
        output_data = [output_data]
    return output_data


def parse_file(path, filetype):
    """Parse a file in the PAF.

    Generator function which reads the specified file line by line 
    and passes each line into the line parser. Accepts path parameter 
    to specify the location of the PAF files.

    Yields a tuple containing split address information.

    Keyword arguments:
    path - the path to the folder containing PAF files
    filetype - the type of file to parse

    """
    filelist = [os.path.join(path, x) for x in filetype_data(filetype, "filename")]
    for entry in filelist:
            with open(entry, errors='replace') as paf_file:
                for line in paf_file:
                    #Skip headers and footers.
                    parsed_line = parse_line(line, filetype)
                    if (parsed_line[0] and 
                            not (parsed_line[0] == 0 or 
                                 parsed_line[0] == 99999999)):
                        yield parsed_line

def parse_line(line, filetype):
    """Parse line of Address File.

    Splits the input address_line into separate components, and returns a 
    tuple containing these components.

    """
    #Calculate indices at which splits occur.
    splits_indices = [0]
    for x in filetype_data(filetype, "components"):
        splits_indices.append(x + splits_indices[-1]) 
    split_line = (line[splits_indices[x]:splits_indices[x+1]].strip()
                  for x in range(len(splits_indices)-1))
    numerical_line = [] #Try to convert each entry to an integer (if possible)
    for x in split_line:
        try:
            #Check if x has a value, then try to make it an integer.
            x = int(x) if x else x
        except ValueError:
            pass
        numerical_line.append(x)
    return tuple(numerical_line)
