# -*- coding: utf-8 -*-

from rdkit import Chem

__author__="Armando Navarro Vázquez"
__copyright__="Copyright 2025, Armando Navarro-Vázquez"
__license__="MIT"
__version__="0.1"
__maintainer__="Armando Navarro-Vázquez"
__email_="armando.navarro@ufpe.br"
__status_="Development"

def ParseFile(file,format="sdf"):
  supplier = Chem.SDMolSupplier(file,strictParsing=False,sanitize=False)
  conformers = [m for m in supplier if m is not None]
  return conformers
