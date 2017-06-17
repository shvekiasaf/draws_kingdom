import os.path
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

    def clean_cache_files(self, pattern):
        import re, os.path
        for root, dirs, files in os.walk(BaseTestCase.cache_url()):
            for file in filter(lambda x: re.match(pattern, x), files):
                os.remove(os.path.join(root, file))
        pass