# savedatasync
Sync various save data across emulators because hard drive died in 2023 and I should back up stuff.

![2023-10-01_07-07-11_582_Vita3K](https://github.com/zydezu/savedatasync/assets/50119098/008ae336-b24b-4d6c-bf30-329a38cb1932)



> [!IMPORTANT]
> Use `sync.py` instead<br>~~Running `upload saves to git.py` should always been done right after finishing playing a game/changing files, and downloading should be done before opening the game `download saves from git.py` (though theoretically downloading can be done any time after uploading)~~

This process uses git (with github to host) to sync save files from (in my case) various emulators across multiple devices. This is done by writing app names and file paths to `locations.txt`, running `upload saves to git.py` to update your save data, and then running `download saves from git.py`. Dates and file hashes are checked to determine when to update locally stored save data. Backups are created as a precautionary measure to prevent data loss.

The format for `locations.txt` is as follows:

```
vita3k P4G
C:\Users\User\AppData\Roaming\Vita3K\Vita3K\ux0\user\00\savedata\PCSB00245

minecraft test
C:\Apps\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
C:\Games\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
```
Multiple lines can be used for file paths, as each one will be checked through.

> [!CAUTION]
> If using multiple paths, the non-valid folder shouldn't exist - otherwise issues may occur.

The `gitFilePath.txt` contains a reference to the master branch, with the main.zip file, this is used for the [download](https://github.com/zydezu/savedatasync?tab=readme-ov-file#downloading) process, so be sure to change if forking!

## Uploading

Play a game as normal, when you're done, run `upload saves to git.py`, you may see an output like this:
```powershell
===========================================================================
Checking each applications save data for changes
===========================================================================
Checking application: vita3k P4G | paths: ['C:\\Users\\User\\AppData\\Roaming\\Vita3K\\Vita3K\\ux0\\user\\00\\savedata\\PCSB00245']
Save data hash | 433714991f5ad0c8da927b9213da409902ecb578d690986a6bbcb3fdfea1f4b2
Info file hash | 433714991f5ad0c8da927b9213da409902ecb578d690986a6bbcb3fdfea1f4b2
Files are the same... not copying files
---------------------------------------------------------------------------
Checking application: minecraft test | paths: ['C:\\Apps\\MultiMC\\instances\\1.20.2 Optimised Mods\\.minecraft\\saves']
Save data hash | 061ccbe1d9dacd66b872ac9ec344b39104bfbb59e19ffcf09bc1ded467199ffc
Info file hash | 33e41b42effe1ef26365438d70f88b1d9cab072f3ed7d4aff54e0fc63e0c2154
Copying path | C:\Apps\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
Compressing file...
Backing up path | C:\Apps\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
---------------------------------------------------------------------------
minecraft test has been updated
===========================================================================
Checking git repo status...
...
```
In this output, `vita3k P4G`'s save hasn't changed since last time, so it's skipped over, wheras `minecraft test`'s save data has been updated, and the more recent version needs to be uploaded.

Hashes of the files are generated - checking if the files have been changed (there's newer save data than what is currently stored on git).

![2023-12-09_15-51-28_934_explorer](https://github.com/zydezu/savedatasync/assets/50119098/77c9feb9-5c1a-41e7-8230-9b0f179c3c2a)
<br/>*The `backup\` folder*

> [!NOTE]
> The `backup\` folder isn't uploaded to github, only saved locally.

If those hashes are different, firstly, the initial save files are copied to a backup folder, named: `backup\[date+time] [app name]` (eg: `backup\2023-11-30_01-21-32 vita3k P4G`), along with a text file of same name with date, time and hash information about the file (eg: stored at `backup\2023-11-30_01-21-32 vita3k P4G.txt`). Contents may look like this:
```
2023-11-30 01:21:32.999073
433714991f5ad0c8da927b9213da409902ecb578d690986a6bbcb3fdfea1f4b2
```

![2023-12-09_15-52-10_002_explorer](https://github.com/zydezu/savedatasync/assets/50119098/68038036-9848-48c1-bd3c-a2c667bddb5b)
<br/>*The `saves\` folder*

Next, the files are zipped and copied to `saves\[appname]` (eg: `save\vita3k P4G`) and the text file with save information (eg: `vita3k P4G.txt`), where `git push` is then ran, and the files are upload your github repository.

## Downloading

On other devices, run `download saves from git.py`. You may see an output like this:

```powershell
===========================================================================
Downloading files...
200GB
Cleaning up...
Done!
===========================================================================
Checking whether to update local save data
===========================================================================
Checking save data | minecraft test
Downloaded file hash | 2023-12-09 16:08:59.543161
Downloaded file hash | 33e41b42effe1ef26365438d70f88b1d9cab072f3ed7d4aff54e0fc63e0c2154
Current file date | 2023-12-09 15:38:13.039474
Current file hash | 061ccbe1d9dacd66b872ac9ec344b39104bfbb59e19ffcf09bc1ded467199ffc
Downloaded files are newer... overriding files
---------------------------------------------------------------------------
Checking save data | vita3k P4G
Downloaded file hash | 2023-12-09 16:08:59.382805
Downloaded file hash | 433714991f5ad0c8da927b9213da409902ecb578d690986a6bbcb3fdfea1f4b2
Current file date | 2023-11-30 01:21:32.993585
Current file hash | 433714991f5ad0c8da927b9213da409902ecb578d690986a6bbcb3fdfea1f4b2
Files are the same... not overriding files
---------------------------------------------------------------------------
minecraft test now has the newest save data
===========================================================================
```
In this output, the git repo is downloaded, unzipped, and checked, where it's shown that `minecraft test` has newer save data available, these saves are then copied into `save\` and to the file path specified in `locations.txt`. The current device now has the newest save data.

> [!NOTE]
> The speed of this somewhat depends on your internet connected.

All the save data from the git repository are downloaded and saved in `temp\`, saves are iterated through, where here hash files and dates are checked. If a save is newer, it is copied to `save\` and then the file path specified in `locations.txt`. The device now has the newest save data.

# Issues

- This isn't automatic
- You could delete all your saves in the game, and then update the repo, and cry (That's why I made a backup solution)

![shinigsmile](https://github.com/zydezu/savedatasync/assets/50119098/2d9e21ea-6b68-485c-8cde-18c9efd360ad)
