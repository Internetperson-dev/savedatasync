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

def calculateFolderHash(folder_path):
    hasher = hashlib.sha256()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
            except FileNotFoundError:
                print(f"Skipping missing file: {file_path}")
            except PermissionError:
                print(f"Skipping unreadable file: {file_path}")
    return hasher.hexdigest()

def readLocationsFile():
    """Make a list of Savelocation instances and return it"""
    
    f = open("locations.txt", "r")
    lines = f.readlines()
    f.close()

    # Remove trailing blank lines
    while len(lines) > 0 and lines[-1].strip() == "":
        lines.pop()

    saveLocations = []
    currentSaveLocation = None
    blank = True

    for line in lines:
        linestripped = line.strip()
        if blank:
            currentSaveLocation = Savelocation(linestripped)
            blank = False
        elif len(linestripped) <= 1:
            saveLocations.append(currentSaveLocation)
            blank = True
        else:
            currentSaveLocation.addLocation(linestripped)

    if not blank:
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
