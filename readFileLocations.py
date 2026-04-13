import os
import shutil
import hashlib
from datetime import datetime

class bcolors:
    LINE = '\x1b[90m'
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKCYAN = '\x1b[96m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'

class Savelocation:
    def __init__(self, appname):
        assert (appname != ""), "Appname is empty, check formatting of locations.txt"
        self.appName = appname
        self.filePaths = []

    def __str__(self):
        return "Checking application: {0}{1}{2} | paths: {3}".format(bcolors.OKGREEN, self.appName, bcolors.ENDC, self.filePaths)

    def addLocation(self, location):
        self.filePaths.append(location)


def calculateFolderHash(folderPath, algorithm='sha256', block_size=65536):
    """Calculate the hash of all files in a folder using the specified algorithm"""
    hash_object = hashlib.new(algorithm)
    for foldername, subfolders, filenames in os.walk(folderPath):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'rb') as f:
                while True:
                    block = f.read(block_size)
                    if not block:
                        break
                    hash_object.update(block)
    return hash_object.hexdigest()


def readLocationsFile():
    """Make a list of Savelocation instances and return it"""
    
    f = open("locations.txt", "r")
    lines = f.readlines()
    f.close()

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
            blank = True
            saveLocations.append(currentSaveLocation)
        else:
            currentSaveLocation.addLocation(linestripped)

    if not blank:
        saveLocations.append(currentSaveLocation)

    return saveLocations


def remove_folder(path):
    try:
        shutil.rmtree(path, True)
    except Exception as e:
        print "Error removing folder {0}: {1}".format(path, str(e))


def newestFile(path):
    if os.path.isfile(path):
        return path
    else:
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getmtime)


def saveData(saveLocations, output=True):
    isaltered = False
    changed = []

    for save in saveLocations:
        if output: print save

        if (not save.filePaths):
            if output: print "There are no file paths for this item... skipping"
            continue

        for path in save.filePaths:
            if not os.path.isdir(path):
                if os.path.isfile(path):
                    if output: print "Is single file... continue"
                else:
                    if output: print "Path doesn't exist | {0}".format(path)
                    if (path == save.filePaths[-1]):
                        if output: print "{0}---------------------------------------------------------------------------{1}".format(bcolors.LINE, bcolors.ENDC)
                    continue # skip to next path iteration

            pathHash = calculateFolderHash(path)
            try:
                fileTime = datetime.fromtimestamp(os.stat(newestFile(path)).st_mtime)
            except:
                fileTime = datetime.fromtimestamp(0)
                print "Folder is empty!"
            if output: print "File modified | {0}".format(fileTime)
            fileInfoPath = os.path.join('saves', '{0}.txt'.format(save.appName))
            backupPath = os.path.join('backup', '{0} {1}".format(fileTime.strftime("%Y-%m-%d_%H-%M-%S"), save.appName))
            if output: print "Save data hash | {0}".format(pathHash)

            # check if an info file exists, and 
            # if it does read the hash from it
            oldHash = ""
            if (os.path.isfile(fileInfoPath)):
                with open(fileInfoPath, "r") as f:
                    lines = f.readlines()
                    oldHash = lines[1]
                    if output: print "Info file hash | {0}".format(oldHash)
            else:
                if output: print "No info file | {0}".format(fileInfoPath)

            if (oldHash != pathHash):
                if output: print "{0}Copying path | {1}{2}".format(bcolors.WARNING, path, bcolors.ENDC)

                isaltered = True
                changed.append("{0} [{1}]".format(save.appName, fileTime.strftime("%Y-%m-%d %H:%M.%S")))
                remove_folder(os.path.join('saves', save.appName))

                if os.path.isfile(path):
                    newdir = os.path.join('saves', save.appName)
                    if not os.path.exists(newdir): os.makedirs(newdir)
                    shutil.copy2(path, os.path.join('saves', save.appName))
                    pass
                else:
                    if output: print "{0}Compressing file...{1}".format(bcolors.WARNING, bcolors.ENDC)
                    shutil.make_archive(os.path.join('saves', save.appName), 'zip', path)  # zip file
                    fileSize = os.path.getsize(os.path.join('saves', '{0}.zip'.format(save.appName)))  # check file size of zip
                    if (fileSize > 100000000): # files above 100MB are too big for github, so just use the folder instead
                        if output: print "Zip is too big, using folder directory instead"
                        shutil.copytree(path, os.path.join('saves', save.appName), True)
                        os.remove(os.path.join('saves', '{0}.zip'.format(save.appName)))

                newinfo = [str(fileTime) + "\n", pathHash]
                with open(fileInfoPath, 'w') as f:
                    f.writelines(newinfo)

                if output: print "{0}Backing up path | {1}{2}".format(bcolors.WARNING, path, bcolors.ENDC)
                remove_folder(backupPath)
                
                if os.path.isfile(path):
                    os.makedirs(backupPath)
                    shutil.copy2(path, backupPath)
                    with open('{0}.txt'.format(backupPath), 'w') as f:
                        f.writelines(newinfo)
                else:
                    shutil.copytree(path, backupPath, True)
                    with open('{0}.txt'.format(backupPath), 'w') as f:
                        f.writelines(newinfo)
            else:
                if output: print "{0}Files are the same... not copying files{1}".format(bcolors.WARNING, bcolors.ENDC)
            if output: print "{0}---------------------------------------------------------------------------{1}".format(bcolors.LINE, bcolors.ENDC)

    return isaltered, changed