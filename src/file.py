import os
from pathlib import Path
import logging

class File:
    @staticmethod
    def path_exists(input_path: str, with_error: bool = False) -> bool:
        if os.path.exists(input_path):
            return True
        else:
            if with_error:
                logging.warning(f"Input path '{input_path}' does not exist.")

            return False

    @staticmethod
    def home_dir() -> str:
        return Path.home()

    @staticmethod
    def separate_extension(input_path: str):
        tuple = os.path.splitext(input_path)
        if tuple[1] is None:
            logging.warning(f"Input path '{input_path}' has no extension")
        
        return tuple

    @staticmethod
    def rename(input_path: str, new_name: str):
        os.rename(input_path, new_name)

    @staticmethod
    def append_to_filename(input_path: str, append_string: str):
        filename_tuple = File.separate_extension(input_path)
        new_filename = filename_tuple[0] + append_string + filename_tuple[1]
        File.rename(input_path, new_filename)

    @staticmethod
    def get_file_extension(input_path: str) -> str:
        return Path(input_path).suffix

    @staticmethod
    def check_extension(input_path: str, desired_extension: str, with_error: bool = False) -> bool:
        file_extension = File.get_file_extension(input_path)
        if file_extension == desired_extension:
            return True
        else:
            if with_error:
                logging.warning(f"File extension of path '{input_path}' does match the desired extension '{desired_extension}'.")

            return False

    @staticmethod
    def create_dir(dir_name: str):
        if not File.path_exists(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def create_file(filename: str):
        if not File.path_exists(filename):
            os.mknod(filename)

    @staticmethod
    def count_files(input_path: str):
        return len([name for name in os.listdir(input_path) if os.path.isfile(name)])

    @staticmethod
    def remove(input_path: str):
        os.remove(input_path)

    @staticmethod
    def only_filename(input_path: str, with_extension: bool = True) -> str:
        filename = os.path.basename(input_path)
        if with_extension:
            return filename
        else:
            pure_filename, _ = File.separate_extension(filename)
            return pure_filename
