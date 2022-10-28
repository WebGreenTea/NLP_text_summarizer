
import glob
import pathlib
import os

FileTypes = ('*.txt','*.pdf')
all_files = []
filenames = []
for filestype in FileTypes:
    path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/{filestype}"
    all_files += glob.glob(path)
for filePath in all_files:
    fileName = filePath.split('\\')
    fileName = fileName[len(fileName)-1]
    fileName = fileName.split("_")
    if(len(fileName) < 3):
        continue
    fileName = fileName[2]
    filenames.append(fileName)

print(filenames)