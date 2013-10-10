from nose.tools import *
from paf_tools.files_parser import *

class TestLineParsing(object):

    def setup(self):
        print("Setup")

    def teardown(self):
        print("Teardown")

    @classmethod
    def setup_class(cls):
        print("Setup class")

    @classmethod
    def teardown_class(cls):
        print("Teardown_class")

    def test_line_parser(self):
        line = "x" * 200
        address_tuple = (
                "x"*7, "x"*8, "x"*6, "x"*8, "x"*4, "x"*8, "x"*4,
                "x"*4, "x"*8, "x"*8, "x"*4, "x"*8, "x"*1, "x"*1, 
                "x"*2, "x"*1, "x"*6)
        building_name_tuple = (
                "x"*8, "x"*50
                )
        locality_tuple = (
                "x"*6, "x"*30, "x"*15, "x"*30, "x"*35, "x"*35
                )
        mailsort_tuple = (
                "x"*5, "x"*5
                )
        organisation_tuple = (
                "x"*8, "x"*1, "x"*60, "x"*60, "x"*24
                )
        sub_building_name_tuple = (
                "x"*8, "x"*30
                )
        thoroughfare_tuple = (
                "x"*8, "x"*60
                )
        thoroughfare_descriptor_tuple = (
                "x"*4, "x"*20, "x"*6
                )
        assert_equal(
                parse_line(line, "address"), 
                address_tuple
                )
        assert_equal(
                parse_line(line, "building_name"), 
                building_name_tuple
                )
        assert_equal(
                parse_line(line, "locality"), 
                locality_tuple
                )
        assert_equal(
                parse_line(line, "mailsort"), 
                mailsort_tuple
                )
        assert_equal(
                parse_line(line, "organisation"), 
                organisation_tuple
                )
        assert_equal(
                parse_line(line, "sub_building_name"), 
                sub_building_name_tuple
                )
        assert_equal(
                parse_line(line, "thoroughfare"), 
                thoroughfare_tuple
                )
        assert_equal(
                parse_line(line, "thoroughfare_descriptor"),
                thoroughfare_descriptor_tuple
                )
