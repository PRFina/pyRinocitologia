import glob
import os
import  configparser


class DataManager:

    def __init__(self, assets_path):
        self.assets_dir = assets_path
        self.input_dir = os.path.join(self.assets_dir, "input")
        self.cells_dir = os.path.join(self.assets_dir, "cells")
        self.out_dir = os.path.join(self.assets_dir, "out")
        self._classes = ["eosinofili", "epiteliali", "linfociti", "mastcellule", "mucipare", "neutrofili", "others"]
        self.classes_dir = []
        self._allowed_input_extensions = [".png", ".PNG", ".jpeg", ".JPEG", ".jpg", ".JPG"]
        self._allowed_output_extensions = [".png"]

        for cell_class in self._classes:
            self.classes_dir.append(os.path.join(self.out_dir, cell_class))

    @staticmethod
    def get_file_by_extensions(path, allowed_extensions):
        files = []
        for extension in allowed_extensions:
            files.extend(glob.glob(os.path.join(path, "*" + extension)))
        return files

    def get_input_images(self):
        return DataManager.get_file_by_extensions(self.input_dir, self._allowed_input_extensions)

    def get_cells_images(self):
        return DataManager.get_file_by_extensions(self.cells_dir, self._allowed_input_extensions)

    def get_output_extension(self):
        return self._allowed_output_extensions[0]
