import os
import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def base_url():

        path = os.path.abspath("s").split("src")[0] + "src/readers/test_files/"
        return path
