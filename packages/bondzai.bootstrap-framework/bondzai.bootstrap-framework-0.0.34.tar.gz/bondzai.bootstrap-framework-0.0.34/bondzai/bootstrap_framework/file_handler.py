import tarfile
import yaml
import json
import struct as st
from pathlib import Path
from io import BufferedReader


def handle_binary_file_data(data) -> tuple:
    return st.unpack(f"{int(len(data)/4)}f", data)


class Tar:
    """
    Class to handle tar and tar.gz files
    """
    def __init__(self, path: Path):

        self.tar = None
        if path.is_file():
            self.tar = tarfile.open(path, "r")
            self.name_list = self.tar.getnames()

    def get_file(self, file_name: str) -> BufferedReader:
        """
        From file name, get file data
        Args:
            file_name: name of the file
        Returns:
            file: file as reader, should be opened with any dedicated reader

        """
        if self.tar is None:
            raise Exception(f"impossible to load {file_name}, tar file not found")

        file = None
        if file_name in self.name_list:
            member = self.tar.getmember(file_name)
            file = self.tar.extractfile(member)
        return file

    def extract_file(self, file_name: str, folder: Path) -> Path:
        """
        From file name extract the file
        Args:
            file_name: name of the file
            folder: folder where to extract the file
        Returns:
            file_path: file path of the extract file

        """
        if self.tar is None:
            raise Exception(f"impossible to extract {file_name}, tar file not found")

        if not folder.exists():
            folder.mkdir(parents=True)
        file_path = None
        if file_name in self.name_list:
            member = self.tar.getmember(file_name)
            self.tar.extract(member, folder)
            file_path = folder / file_name
        return file_path

    def extract(self, folder: Path):
        """
        Extract all files at once in given folder
        Args:
            folder: folder where to extract the files
        """
        if self.tar is None:
            raise Exception(f"impossible to extract folder {folder}, tar file not found")

        if not folder.exists():
            folder.mkdir(parents=True)
        self.tar.extractall(folder)

    def __del__(self):
        if self.tar:
            self.tar.close()

    def read_yml(self,filepath):
        if self.tar is None:
            raise Exception(f"impossible to read yml {filepath}, tar file not found")

        filepath = filepath.replace("./", "")
        f = self.get_file(filepath)
        data = yaml.safe_load(f)

        return data
    
    def read_binary(self,filepath): 
        if self.tar is None:
            raise Exception(f"impossible to read binary {filepath}, tar file not found")
        filepath = filepath.replace("./", "")
        f = self.get_file(filepath)
        if f is None:
            raise Exception(f" file {filepath} not found")
        d = f.read()
        return handle_binary_file_data(d)

# JSON
def read_json(filepath: Path):
    data = []
    if filepath.is_file():
        with open(filepath, 'r') as fp:
            data = json.load(fp)
    return data

def write_json(filepath: Path,data: dict): 
    with open(filepath, 'w') as fp:
        json.dump(data, fp)
# BINARY
def read_binary(filepath):
    with open(filepath, 'rb' ) as f:
        if f is None:
            raise Exception(f" file {filepath} not found")
        d = f.read()
    return handle_binary_file_data(d)