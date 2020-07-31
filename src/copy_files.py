from data.definition import NEW_TRAIN
from data.test_files import TEST_FILES
from data.definition import COPY_FILES
import os
import shutil

for filename in sorted(os.listdir(NEW_TRAIN), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
    if filename in TEST_FILES:
        full_file_name = NEW_TRAIN + filename
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, COPY_FILES)