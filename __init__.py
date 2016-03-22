import sys

if sys.platform == 'win32':
    from . win_printer import WinPrinter as Printer
else:
    raise Exception('Not implemented for current Operatin System.')
