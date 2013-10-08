from __future__ import division

__author__ = "John Chase"
__copyright__ = ""
__credits__ = ["John Chase"]
__license__ = "GPL"
__version__ = ""
__maintainer__ = "John Chase"
__email__ = "chasejohnh@gmail.com"
__status__ = "Development"

from shutil import rmtree
from os.path import exists, join
from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files, create_dir
from qiime.util import (get_qiime_temp_dir, 
                        get_tmp_filename)
from qiime.test import initiate_timeout, disable_timeout
from numpy import array

from check_city_map import parse_sample_id, correct_time, add_line_data

class ExampleTests(TestCase):
    
    def setUp(self):
        """ Initialize variables to be used by the tests """
    
    def test_parse_sample_id(self):
        """Does this work when given correct input?"""
        input = 'T3F.3.Ca.013'
        expected = ('toronto', '3', 'floor','3', 'carpet', '013', '2')
        self.assertEqual(parse_sample_id(input), expected)
    
    def test_parse_sample_id_1(self):
        input = 'F1W.3.Ce.003'
        expected = 'flagstaff', '1', 'wall', '3', 'ceiling', '003', '1'
        self.assertEqual(parse_sample_id(input), expected)
    
    def test_parse_sample_id_2(self):
        ''' Does this return an error with incorrect input?'''
        input = 'F1W3.Dr.002'
        self.assertRaises(ValueError, parse_sample_id, input)
        
    def test_parse_sample_id_3(self):
        ''' Does this return an error with incorrect input?'''
        input = 'F32.3Dr.021'
        self.assertRaises(ValueError, parse_sample_id, input)
        
    def test_parse_sample_id_4(self):
        ''' Does this return an error with incorrect input?'''
        input = 'S1S.3.Dr.003'
        self.assertRaises(ValueError, parse_sample_id, input)

    def test_parse_sample_id_5(self):
        ''' Does this return an error with incorrect input?'''
        input = '3C.3.Dr.020'
        self.assertRaises(ValueError, parse_sample_id, input)
    
    def test_correct_time(self):
        '''Does this work with correct input?'''
        input = '16:45:00'
        expected = '16:45:00'
        self.assertEqual(correct_time(input), expected)
        
    def test_correct_time1(self):
        '''Does this work with correct input?'''
        input = '1515'
        expected = '15:15:00'
        self.assertEqual(correct_time(input), expected)
        
    def test_correct_time2(self):
        '''Does this work with correct input?'''
        input = '15:15'
        expected = '15:15:00'
        self.assertEqual(correct_time(input), expected)

    def test_correct_time3(self):
        '''Does this work with incorrect input?'''
        input = '15.153'
        expected = '15:15:00'
        self.assertRaises(ValueError, correct_time, input)
        
    def test_correct_time4(self):
        '''Does this work with incorrect input?'''
        input = 'hello'
        expected = '15:15:00'
        self.assertRaises(ValueError, correct_time, input)
    
    def test_correct_time5(self):
        '''Does this work with incorrect input?'''
        input = '8:45'
        expected = '8:45:00'
        self.assertEqual(correct_time(input), expected)
        
        
    def test_add_line_data(self):
        '''Does this work with correct input'''
        input = 'F3W.3.Dr.002	6/29/2013	450'
        expected = 'F3W.3.Dr.002	6/29/2013	4:50:00	no_data	flagstaff	3	wall	3	drywall	002	1	no_data'
        self.assertEqual(add_line_data(input), expected)
        
    def test_add_line_data1(self):
        '''Does this work with correct input'''
        input = 'T3C.3.Ce.016	8/2/2013	13:43:00	JS	3'
        expected = 'T3C.3.Ce.016	8/2/2013	13:43:00	JS	toronto	3	ceiling	3	ceiling	016	3	3'
        self.assertEqual(add_line_data(input), expected)
        
    def test_add_line_data2(self):
        '''Does this work with correct input'''
        input = 'F2F.3.Ca.009			'
        expected = 'F2F.3.Ca.009	no_data	no_data	no_data	flagstaff	2	floor	3	carpet	009	2	no_data'
        self.assertEqual(add_line_data(input), expected)
        
#         line[0], date, time, notes, city, office, plate_location, row, surface,\
#                time_point, time_point_category, cooler
        
if __name__ == "__main__":
    main()
    
