# Share a folder between Windows 10 host and CentOS 7 guest

## Windows part

Steps:
- Create a folder eg C:\Shared\common
- Right click on this folder, open tab `Sharing`, Share...
- Keep only you to share only with yourself
- Share and Apply

## CentOS 7 part

```bash
sudo yum install cifs-utils -y

user=windowsusername ; ip=windowsip;
folder=windowssharedfoldername # common
uid=$(id | sed 's,.*uid=,,' | sed 's,[^0-9].*,,')
gid=$(id | sed 's,.*gid=,,' | sed 's,[^0-9].*,,')

sudo mkdir /mnt/$folder
sudo mount.cifs -o username=$user,uid=$uid,gid=$gid //$ip/$folder /mnt/$folder
# You are prompted to enter password for $user@//$ip/$folder:

ln -s /mnt/$folder $HOME/$folder
```

## Sharing files

From Windows 10: Create C:\Shared\common\host.txt

From Linux:
- See the file $HOME/$folder/host.txt
- Create new file $HOME/$folder/guest.txt

From Windows 10: See the file C:\Shared\common\guest.txt
