# savedatasync
Sync various save data across emulators because my hard drive died in 2023 and I should back up important files.

The compression libary zpaq is now used for files over 100MB.

![2023-10-01_07-07-11_582_Vita3K](https://github.com/zydezu/savedatasync/assets/50119098/008ae336-b24b-4d6c-bf30-329a38cb1932)

> [!IMPORTANT]
> Use `sync.py`

This process uses git (with github to host) to sync save files from (in my case) various emulators across multiple devices. This is done by writing app names and file paths to `locations.txt`, running `upload saves to git.py` to update your save data, and then running `download saves from git.py`. Dates and file hashes are checked to determine when to update locally stored save data. Backups are created as a precautionary measure to prevent data loss.

The format for `locations.txt` is as follows for Windows file systems:

```
vita3k P4G
C:\Users\User\AppData\Roaming\Vita3K\Vita3K\ux0\user\00\savedata\PCSB00245

Minecraft Test
C:\Apps\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
C:\Games\MultiMC\instances\1.20.2 Optimised Mods\.minecraft\saves
```


For Linux file systems:

```
Persona 4 Golden
/home/user/.var/app/com.valvesoftware.Steam/.steam/steam/steamapps/userdata/123456/1113000/remote/

Minecraft
/home/user/Apps/MultiMC/instances/1.20.2 Optimised Mods/.minecraft/saves
```

Multiple lines can be used for file paths, as each one will be checked through.

>
# Issues

- This isn't automatic
- You could delete all your saves in the game, and then update the repo, and cry (That is why I made a backup solution).

![shinigsmile](https://github.com/zydezu/savedatasync/assets/50119098/2d9e21ea-6b68-485c-8cde-18c9efd360ad)
