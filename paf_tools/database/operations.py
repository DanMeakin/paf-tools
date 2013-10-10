"""Operations module.

Provides various helper functions for carrying out database operations.

"""
import re

def format_address(**args):
    """Properly format an address according to the Royal Mail's recommendations.

    The rules are convoluted but explained from page 27 of the Programmers' 
    Guide to the PAF: http://www.royalmail.com/sites/default/files/docs/pdf/programmers_guide_edition_7_v5.pdf
        
    """
    address = ""
    #Begin with the organisation, if applicable.
    address += args['organisation'] + '\n' if args['organisation'] else ''
    #Add PO Box number
    address += args['PO box'] + '\n' if args['PO box'] else ''
    #Check if sub- and building name and building number
    if (args['sub-building name'] or args['building name'] or 
        args['building number']):
        #Define exception to usual rule of newline for building name.
        #See p. 27 of PAF Guide for details.
        exception_rule = re.compile("^\d.*\d$|^\d.*\d[A-Za-z]$|^.$")
        for x in (args['sub-building name'], args['building name']):
            if x:
                #If the entry is filled, check for exception
                exception = re.match(exception_rule, x)
                if not exception:
                    #Check if final portion of string is numeric/alphanumeric.
                    #If so, split and apply exception to that section only.
                    final_portion = x.split(' ')[-1]
                    if (re.match(exception_rule, final_portion) and not
                        args['building number'] and not
                        re.match('^\d*$', final_portion)):
                        x = ' '.join(x.split(' ')[:-1])
                        address += x + '\n' + final_portion + ' '
                    else:
                        address += x + '\n'
                else:
                    address += x + ', ' if x.isalpha() else x + ' ' 
        address += (args['building number'] + ' ' 
                        if args['building number'] else '')
    #Add thoroughfare if present.
    address += args['thoroughfare'] + '\n' if args['thoroughfare'] else ''
    #Add locality/town and postcode.
    address += args['locality'] + '\n' + args['postcode']
    return address
