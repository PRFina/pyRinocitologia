import datetime as dt
import hashlib
import json
import argparse


def generate_id():
    """
    Generate a unique id based on the current date and time.

    Note that in this context md5 hash collision or other vulnerabilities are not
    issues.

    :return: the md5 digest string as id
    """
    date = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    md5 = hashlib.md5()
    md5.update(date.encode())
    return md5.hexdigest()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a pre-filled template file for dataset metadata")

    parser.add_argument("--show", action='store_true', help="Show file content in stdout")
    parser.add_argument("-o", "--outfile", default="info.json", help="Output file")
    parser.add_argument("-i", "--iteration", default="2", help="Project iteration which dataset belongs to")
    parser.add_argument("-l", "--location", default="Policlinico di Bari", help="Location where data had been acquired")
    parser.add_argument("-m", "--magnification", default="1000x", help="Microscope magnification factor used in field acquisiton")
    parser.add_argument("-c", "--content", default="Nasal Smear", help="Content of slides where data is acquired from")
    parser.add_argument("-t", "--technique", default="Cytospin", help="Any technique used in data preparation phase")
    parser.add_argument("-s", "--staining", default="MGG", help="Staining used in data preparation phase")
    parser.add_argument("-p", "--people", nargs="+", default=["Dott. Matteo Gelardi", "Pio Raffale Fina", "Francesco Troccoli"], help="People that contributed to the dataset")
    parser.add_argument("--extra", nargs="+", help="List of <key>:<value> to add to the file")

    args = vars(parser.parse_args())  # parse and build arguments dict

    datetime = dt.datetime.now()
    date_str = datetime.strftime("%d/%m/%Y")
    time_str = datetime.strftime("%H:%M:%S")

    metadata = dict()
    metadata["id"] = generate_id()
    metadata["iteration"] = args["iteration"]
    metadata["acquisition_date"] = date_str
    metadata["acquisition_time"] = time_str
    metadata["acquisition_location"] = args["location"]
    metadata["magnification_factor"] = args["magnification"]
    metadata["content"] = args["content"]
    metadata["technique"] = args["technique"]
    metadata["staining"] = args["staining"]
    metadata["people"] = args["people"]

    # Add "extra" arguments value to the dict
    pairs = args["extra"]
    if pairs is not None:
        for pair in pairs:
            k, v = pair.split(":")
            metadata[k] = v

    with open(args["outfile"], "w") as file:
        json.dump(metadata, file, indent=4)
        print("File created successfully!")

    if args["show"]:
        print("************************\n{}\n************************".format(metadata))
