"""
Script to setup the repository environment
"""

import subprocess
from pathlib import Path

DATASET_REPO_URL = 'https://github.com/PRFina/Rinocitologia-Datasets.git'
DATASET_DIR_NAME = 'Datasets'
CONFIG_FILE_NAME = 'config.ini'
cwd = Path(".")



print("1) Downloading datasets")
subprocess.call(['git','clone', DATASET_REPO_URL, DATASET_DIR_NAME])
print("DONE")



print("2) Creating Data directory structure")
data_dir = Path('data')
if not data_dir.exists():
	data_dir.mkdir()

assets_dir = data_dir / 'assets'
if not assets_dir.exists():
	assets_dir.mkdir()

top_level = ['cells','input','out']

for dirname in top_level:
	(assets_dir / dirname).mkdir()

classes = ['epiteliali','neutrofili','eosinofili','mastcellule','linfociti','mucipare','altro']

out_dir = assets_dir / 'out'
for class_name in classes:
	(out_dir / class_name).mkdir()
print("DONE")



print("3) Renaming configuration file")
config_file = Path(CONFIG_FILE_NAME + '.example')
try:
	config_file.rename(CONFIG_FILE_NAME)
except:
	print('Configuration file not found!')
print("DONE")