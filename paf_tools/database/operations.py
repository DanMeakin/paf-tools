"""Operations module.

Provides various helper functions for carrying out database operations.

"""
import re
from sqlalchemy import MetaData
from paf_tools.database import engine
from paf_tools.database.tables import Base

#############################
# Database helper functions #
#############################

def erase_database():
    """Erase contents of database and start over."""
    metadata = MetaData(engine)
    metadata.reflect()
    metadata.drop_all()
    Base.metadata.create_all(engine)
    return None

#############################
# Data formatting functions #
#############################

def format_address(**args):
    """Properly format an address according to the Royal Mail's recommendations.

    The rules are convoluted but explained from page 27 of the Programmers' 
    Guide to the PAF: http://www.royalmail.com/sites/default/files/docs/pdf/programmers_guide_edition_7_v5.pdf
        
    """
    #Begin with the organisation and PO Box number, if applicable.
    address = ''.join([args[entry] + '\n' 
                       for entry in ['organisation', 'PO box']
                       if args.get(entry)])
    #Format building name/number components.
    address += format_building_components(*[args.get(x) for x in 
                                            ['sub-building name', 
                                             'building name', 
                                             'building number',
                                             'concatenation indicator']])
   #Add thoroughfare (if present), locality/town and postcode.
    address += ''.join([args[entry] + '\n' 
                        for entry in ['dependent thoroughfare', 
                                      'thoroughfare',
                                      'double dependent locality',
                                      'dependent locality',
                                      'town',
                                      'postcode']
                        if args.get(entry)])
    return address.strip()

def format_building_components(sub_building_name=None, 
                               building_name=None, 
                               building_number=None,
                               concatenation_indicator=False):
    """Properly format building name/number components.

    Follows the rules laid down in the Royal Mail's Programmers' Guide.

    """
    #Check if sub- and building name and building number
    if not (sub_building_name or building_name or building_number):
        return ""
    #Check if concatenation indicator is True. If so, simply concat and return.
    if concatenation_indicator:
        return str(building_number or '') + sub_building_name + ' '
    #Define exception to usual rule of newline for building name.
    #See p. 27 of PAF Guide for details.
    return_str = ""
    exception_rule = re.compile("^\d.*\d$|^\d.*\d[A-Za-z]$|^.$")
    for x in (sub_building_name, building_name):
        if x:
            #If the entry is filled, check for exception
            if re.match(exception_rule, x):
                return_str += x + ', ' if x.isalpha() else x + ' '
            else:
                #Check if final portion of string is numeric/alphanumeric.
                #If so, split and apply exception to that section only.
                final_portion = x.split(' ')[-1]
                if (re.match(exception_rule, final_portion) and not
                    building_number and not
                    re.match('^\d*$', final_portion)):
                    x = ' '.join(x.split(' ')[:-1])
                    return_str += x + '\n' + final_portion + ' '
                else:
                    return_str += x + '\n'
    return_str += str(building_number) + ' ' if building_number else ''
    return return_str
 
