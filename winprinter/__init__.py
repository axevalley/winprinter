import sys

if sys.platform == 'win32':
    from . winprinter import WinPrinter as Printer
else:
    raise Exception('Not implemented for current Operatin System.')
