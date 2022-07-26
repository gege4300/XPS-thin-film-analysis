#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.4
#  in conjunction with Tcl version 8.6
#    Jul 07, 2022 02:38:10 PM CEST  platform: Linux

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import xpsquanti

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    root.attributes('-type', 'dialog') 
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = xpsquanti.Toplevel1(_top1)
    root.mainloop()

def calculate(*args):
    print('xpsquanti_support.calculate')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

if __name__ == '__main__':
    xpsquanti.start_up()



