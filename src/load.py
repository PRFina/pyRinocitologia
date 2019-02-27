import glob
import os

def get_file_by_extensions(path, allowed_extensions, sep=";"):
    files = []
    for extension in allowed_extensions.split(sep):
        files.extend(glob.glob(os.path.join(path, "*" + extension)))
    return files
