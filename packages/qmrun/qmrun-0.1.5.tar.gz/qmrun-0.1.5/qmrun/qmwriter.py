from rdkit import Chem
import platform

class Writer:
    def __init__(self, mol, filename, pre=None, post=None):
        self.mol = mol
        self.filename = filename
        self.molfile = None
        self.prefile = None
        self.postfile = None
        if pre:
            self.prefile = open(pre, "r")
        if post:
            self.postfile = open(post, "r")

    def Write(self):
        self.molfile=open(self.filename, "w")
        if self.prefile:
            lines = self.prefile.readlines()
            self.molfile.writelines(lines)
            if platform.system() == "Windows":
                self.molfile.write("\n")
        #write blannk
        self.molfile.write("*xyz 0 1\n")
        self.WriteMol()
        if self.postfile:
            lines = self.postfile.readlines()
            self.molfile.writelines(lines)
            self.molfile.write("\n")

        self.molfile.close()

    def WriteMol(self):
        conf = self.mol.GetConformer()
        for at in self.mol.GetAtoms():
            idx = at.GetIdx()
            xyz = conf.GetAtomPosition(idx)
            line = "{:<4}{:>12.6f}{:>12.6f}{:>12.6f}\n".format(str(at.GetSymbol()), xyz.x, xyz.y, xyz.z)
            self.molfile.write(line)
        self.molfile.write("*")
        self.molfile.write("\n")
