import os
import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def base_url():

        path = os.path.abspath("s").split("draws_kingdom")[0] + "draws_kingdom/src/readers/test_files/"
        return path
