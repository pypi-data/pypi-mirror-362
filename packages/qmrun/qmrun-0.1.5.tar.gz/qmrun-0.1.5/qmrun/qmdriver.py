import platform

import os
from qmrun import qmparser
from qmrun import qmwriter
import sys
import subprocess


def help():
    print("Usage: qmrun file.sdf pre.txt post.txt")
    print("file.sdf:"," ","a V2000 SDF file containing initial geometries")
    print("pre.txt:"," ","a text file containing Orca keywords before *xyz block")
    print("A typical pre.txt file may look like:")
    print("!PAL8")
    print("B3LYP def2-SVP NMR")
    print("post.txt (optional):"," ","a text file containing Orca keywords after *xyz block")
    print("A typical post.txt file may look like:")
    print("%eprnmr\n","Nuclei = all\n","{ssfc}\n","SpinSpinRThresh\n","500.0\n","end")


def Run():
    filename = sys.argv[1]
    if len(sys.argv) < 3:
        help()
        exit(1)

    rootname=filename[0:filename.rfind(".")]
    if not os.path.exists(rootname):
      os.mkdir(rootname)
    conformers = qmparser.ParseFile(filename, format="sdf")
    print(len(conformers)," structures read from file")
    filestorun=[]
    postf=None
    minidx=None
    maxidx=None
    if len(sys.argv) > 3:
        postf=sys.argv[3]
    if len(sys.argv) > 4:
        minidx=int(sys.argv[4])
    if len(sys.argv) > 5:
        maxidx=int(sys.argv[5])
    if minidx == None:
        minidx=0
    if maxidx == None:
       maxidx=len(conformers)
    print("nconf=",len(conformers))
    for idx, mol in enumerate(conformers):
        if (idx+1) < minidx or (idx+1) > maxidx:
            continue
        fname = rootname + "_"+str(idx + 1)+".inp"
        fname=rootname+"/"+fname
        filestorun.append(fname[0:fname.rfind(".")])
        print(fname)
        wr = qmwriter.Writer(mol, fname, pre=sys.argv[2], post=postf)
        wr.Write()
    #and now run
    for f in filestorun:
        print("f=",f)
        arguments=[]
        print("arguments=",arguments)
        print(platform.system())
        if platform.system() != "Windows":
            arguments.append("qmrun-orca6")
        else:
            arguments.append("powershell")
            arguments.append("qmrun-orca6.ps1")
        arguments.append(f)
        print(arguments)
        subprocess.call(arguments)


if __name__ == "__main__":
    Run()
