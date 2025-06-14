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

>
# Issues

- This isn't automatic
- You could delete all your saves in the game, and then update the repo, and cry (That's why I made a backup solution)

![shinigsmile](https://github.com/zydezu/savedatasync/assets/50119098/2d9e21ea-6b68-485c-8cde-18c9efd360ad)
