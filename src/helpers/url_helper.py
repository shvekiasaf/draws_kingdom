import os


class URLHelper:

    @staticmethod
    def base_project_url():

        path = os.path.abspath("s").split("draws_kingdom")[0] + "draws_kingdom/src"
        return path

    @staticmethod
    def cache_folder_path():
        cache_folder_path = URLHelper.base_project_url() + "/readers/cache/"
        return cache_folder_path
