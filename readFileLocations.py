import os
import shutil
import hashlib
from datetime import datetime

class Savelocation:
    def __init__(self, appname):
        assert (appname != ""), "Appname is empty, check formatting of locations.txt"
        self.appName = appname
        self.filePaths = []

    def __str__(self):
        return f"Checking application: {self.appName} | paths: {self.filePaths}"

    def addLocation(self, location):
        self.filePaths.append(location)

def calculateFolderHash(folderPath, algorithm='sha256', block_size=65536):
    """Calculate the hash of all files in a folder using the specified algorithm"""
    hash_object = hashlib.new(algorithm)
    for foldername, subfolders, filenames in os.walk(folderPath):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hash_object.update(block)
    return hash_object.hexdigest()

def readLocationsFile():
    """Make a list of Savelocation instances and return it"""
    
    f = open("locations.txt", "r")
    lines = f.readlines()
    f.close()

    saveLocations = []
    currentSaveLocation = None
    blank = True
    for line in lines:
        linestripped = line.strip()
        if (blank):
            #print("ADDED APP NAME : ",linestripped)
            currentSaveLocation = Savelocation(linestripped)
            blank = False
        elif (len(linestripped) <= 1):
            #add instance to list
            blank = True
            saveLocations.append(currentSaveLocation)
        else:
            #print("FILE PATH : ",linestripped)
            currentSaveLocation.addLocation(linestripped)

    if (not blank):
        saveLocations.append(currentSaveLocation)

    return saveLocations

def remove_folder(path):
    try:
        shutil.rmtree(path, True)
    except Exception as e:
        print(f"Error removing folder {path}: {e}")

def newestFile(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getmtime)

def saveData(saveLocations, output=True):
    isaltered = False
    changed = []

    for save in saveLocations:
        if output: print(save)

        if (not save.filePaths):
            if output: print("There are no file paths for this item... skipping")
            continue

        for path in save.filePaths:
            if not os.path.isdir(path):
                if output: print("Path doesn't exist |", path)
                if (path == save.filePaths[-1]):
                    if output: print("---------------------------------------------------------------------------")
                continue # skip to next path iteration

            pathHash = calculateFolderHash(path)
            fileTime = datetime.fromtimestamp(os.stat(newestFile(path)).st_mtime)
            if output: print("File modified |", fileTime)
            fileInfoPath = os.path.join('saves', f'{save.appName}.txt')
            backupPath = os.path.join('backup', f'{save.appName} {fileTime.strftime("%Y-%m-%d_%H-%M-%S")}')
            if output: print("Save data hash |", pathHash)

            # check if an info file exists, and 
            # if it does read the hash from it
            oldHash = ""
            if (os.path.isfile(fileInfoPath)):
                with open(fileInfoPath, "r") as f:
                    lines = f.readlines()
                    oldHash = lines[1]
                    if output: print("Info file hash |", oldHash)
            else:
                if output: print("No info file |", fileInfoPath)

            if (oldHash != pathHash):
                if output: print("Copying path |", path)

                isaltered = True
                changed.append(f"{save.appName} [{fileTime.strftime("%Y-%m-%d %H:%M.%S")}]")
                remove_folder(os.path.join('saves', save.appName))

                if output: print("Compressing file...")
                shutil.make_archive(os.path.join('saves', save.appName), 'zip', path)  # zip file
                fileSize = os.path.getsize(os.path.join('saves', f'{save.appName}.zip'))  # check file size of zip
                if (fileSize > 100000000): # files above 100MB are too big for github, so just use the folder instead
                    if output: print("Zip is too big, using folder directory instead")
                    shutil.copytree(path, os.path.join('saves', save.appName), dirs_exist_ok=True)
                    os.remove(os.path.join('saves', f'{save.appName}.zip'))

                newinfo = [str(fileTime) + "\n", pathHash]
                with open(fileInfoPath, 'w') as f:
                    f.writelines(newinfo)

                if output: print("Backing up path |", path)
                remove_folder(backupPath)
                shutil.copytree(path, backupPath, dirs_exist_ok=True)
                with open(f'{backupPath}.txt', 'w') as f:
                    f.writelines(newinfo)
            else:
                if output: print("Files are the same... not copying files")
            if output: print("---------------------------------------------------------------------------")

    return isaltered, changed