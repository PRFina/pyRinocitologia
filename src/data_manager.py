import glob
import os
import  configparser


class DataManager:

    def __init__(self, assets_path):
        self.assets_dir = assets_path
        self.input_dir = os.path.join(self.assets_dir, "input")
        self.cells_dir = os.path.join(self.assets_dir, "cells")
        self.out_dir = os.path.join(self.assets_dir, "out")
        self._allowed_input_extensions = [".png", ".PNG", ".jpeg", ".JPEG", ".jpg", ".JPG"]
        self._allowed_output_extensions = [".png"]

        self._classes = {0: "epiteliali",
                         1: "neutrofili",
                         2: "eosinofili",
                         3: "mastcellule",
                         4: "linfociti",
                         5: "mucipare",
                         6: "others"
                         }

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

    def get_cell_class_dir(self, class_index):
        return os.path.join(self.out_dir, self._classes[class_index])
