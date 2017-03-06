import os
import pickle


class FileHelper:

    @staticmethod
    def read_object_from_disk(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as input:
                tmp_cached_game_list = pickle.load(input)
                return tmp_cached_game_list

    @staticmethod
    def save_object_to_disk(game_list, file_path):

        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # save list to disk
        with open(file_path, 'wb') as output:
            pickle.dump(game_list, output, pickle.HIGHEST_PROTOCOL)
