
import glob
import pathlib
import os

FileTypes = ('*.txt','*.pdf')
all_files = []
for filestype in FileTypes:
    path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/{filestype}"
    all_files += glob.glob(path)


print(all_files)