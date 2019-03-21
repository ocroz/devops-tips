# Boost your Windows 10 machine

https://www.partitionwizard.com/partitionmagic/100-disk-usage-windows-10.html

For disk problems:
```bash
# powershell
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
CHKDSK C: /F /R
```
+Force a manual defragmentation of the disks

Programs launched at startup:<br/>
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Cheaper licenses:<br/>
https://www.hrkgame.com/fr/games/products/?search=office
