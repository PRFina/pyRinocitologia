from pathlib import Path
import random as rnd
import shutil


class Sampler:

    def __init__(self,  in_dir,  is_flat=False, extension="png",seed=420):

        rnd.seed(seed)

        self.in_dir = Path(in_dir)

        self.is_flat = is_flat
        self.extension = extension

        self.samples = []

    def get_dataset_size(self):
        return len(list(self.in_dir.glob("**/*.{}".format(self.extension))))

    def sampling(self, sample_size=10, percent=None):
        if percent:
            k = int((percent / self.get_dataset_size()) * 100)
        else:
            k = sample_size

        if sample_size > self.get_dataset_size():
            raise ValueError("Not enough samples to sample, lower the sample size")

        if not self.is_flat:
            dirs = [dir for dir in self.in_dir.glob("*") if dir.is_dir()]
            k = k // len(dirs)  # sampling equally in each folder

            for dir in dirs:
                files = list(dir.glob("*.{}".format(self.extension)))
                if k > len(files):
                    self.samples.extend(rnd.sample(files, len(files)))
                else:
                    self.samples.extend(rnd.sample(files, k))
        else:
            files = list(self.in_dir.glob("*.{}".format(self.extension)))
            self.samples.extend(rnd.sample(files, k))

        return [str(file) for file in self.samples]

    def create_dataset_from_sample(self, out_dir):
        out_dir = Path(out_dir)
        out_dir.mkdir()

        for i, file in enumerate(self.samples):
            shutil.copy(file,  out_dir / "{}-.png".format(i + 1))


class LatexDoc:
    """
    Small Utility class to write python variables as latex command and than use in a latex document

    Simple usage: instantiate an object, add a bunch of variables, call toTex() method to write out
    a tex file
    """

    def __init__(self):
        self.variables = {}

    def add_variable(self, name, value):
        self.variables[name] = value

    def toTex(self, out_path="generated", file_name="Latex_Snippet.tex"):
        path = Path(out_path) / file_name

        with path.open("w") as file:
            for name, value in self.variables.items():
                camelized = "".join(w.capitalize() for w in name.split("_")) ## due to latex syntax limitation
                latex_command = "\\newcommand{{\\var{name}}}{{{value}}}\n".format(name=camelized, value=value)
                file.writelines(latex_command)
