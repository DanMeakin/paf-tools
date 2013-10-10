"""Tables module.

Defines the SQLAlchemy tables as declarative_base classes. 

"""
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from paf_tools.database.operations import format_address

#Use the declarative base to create database tables and fields.
Base = declarative_base()

class Address(Base):
    __tablename__ = "addresses"

    #id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    postcode = Column(String(7))
    address_key = Column(Integer, primary_key=True)
    locality_id = Column(Integer, ForeignKey('localities.id'))
    thoroughfare_id = Column(Integer, ForeignKey('thoroughfares.id'))
    thoroughfare_descriptor_id = Column(
            Integer, 
            ForeignKey('thoroughfare_descriptors.id')
            )
    dependent_thoroughfare_id = Column(
            Integer,
            ForeignKey('thoroughfares.id')
            )
    dependent_thoroughfare_descriptor_id = Column(
            Integer,
            ForeignKey('thoroughfare_descriptors.id')
            )
    building_number = Column(Integer)
    building_name_id = Column(Integer, ForeignKey('building_names.id'))
    sub_building_name_id = Column(Integer, ForeignKey('sub_building_names.id'))
    num_households = Column(Integer)
    organisation_id = Column(
            Integer, 
            ForeignKey('organisations.id'), 
            primary_key=True
            )
    postcode_type = Column(String(1), primary_key=True)
    concatenation_indicator = Column(String(1))
    delivery_point_suffix = Column(String(2))
    small_user_org_indicator = Column(String(1))
    po_box_num = Column(String(6))

    locality = relationship(
            "Locality", 
            backref=backref('addresses')
            )
    thoroughfare = relationship(
            "Thoroughfare", 
            backref=backref('addresses'),
            foreign_keys=[thoroughfare_id],
            )
    thoroughfare_descriptor = relationship(
            "ThoroughfareDescriptor", 
            backref=backref('addresses'),
            foreign_keys=[thoroughfare_descriptor_id],
            )
    dependent_thoroughfare = relationship(
            "Thoroughfare",
            foreign_keys=[dependent_thoroughfare_id],
            )
    dependent_thoroughfare_descriptor = relationship(
            "ThoroughfareDescriptor",
            foreign_keys=[dependent_thoroughfare_descriptor_id],
            )
    building_name = relationship(
            "BuildingName",
            backref=backref('addresses')
            )
    sub_building_name = relationship(
            "SubBuildingName",
            backref=backref('addresses')
            )
    organisation = relationship(
            "Organisation",
            backref=backref('addresses')
            )

    def __init__(self, postcode, address_key, locality_id, thoroughfare_id, 
                 thoroughfare_descriptor_id, dependent_thoroughfare_id,
                 dependent_thoroughfare_descriptor_id, building_number,
                 building_name_id, sub_building_name_id, num_households,
                 organisation_id, postcode_type, concatenation_indicator, 
                 delivery_point_suffix, small_user_org_indicator, po_box_num):
        self.postcode = postcode
        self.address_key = address_key
        self.locality_id = locality_id
        self.thoroughfare_id = thoroughfare_id
        self.thoroughfare_descriptor_id = thoroughfare_descriptor_id
        self.dependent_thoroughfare_id = dependent_thoroughfare_id
        self.dependent_thoroughfare_descriptor_id = dependent_thoroughfare_descriptor_id
        self.building_number = building_number
        self.building_name_id = building_name_id
        self.sub_building_name_id = sub_building_name_id
        self.num_households = num_households
        self.organisation_id = organisation_id
        self.postcode_type = postcode_type
        self.concatenation_indicator = concatenation_indicator
        self.delivery_point_suffix = delivery_point_suffix
        self.small_user_org_indicator = small_user_org_indicator
        self.po_box_num = po_box_num

    def __repr__(self):
        return "<Address: {}>".format(
                format_address(**self._get_elements()).replace('\n', ', ')
                )

    def __str__(self):
        """String representation of Address.

               """
        return format_address(**self._get_elements()) 

    def _get_elements(self):
        """Get address elements for string representation."""
        address_elements = {
                'organisation': str(self.organisation) 
                                if self.organisation else None,
                'sub-building name': str(self.sub_building_name) 
                                     if self.sub_building_name else None,
                'building name': str(self.building_name)
                                 if self.building_name else None,
                'building number': str(self.building_number)
                                   if self.building_number else None,
                'PO box': str(self.po_box_num) if self.po_box_num else None,
                'dependent thoroughfare': "{} {}".format(
                    str(self.dependent_thoroughfare), 
                    str(self.dependent_thoroughfare_descriptor)
                    ) if self.dependent_thoroughfare else None,
                'thoroughfare': "{} {}".format(
                    str(self.thoroughfare), 
                    str(self.thoroughfare_descriptor),
                    ) if self.thoroughfare else None,
                'locality': str(self.locality),
                'postcode': "{} {}".format(
                    self.postcode[:-3], 
                    self.postcode[-3:]
                    ),
                }
        return address_elements

#class WelshAddress(Address):
#    __tablename__ = "welsh_addresses"


class BuildingName(Base):
    __tablename__ = "building_names"

    id = Column(Integer, primary_key=True)
    building_name = Column(String(50))

    def __init__(self, building_name_id, building_name=None):
        self.id = building_name_id
        self.building_name = building_name

    def __repr__(self):
        return "<Building Name: {}>".format(self.building_name).title()

    def __str__(self):
        return self.building_name.title()


class Locality(Base):
    __tablename__ = "localities"

    id = Column(Integer, primary_key=True)
    post_town = Column(String(30))
    dependent_locality = Column(String(35))
    double_dependent_locality = Column(String(35))

    def __init__(self, locality_id, filler_1=None, filler_2=None, 
                 post_town=None, dependent_locality=None, 
                 double_dependent_locality=None):
        #Two filler variables are defined to allow the populator function 
        #elsewhere to populate the database without throwing an error.
        self.id = locality_id
        self.post_town = post_town
        self.dependent_locality = dependent_locality
        self.double_dependent_locality = double_dependent_locality

    def __repr__(self):
        return "<Locality: {}{}{}>".format(
                self.double_dependent_locality + ", " 
                    if self.double_dependent_locality else "",
                self.dependent_locality + ", "
                    if self.dependent_locality else "",
                self.post_town
                ).title()

    def __str__(self):
        return "{}{}{}".format(
                self.double_dependent_locality + "\n"
                    if self.double_dependent_locality else "",
                self.dependent_locality + "\n"
                    if self.dependent_locality else "",
                self.post_town
                ).title()
                

class Mailsort(Base):
    __tablename__ = "mailsort"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    postcode_sector = Column(String(5), unique=True)
    selection_code = Column(Integer)

    def __init__(self, postcode_sector, selection_code):
        self.postcode_sector = postcode_sector
        self.selection_code = selection_code

    def __repr__(self):
        return "<Mailsort: {} - {}>".format(
                self.postcode_sector, 
                self.selection_code
                )


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True)
    postcode_type = Column(String(1), primary_key=True)
    organisation_name = Column(String(60))
    department_name = Column(String(60))

    def __init__(self, organisation_id, postcode_type=None, 
                 organisation_name=None, department_name=None, filler=None):
        self.id = organisation_id
        self.postcode_type = postcode_type
        self.organisation_name = organisation_name
        self.department_name = department_name

    def __repr__(self):
        return "<Organisation: {}{}>".format(
                self.department_name + ", " if self.department_name else "",
                self.organisation_name if self.organisation_name else "(unnamed)",
                ).title()

    def __str__(self):
        return "{}{}".format(
                self.organisation_name 
                    if self.organisation_name else "(unnamed)",
                "\n" + self.department_name 
                    if self.department_name else ""
                ).title()


class SubBuildingName(Base):
    __tablename__ = "sub_building_names"

    id = Column(Integer, primary_key=True)
    sub_building_name = Column(String(30))

    def __init__(self, sub_building_id, sub_building_name=None):
        self.id = sub_building_id
        self.sub_building_name = sub_building_name

    def __repr__(self):
        return "<Sub-Building Name: {}>".format(self.sub_building_name).title()

    def __str__(self):
        return self.sub_building_name.title()

class Thoroughfare(Base):
    __tablename__ = "thoroughfares"

    id = Column(Integer, primary_key=True)
    thoroughfare_name = Column(String(60))

    def __init__(self, thoroughfare_id, thoroughfare_name=None):
        self.id = thoroughfare_id
        self.thoroughfare_name = thoroughfare_name

    def __repr__(self):
        return "<Thoroughfare: {}>".format(self.thoroughfare_name).title()

    def __str__(self):
        return self.thoroughfare_name.title()


class ThoroughfareDescriptor(Base):
    __tablename__ = "thoroughfare_descriptors"

    id = Column(Integer, primary_key=True)
    thoroughfare_descriptor = Column(String(20))
    approved_abbreviation = Column(String(6))

    def __init__(self, thoroughfare_descriptor_id, 
                 thoroughfare_descriptor=None, approved_abbreviation=None):
        self.id = thoroughfare_descriptor_id
        self.thoroughfare_descriptor = thoroughfare_descriptor
        self.approved_abbreviation = approved_abbreviation

    def __repr__(self):
        return "<Thoroughfare Descriptor: {}>".format(
                self.thoroughfare_descriptor
                ).title()

    def __str__(self):
        return self.thoroughfare_descriptor.title()
