$jobdir = $PWD
$gfile = (Get-Item ($args[0]+".inp")).Basename
$gdir = (Split-Path $args[0] -Parent)
$uuid = New-Guid
$tmp = [System.IO.Path]::GetTempPath()
$scrdir = $tmp+$gfile+"_"+$uuid
mkdir $scrdir
cp ($args[0]+".inp") $scrdir
Set-Location $scrdir
orca.exe ($gfile+".inp") > ${jobdir}/${gdir}/$gfile.out
cd $jobdir
