import subprocess
from readFileLocations import *

def upload(overrideAltered=False, overrideChangedMessage=False, output=True):
    if output: print("===========================================================================")
    if output: print("Checking each application's save data for changes")
    if output: print("===========================================================================")
    
    saveLocations = readLocationsFile()
    isaltered, changed = saveData(saveLocations, output)
    if overrideAltered:
        isaltered = overrideAltered
    if overrideChangedMessage:
        changed = overrideChangedMessage

    changedString = "update repo"
    if isaltered:
        if len(changed) > 1:
            changedString = f"{', '.join(changed[:-1])}, and {changed[-1]}"
            print(changedString,"have been updated")
        else:
            changedString = changed[0]
            print(changedString,"has been updated")
        changedString = f"updated savefiles: {changedString}"
    else:
        print("No save data has changed!")

    print("===========================================================================")
    print("Checking git repo status...")
    print("===========================================================================")

    subprocess.call(["git", "pull", "--allow-unrelated-histories"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", changedString])
    subprocess.call(["git", "push"])

    print("===========================================================================")

if __name__ == "__main__":
    # Provide appropriate values for overrideAltered and overrideChangedMessage
    overrideAltered = False  # Provide the appropriate value
    overrideChangedMessage = False  # Provide the appropriate value
    upload(overrideAltered, overrideChangedMessage)
    print("Press ENTER to close")
    input()
