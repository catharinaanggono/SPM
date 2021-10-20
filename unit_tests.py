# WRITTEN BY WELLSON ARCHUN HAREND (wellsonah.2019)

import unittest
from course_and_class import SectionMaterial
import os

class TestSectionMaterial(unittest.TestCase):
    def setUp(self):
        self.secMat1 = SectionMaterial(1000, 1000, 1, 1, 'Material1.pdf') # FOLDER NOT CREATED YET (CHECK IF EXIST AFTER CREATION)
        self.secMat2 = SectionMaterial(1, 1, 1, 1, 'Material2.pdf') # FOLDER HAS BEEN CREATED (CHECK FOR EXIST TO PROHIBIT CREATION)
    
    def tearDown(self):
        self.secMat1 = None
        self.secMat2 = None
    
    def test_create_path(self):
        create = self.secMat1.create_path() # Create path based on CourseID, ClassID, SectionID, and MaterialContent
        path = 'course_material/' + str(self.secMat1.CourseID) + '/' + str(self.secMat1.ClassID) + '/' + str(self.secMat1.SectionID)
        self.assertTrue(os.path.isdir(path))

if __name__ == '__main__':
    unittest.main()