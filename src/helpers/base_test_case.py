import unittest

from helpers.url_helper import URLHelper


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def base_url():

        path = URLHelper.base_project_url() + "/readers/test_files/"
        return path

    @staticmethod
    def cache_url():
        return URLHelper.base_project_url() + "/readers/cache/tests"