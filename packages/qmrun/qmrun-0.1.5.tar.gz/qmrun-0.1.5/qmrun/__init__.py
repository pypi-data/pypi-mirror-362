"""
qmrun.

A Orca6 Input File Generator from SDF files.
"""

from qmrun import qmdriver

__version__ = "0.1.5"
__author__ = 'Armando Navarro-Vázquez'
__credits__ = 'Armando Navarro-Vázquez. Universidade Federal de Pernambuco'

def run():
    qmdriver.Run()