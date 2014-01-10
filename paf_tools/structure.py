"""Structure module.

Contains the names of the various files contained within the PAF Mainfile, 
and defines their internal structure for parsing purposes.

The PAF Mainfile is made up of a number of separate components:-

    * Address Files;
    * Localities File;
    * Thoroughfare (and Dependent Thoroughfare) File;
    * Thoroughfare (and Dependent Thoroughfare) Descriptor;
    * Building Names File;
    * Sub Building Names File;
    * Organisations File;
    * Mailsort File; and
    * Welsh Address File.

Filenames are as follows:-

COMPONENT                       FILENAME
----------------------------------------------
Address Files                   fpmainfl.c02-6
Building Names File             bname.c01
Localities File                 local.c01
Mailsort File                   mailsort.c01
Organisations File              org.c01
Sub Building Names File         subbname.c01
Thoroughfare File               thfare.c01
Thoroughfare Descriptor File    thdesc.c01
Welsh Address File              wfmainfl.c06
----------------------------------------------

These may change, so this module makes it trivial to implement changes 
to filenames.

"""
###########################
# FILETYPES AND DATATYPES #
###########################
VALID_FILETYPES = [
        'ADDRESS', 'BUILDING_NAME', 'LOCALITY', 'MAILSORT', 
        'ORGANISATION', 'SUB_BUILDING_NAME', 'THOROUGHFARE', 
        'THOROUGHFARE_DESCRIPTOR', #'WELSH_ADDRESS'
        ]
VALID_DATATYPES = [
        'FILENAME', 'COMPONENTS'
        ]

########################
# FILENAME DEFINITIONS #
########################
ADDRESS_FILENAME = ["fpmainfl.c0" + str(x) for x in range(2, 7)] #Series of files 
BUILDING_NAME_FILENAME = "bname.c01"
LOCALITY_FILENAME = "local.c01"
MAILSORT_FILENAME = "mailsort.c01"
ORGANISATION_FILENAME = "org.c01"
SUB_BUILDING_NAME_FILENAME = "subbname.c01"
THOROUGHFARE_FILENAME = "thfare.c01"
THOROUGHFARE_DESCRIPTOR_FILENAME = "thdesc.c01"
WELSH_ADDRESS_FILENAME = "wfmainfl.c06"

#########################
# STRUCTURE DEFINITIONS #
#########################
ADDRESS_COMPONENTS = [
        7, #Postcode
        8, #Address Key
        6, #Locality Key 
        8, #Thoroughfare Key
        4, #Thoroughfare Descriptor Key
        8, #Dependent Thoroughfare Key
        4, #Dependent Thoroughfare Descriptor Key
        4, #Building Number
        8, #Building Name Key
        8, #Sub Building Name Key
        4, #Number of Households
        8, #Organisation Key
        1, #Postcode Type
        1, #Concatenation Indicator
        2, #Delivery Point Suffix
        1, #Small User Organisation Indicator
        6, #PO Box Number
        ]
BUILDING_NAME_COMPONENTS = [
        8,  #Building Name Key
        50, #Building Name
        ]
LOCALITY_COMPONENTS = [
        6,  #Locality Key
        30, #Filler
        15, #Filler
        30, #Post Town
        35, #Dependent Locality
        35, #Double Dependent Locality
        ]
MAILSORT_COMPONENTS = [
        5, #Postcode Sector
        5, #Standard Selection Code
        ]
ORGANISATION_COMPONENTS = [
        8,  #Organisation Key
        1,  #Postcode Type
        60, #Organisation Name
        60, #Department Name
        24, #Filler
        ]
SUB_BUILDING_NAME_COMPONENTS = [
        8,  #Sub Building Name Key
        30, #Sub Building Name
        ]
THOROUGHFARE_COMPONENTS = [
        8,  #Thoroughfare Key
        60, #Thoroughfare Name
        ]
THOROUGHFARE_DESCRIPTOR_COMPONENTS = [
        4,  #Thoroughfare Descriptor Key
        20, #Thoroughfare Descriptor
        6,  #Approved Abbreviation
        ]
