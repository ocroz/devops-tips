# Query LDAP

## Linux

```bash
sudo apt install ldap-utils
echo "TLS_REQCERT never" ~/.ldaprc

dn="CN=Olivier Crozier,OU=Cheseaux,OU=Users,OU=Enterprise,DC=hq,DC=k,DC=grp"
. getpw

ldapwhoami -H ldaps://hq.k.grp -D "$dn" -w "$pw" -x -v
ldapsearch -H ldaps://hq.k.grp -D "$dn" -w "$pw" -x -v -b "DC=hq,DC=k,DC=grp" sAMAccountName=crozier dn
```

## Windows

If `net user|group /domain ...` is not working, use this PowerShell module:

```powershell
Import-Module ActiveDirectory
Get-Module -All
Get-Command -Module ActiveDirectory

Get-ADUser -Server hq.k.grp:389 crozier

$Profile
Test-Path $Profile # Then if False: New-Item -Type file -Path $Profile -Force
notepad $Profile   # $PSDefaultParameterValues = @{"*-AD*:Server"='hq.k.grp:389'}

Get-ADUser crozier
Get-ADUser crozier -Properties *
Get-ADUser crozier -Properties PasswordExpired,LockedOut | select Name,SamAccountName,UserPrincipalName,PasswordExpired,LockedOut | Format-List
Get-ADUser crozier -Properties PasswordExpired,LockedOut | Format-List -Property Name,SamAccountName,UserPrincipalName,PasswordExpired,LockedOut

Get-ADUser -Filter 'SamAccountName -eq "crozier"' | select * # select -expandproperty PropertyNames
(Get-ADUser crozier -Properties mail).mail

Get-ADGroup svc-gitlab-corp-admins
Get-ADGroup -Filter 'SamAccountName -eq "svc-gitlab-corp-admins"' # -like "svc-gitlab-corp-*"

Get-ADGroupMember svc-gitlab-corp-admins
Get-ADGroupMember -Identity 'svc-gitlab-corp-admins' | Format-Table -Property distinguishedName,name,SamAccountName
(Get-ADGroupMember svc-gitlab-corp-admins).SamAccountName
```
