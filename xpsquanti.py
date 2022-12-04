#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
#    Jul 07, 2022 02:38:01 PM CEST  platform: Linux
#####  SF method T(E) function is still not included or T(E) is wrong, one need to consider their own sensitivity factors
##  all the calculations are assumed that electrons are collected with the spectrometer perpendicular to the sample

import sys
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter.constants import *
from numpy import loadtxt, interp, arange, sin, pi, max, random
from PIL import ImageTk, Image
from sympy import symbols, nsolve, exp

#import matplotlib.pyplot as plt
#from matplotlib import style
#import matplotlib.lines as lines
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
#from lmfit.models import GaussianModel, LorentzianModel, VoigtModel, PseudoVoigtModel, ThermalDistributionModel, PolynomialModel, StepModel
#from lmfit.models import ExponentialGaussianModel, SkewedGaussianModel, SkewedVoigtModel, DoniachModel, BreitWignerModel, LognormalModel
#from lmfit import Model

#style.use('ggplot')

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        #tk.Frame.configure(self, background="black")
    def show(self):
        self.lift()

# peak fitting panel
class Page0(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)

        



        self.TCombobox_imp = ttk.Combobox(self)
        self.TCombobox_imp.place(x=10, y=30, height=27, width=170)
        #self.TCombobox_imp.configure(textvariable=self.combobox)
        self.TCombobox_imp.configure(takefocus="")
        self.TCombobox_imp['values']=("Open data","Open txt")
        self.TCombobox_imp.current(0)
        self.TCombobox_imp.bind("<<ComboboxSelected>>",self.plot)

        self.Daplot = tk.Button(self)
        self.Daplot.place(x=190, y=30, height=30, width=71)
        self.Daplot.configure(activebackground="beige")
        self.Daplot.configure(background="#3498DB")
        self.Daplot.configure(borderwidth="2")
        #self.Daplot.configure(command=self.plot)
        self.Daplot.configure(compound='left')
        self.Daplot.configure(foreground="#ffffff")
        self.Daplot.configure(text='''plot''')

        self.Label1 = tk.Label(self)
        self.Label1.place(x=10, y=60)
        #self.Label1.configure(activebackground="#f9f9f9")
        #self.Label1.configure(anchor='w')
        #self.Label1.configure(background="#262626")
        self.Label1.configure(compound='left')
        #self.Label1.configure(foreground="#ffffff")

        self.Framefig=tk.Frame(self)
        self.Framefig.place(x=13, y=80, height=200, width=200)
        self.Framefig.configure(relief='groove')
        self.Framefig.configure(borderwidth="2")
        self.Framefig.configure(relief="groove")

        
        
    # initial file path for opening the file 
    def filePath(self):

        return os.path.dirname(os.path.realpath(__file__))

    def imp(self,path):
        if self.TCombobox_imp.get() == "Open txt":
            filename = filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
            X, Y = [], []
            for line in open(filename):
                values = [float(s) for s in line.split()]
                X.append(values[0])
                Y.append(values[1])
                XY=[X,Y]
        else:
            XY="choose Open txt"

        return XY
    
    def plot(self,_):
        xx=self.imp(self.filePath)
        print (xx)


## atomic ratio caculation panel
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.Label1 = tk.Label(self)
        self.Label1.place(x=20, y=60, height=30, width=80)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#262626")
        self.Label1.configure(compound='left')
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''1. Ephoton''')

        self.Label1_1 = tk.Label(self)
        self.Label1_1.place(x=20, y=140, height=30, width=132)
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(anchor='w')
        self.Label1_1.configure(background="#262626")
        self.Label1_1.configure(compound='left')
        self.Label1_1.configure(foreground="#ffffff")
        self.Label1_1.configure(text='''2. angle(beam-spec)''')

        self.Label1_1_1 = tk.Label(self)
        self.Label1_1_1.place(x=200, y=60, height=30, width=189)
        self.Label1_1_1.configure(activebackground="#f9f9f9")
        self.Label1_1_1.configure(anchor='w')
        self.Label1_1_1.configure(background="#262626")
        self.Label1_1_1.configure(compound='center')
        self.Label1_1_1.configure(foreground="#ffffff")
        self.Label1_1_1.configure(text='''        3.       element    &    area''')

        self.Labelele1 = tk.Label(self)
        self.Labelele1.place(x=200, y=98, height=30, width=44)
        self.Labelele1.configure(activebackground="#f9f9f9")
        self.Labelele1.configure(anchor='w')
        self.Labelele1.configure(background="#262626")
        self.Labelele1.configure(compound='left')
        self.Labelele1.configure(foreground="#ffffff")
        self.Labelele1.configure(text='''ele1''')

        self.Labelele2 = tk.Label(self)
        self.Labelele2.place(x=200, y=135, height=30, width=44)
        self.Labelele2.configure(activebackground="#f9f9f9")
        self.Labelele2.configure(anchor='w')
        self.Labelele2.configure(background="#262626")
        self.Labelele2.configure(compound='left')
        self.Labelele2.configure(foreground="#ffffff")
        self.Labelele2.configure(text='''ele2''')

        self.Entryphoton = tk.Entry(self)
        self.Entryphoton.place(x=20, y=95, height=23, width=70)

        self.Entryphoton.configure(background="#f2f2f2")
        self.Entryphoton.configure(font="TkFixedFont")
        self.Entryphoton.configure(foreground="#aa80bf")
        self.Entryphoton.configure(selectbackground="#c4c4c4")
        self.Entryphoton.insert(-1, 1486.6)

        self.Button1 = tk.Button(self)
        self.Button1.place(x=460, y=60, height=30, width=71)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(background="#3498DB")
        self.Button1.configure(borderwidth="2")
        self.Button1.configure(command=self.clicked)
        self.Button1.configure(compound='left')
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(text='''calculate''')

        self.Button3 = tk.Button(self)
        self.Button3.place(x=460, y=280, height=30, width=140)
        self.Button3.configure(activebackground="beige")
        self.Button3.configure(background="#3498DB")
        self.Button3.configure(borderwidth="2")
        self.Button3.configure(command=self.sfclicked)
        self.Button3.configure(compound='left')
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(text='''calculate (SF method)''')


        self.Labelresu2 = tk.Label(self)
        self.Labelresu2.place(x=445, y=320)
        #self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu2.configure(anchor='w')
        self.Labelresu2.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu2.configure(compound='left')
        self.Labelresu2.configure(foreground="#000000")

        #self.Labelele3 = tk.Label(self.top)
        #self.Labelele3.place(relx=0.623, rely=0.167, height=30, width=84)
        #self.Labelele3.configure(activebackground="#f9f9f9")
        #self.Labelele3.configure(anchor='w')
        #self.Labelele3.configure(background="#262626")
        ##self.Labelele3.configure(compound='left')
        #self.Labelele3.configure(foreground="#ffffff")
        #self.Labelele3.configure(text='''the result is:''')

        self.Labelresu = tk.Label(self)
        self.Labelresu.place(x=445, y=100)
        self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu.configure(anchor='w')
        self.Labelresu.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu.configure(compound='left')
        self.Labelresu.configure(foreground="#000000")

        self.Labelele4 = tk.Label(self)
        self.Labelele4.place(x=20, y=225, height=30, width=159)
        self.Labelele4.configure(activebackground="#f9f9f9")
        self.Labelele4.configure(anchor='w')
        self.Labelele4.configure(background="#262626")
        self.Labelele4.configure(compound='left')
        self.Labelele4.configure(foreground="#ffffff")
        self.Labelele4.configure(text='''IMFP calculation (TPP-2M)''')

        self.Labelele5 = tk.Label(self)
        self.Labelele5.place(x=20, y=265, height=25, width=40)
        self.Labelele5.configure(activebackground="#f9f9f9")
        self.Labelele5.configure(anchor='w')
        self.Labelele5.configure(background="#262626")
        self.Labelele5.configure(compound='left')
        self.Labelele5.configure(foreground="#ffffff")
        self.Labelele5.configure(text='''Zavg''')

        self.Labelele6 = tk.Label(self)
        self.Labelele6.place(x=20, y=300, height=25, width=40)
        self.Labelele6.configure(activebackground="#f9f9f9")
        self.Labelele6.configure(anchor='w')
        self.Labelele6.configure(background="#262626")
        self.Labelele6.configure(compound='left')
        self.Labelele6.configure(foreground="#ffffff")
        self.Labelele6.configure(text='''egap''')

        self.Labelele7 = tk.Label(self)
        self.Labelele7.place(x=20, y=335, height=25, width=40)
        self.Labelele7.configure(activebackground="#f9f9f9")
        self.Labelele7.configure(anchor='w')
        self.Labelele7.configure(background="#262626")
        self.Labelele7.configure(compound='left')
        self.Labelele7.configure(foreground="#ffffff")
        self.Labelele7.configure(text='''a(nm)''')

        self.Labelele8 = tk.Label(self)
        self.Labelele8.place(x=20, y=370, height=25, width=40)
        self.Labelele8.configure(activebackground="#f9f9f9")
        self.Labelele8.configure(anchor='w')
        self.Labelele8.configure(background="#262626")
        self.Labelele8.configure(compound='left')
        self.Labelele8.configure(foreground="#ffffff")
        self.Labelele8.configure(text='''BE1''')

        self.Labelele9 = tk.Label(self)
        self.Labelele9.place(x=20, y=405, height=25, width=40)
        self.Labelele9.configure(activebackground="#f9f9f9")
        self.Labelele9.configure(anchor='w')
        self.Labelele9.configure(background="#262626")
        self.Labelele9.configure(compound='left')
        self.Labelele9.configure(foreground="#ffffff")
        self.Labelele9.configure(text='''BE2''')

        self.Labelele10 = tk.Label(self)
        self.Labelele10.place(x=20, y=435, height=25, width=120)
        self.Labelele10.configure(activebackground="#f9f9f9")
        self.Labelele10.configure(anchor='w')
        self.Labelele10.configure(background="#262626")
        self.Labelele10.configure(compound='left')
        self.Labelele10.configure(foreground="#ffffff")
        self.Labelele10.configure(text='''film thickness(nm)''')

        self.Showquation = tk.Label(self)
        self.Showquation.place(x=20, y=475, height=25, width=100)
        self.Showquation.configure(activebackground="#f9f9f9")
        self.Showquation.configure(anchor='w')
        self.Showquation.configure(background="#262626")
        self.Showquation.configure(compound='left')
        self.Showquation.configure(foreground="#ffffff")
        self.Showquation.configure(text='''show equation:''')

        self.Equationpic = tk.Label(self)
        self.Equationpic.place(x=20, y=505, height=25, width=200)
        #self.Equationpic.configure(activebackground="#f9f9f9")
        self.Equationpic.configure(anchor='w')
        #self.Equationpic.configure(background="#262626")
        self.Equationpic.configure(compound='left')
        #self.Equationpic.configure(foreground="#ffffff")
        self.Equationpic.configure(text='''will add if necessary''')

        self.zavg = tk.Entry(self)
        self.zavg.place(x=70, y=265, height=23, width=70)
        self.zavg.configure(background="#f2f2f2")
        self.zavg.configure(font="TkFixedFont")
        self.zavg.configure(foreground="#aa80bf")
        self.zavg.configure(selectbackground="#c4c4c4")
        self.zavg.insert(-1, 4)

        self.egap = tk.Entry(self)
        self.egap.place(x=70, y=300, height=23, width=70)
        self.egap.configure(background="#f2f2f2")
        self.egap.configure(font="TkFixedFont")
        self.egap.configure(foreground="#aa80bf")
        self.egap.configure(selectbackground="#c4c4c4")
        self.egap.insert(-1, 3)

        self.anm = tk.Entry(self)
        self.anm.place(x=70, y=335, height=23, width=70)
        self.anm.configure(background="#f2f2f2")
        self.anm.configure(font="TkFixedFont")
        self.anm.configure(foreground="#aa80bf")
        self.anm.configure(selectbackground="#c4c4c4")
        self.anm.insert(-1, 0.25)

        self.be1 = tk.Entry(self)
        self.be1.place(x=70, y=370, height=23, width=70)
        self.be1.configure(background="#f2f2f2")
        self.be1.configure(font="TkFixedFont")
        self.be1.configure(foreground="#aa80bf")
        self.be1.configure(selectbackground="#c4c4c4")
        self.be1.insert(-1, 285)

        self.be2 = tk.Entry(self)
        self.be2.place(x=70, y=405, height=23, width=70)
        self.be2.configure(background="#f2f2f2")
        self.be2.configure(font="TkFixedFont")
        self.be2.configure(foreground="#aa80bf")
        self.be2.configure(selectbackground="#c4c4c4")
        self.be2.insert(-1, 395)

        self.fthick = tk.Entry(self)
        self.fthick.place(x=150, y=435, height=23, width=70)
        self.fthick.configure(background="#f2f2f2")
        self.fthick.configure(font="TkFixedFont")
        self.fthick.configure(foreground="#aa80bf")
        self.fthick.configure(selectbackground="#c4c4c4")
        self.fthick.insert(-1, 10)


        self.Entryangle = tk.Entry(self)
        self.Entryangle.place(x=20, y=175, height=23, width=70)
        self.Entryangle.configure(background="#f2f2f2")
        self.Entryangle.configure(font="TkFixedFont")
        self.Entryangle.configure(foreground="#aa80bf")
        self.Entryangle.configure(selectbackground="#c4c4c4")
        self.Entryangle.insert(-1, 54.7)

        self.Entryele1 = tk.Entry(self)
        self.Entryele1.place(x=250, y=100, height=23, width=60)
        self.Entryele1.configure(background="#f2f2f2")
        self.Entryele1.configure(font="TkFixedFont")
        self.Entryele1.configure(foreground="#aa80bf")
        self.Entryele1.configure(selectbackground="#c4c4c4")
        self.Entryele1.insert(-1, "c1s")

        self.TCombobox1 = ttk.Combobox(self)
        self.TCombobox1.place(x=210, y=243, height=27, width=170)
        #self.TCombobox1.configure(textvariable=self.combobox)
        self.TCombobox1.configure(takefocus="")
        self.TCombobox1['values']=("bulk","layer1","layer2","layer3")
        #self.TCombobox1.current(0)
        self.TCombobox1.bind("<<ComboboxSelected>>",self.getim)

        self.Entryele2 = tk.Entry(self)
        self.Entryele2.place(x=250, y=135, height=23, width=60)
        self.Entryele2.configure(background="#f2f2f2")
        self.Entryele2.configure(font="TkFixedFont")
        self.Entryele2.configure(foreground="#aa80bf")
        self.Entryele2.configure(selectbackground="#c4c4c4")
        self.Entryele2.insert(-1, "c1s")

        self.Entryarea1 = tk.Entry(self)
        self.Entryarea1.place(x=320, y=100, height=23, width=70)
        self.Entryarea1.configure(background="#f2f2f2")
        self.Entryarea1.configure(font="TkFixedFont")
        self.Entryarea1.configure(foreground="#aa80bf")
        self.Entryarea1.configure(selectbackground="#c4c4c4")

        self.Entryarea2 = tk.Entry(self)
        self.Entryarea2.place(x=320, y=135, height=23, width=70)
        self.Entryarea2.configure(background="#f2f2f2")
        self.Entryarea2.configure(font="TkFixedFont")
        self.Entryarea2.configure(foreground="#aa80bf")
        self.Entryarea2.configure(selectbackground="#c4c4c4")

        self.Label1_1_1_2 = tk.Label(self)
        self.Label1_1_1_2.place(x=200, y=200, height=30, width=189)
        self.Label1_1_1_2.configure(activebackground="#f9f9f9")
        self.Label1_1_1_2.configure(anchor='w')
        self.Label1_1_1_2.configure(background="#262626")
        self.Label1_1_1_2.configure(compound='center')
        self.Label1_1_1_2.configure(foreground="#ffffff")
        self.Label1_1_1_2.configure(text='''                   4. XPS model''')

    # here start the defining the functions, define a simplified IMFP equation
    def tpp(self, KE,z,eg,a):
        return (a**1.7)*(4 + 0.44 *z**0.5 + 0.104 *KE**0.872)/((z**0.38)*(1 - 0.02 *eg))

    #this is the get crosssection function
    def getcs(self,penergy):
        #path="/home/qiankun/python/xpsquanti/tkmethod/cs"
        #os.chdir(path)
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path1 = dir_path+'/cs'
        try:
            os.chdir(path1)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        ele1cs = loadtxt(self.Entryele1.get())
        ele2cs = loadtxt(self.Entryele2.get())
        ele1csx = ele1cs[:,0]
        ele1csy = ele1cs[:,1]
        ele1csv = interp(penergy,ele1csx,ele1csy)  #linear interpolation
        ele2csx = ele2cs[:,0]
        ele2csy = ele2cs[:,1]
        ele2csv = interp(penergy,ele2csx,ele2csy)  #linear interpolation
        ele12csv = [ele1csv,ele2csv]
        return ele12csv
    ### here get image
    def getim(self,model):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path2 = dir_path +'/images'
        try:
            os.chdir(path2)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        self.modelfig1=ImageTk.PhotoImage(Image.open("bulk").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig2=ImageTk.PhotoImage(Image.open("layer1").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig3=ImageTk.PhotoImage(Image.open("layer2").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig4=ImageTk.PhotoImage(Image.open("layer3").resize((150, 150), Image.Resampling.LANCZOS))
        if self.TCombobox1.get()== "bulk":
            self.model1=tk.Label(self, image=self.modelfig1).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer1":
            self.model1=tk.Label(self, image=self.modelfig2).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer2":
            self.model1=tk.Label(self, image=self.modelfig3).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer3":
            self.model1=tk.Label(self, image=self.modelfig4).place(x=220, y=280, height=150, width=150)
    
    '''
    def getform(self,formula):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path2 = dir_path +'/images'
        try:
            os.chdir(path2)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        self.modelfig1=ImageTk.PhotoImage(Image.open("bulk").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig2=ImageTk.PhotoImage(Image.open("layer1").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig3=ImageTk.PhotoImage(Image.open("layer2").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig4=ImageTk.PhotoImage(Image.open("layer3").resize((150, 150), Image.Resampling.LANCZOS))
        if self.TCombobox1.get()== "bulk":
            self.model1=tk.Label(self, image=self.modelfig1).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer1":
            self.model1=tk.Label(self, image=self.modelfig2).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer2":
            self.model1=tk.Label(self, image=self.modelfig3).place(x=220, y=280, height=150, width=150)
        elif self.TCombobox1.get()== "layer3":
            self.model1=tk.Label(self, image=self.modelfig4).place(x=220, y=280, height=150, width=150)
    '''
    # get snsitivity factors
    def getsf(self,element):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path3 = dir_path +'/sf'
        try:
            os.chdir(path3)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        sfx, sfy = [], []
        if float(self.Entryangle.get())==54.7:
            for line in open('sf54_7', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        else:
            for line in open('sf90', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        return valp

     #### here define calculate   
    def clicked(self):
        ratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        ccs = self.getcs(self.Entryphoton.get())
        ccsele1=ccs[0]
        ccsele2=ccs[1]
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        ratiobulk2=(ratiobulk1*float(ccsele2)*imfp2)/(float(ccsele1)*imfp1)
        tfilm=float(self.fthick.get())
        ratiolayer12=ratiobulk2*(1-exp(-tfilm/imfp2))/(1-exp(-tfilm/imfp1))
        ratiolayer21=ratiobulk1*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        ratiolayer22=ratiobulk2*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        ratiolayer32=ratiobulk2*exp(-tfilm/imfp2)/exp(-tfilm/imfp1)
        if self.TCombobox1.get()== "bulk":
            if self.Entryele1.get()==self.Entryele2.get():
                #tkinter.messagebox.showinfo('the answer is: ', 'CS and IMFP ignored\n' ,ccs)
                self.Labelresu.configure(text="Area=N*fph*cs*IMFP*\nTransmission(E)*Cos(thetA)*A\n"+"CS,IMFP,T(E) ignored, only area considered\n"+ "\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2= "+str(ratiobulk1))
            else:
                self.Labelresu.configure(text="Area=N*fph*cs*IMFP*\nTransmission(E)*Cos(thetA)*A\n"+"CS,IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*cs2*imfp2/(Area2*cs1*imfp1)= "+str(ratiobulk2))
        elif self.TCombobox1.get()== "layer1":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu.configure(text="Area=N*cs*IMFP*(1-exp(-t/IMFP))\n"+"CS,IMFP,T(E) ignored, only area considered\n"+ "\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2= "+str(ratiobulk1))
            else:
                self.Labelresu.configure(text="Area=N*cs*IMFP*(1-exp(-t/IMFP))\n"+"CS,IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*cs2*imfp2*(1-exp(-t/imf2))/(Area2*cs1*imfp1*(1-exp(-t/imfp1)))= \n"+str(ratiolayer12))
        elif self.TCombobox1.get()== "layer2":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu.configure(text="Area1(toplayer)=N1*cs*IMFP*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*cs*IMFP*exp(-t/IMFP2)\n"+"CS ignored, IMFP1=IMFP2\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*exp(-t/imfp2)/(Area2*(1-exp(-t/imfp1)))= \n"+str(ratiolayer21))
            else:
                self.Labelresu.configure(text="Area1(toplayer)=N1*cs*IMFP*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*cs*IMFP*exp(-t/IMFP2)\n"+"CS,IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*cs2*imfp2*exp(-t/imfp2)/(Area2*cs1*imfp1*(1-exp(-t/imfp1)))= \n"+str(ratiolayer22))
        elif self.TCombobox1.get()== "layer3":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu.configure(text="Area=N*cs*IMFP*exp(-t/IMFP)\n"+"CS, IMFP ignored\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2="+str(ratiobulk1))
            else:
                self.Labelresu.configure(text="Area1=N1*cs1*IMFP1*exp(-t/IMFP1)\n"+"Area2=N2*cs2*IMFP2*exp(-t/IMFP2)\n"+"CS, IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*cs2*imfp2*exp(-t/imfp2)/(Area2*cs1*imfp1*exp(-t/imfp1))= \n"+str(ratiolayer32))
        else:
            pass

    ### sensitiity factor calculate
    def sfclicked(self):
        sfratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        #ccs = self.getcs(self.Entryphoton.get())
        #ccsele1=ccs[0]
        #ccsele2=ccs[1]
        sfele1 = self.getsf(self.Entryele1.get())
        sfele2 = self.getsf(self.Entryele2.get())
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        sfratiobulk2=sfratiobulk1*float(sfele2)/float(sfele1)
        tfilm=float(self.fthick.get())
        sfratiolayer12=sfratiobulk2*(1-exp(-tfilm/imfp2))/(1-exp(-tfilm/imfp1))
        sfratiolayer21=sfratiobulk1*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        sfratiolayer22=sfratiobulk2*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        sfratiolayer32=sfratiobulk2*exp(-tfilm/imfp2)/exp(-tfilm/imfp1)
        if self.TCombobox1.get()== "bulk":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area=N*sf\n"+ "the same element, sf ignored\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2= "+str(sfratiobulk1))
            else:
                self.Labelresu2.configure(text="Area=N*sf\n"+"sf considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)  +"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*sfele2/(Area2*sfele1)= "+str(sfratiobulk2))
        elif self.TCombobox1.get()== "layer1":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area=N*sf*(1-exp(-t/IMFP))\n"+"sf,IMFP, ignored, only area considered\n"+ "\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2= "+str(sfratiobulk1))
            else:
                self.Labelresu2.configure(text="Area=N*sf*(1-exp(-t/IMFP))\n"+"sf,IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2) +"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*sf2*(1-exp(-t/imf2))/(Area2*sf1*(1-exp(-t/imfp1)))= \n"+str(sfratiolayer12))
        elif self.TCombobox1.get()== "layer2":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area1(toplayer)=N1*sf1*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*sf2*exp(-t/IMFP2)\n"+"sf,IMFP1=IMFP2\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2) +"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*exp(-t/imfp2)/(Area2*(1-exp(-t/imfp1)))= \n"+str(sfratiolayer21))
            else:
                self.Labelresu2.configure(text="Area1(toplayer)=N1*sf1*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*sf2*exp(-t/IMFP2)\n"+"sf,IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*sf2*exp(-t/imfp2)/(Area2*sf1*(1-exp(-t/imfp1)))= \n"+str(sfratiolayer22))
        elif self.TCombobox1.get()== "layer3":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area=N*sf*exp(-t/IMFP)\n"+"sf ignored\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1/Area2="+str(sfratiobulk1))
            else:
                self.Labelresu2.configure(text="Area1=N1*sf1*exp(-t/IMFP1)\n"+"Area2=N2*sf2*exp(-t/IMFP2)\n"+"sf, IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"film thickness= "+str(tfilm)+"\n"+"\n"+"element density ratio is:\n" +"N1/N2=Area1*sf2*exp(-t/imfp2)/(Area2*sf1*exp(-t/imfp1))= \n"+str(sfratiolayer32))
        else:
            pass

        #self.Labelresu.configure(text="the result is: "+str(ccs))

## thin film thickness calculation panel
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.epholabel = tk.Label(self)
        self.epholabel.place(x=20, y=60, height=30, width=80)
        self.epholabel.configure(activebackground="#f9f9f9")
        self.epholabel.configure(anchor='w')
        self.epholabel.configure(background="#262626")
        self.epholabel.configure(compound='left')
        self.epholabel.configure(foreground="#ffffff")
        self.epholabel.configure(text='''1. Ephoton''')

        self.anglabel = tk.Label(self)
        self.anglabel.place(x=20, y=140, height=30, width=132)
        self.anglabel.configure(activebackground="#f9f9f9")
        self.anglabel.configure(anchor='w')
        self.anglabel.configure(background="#262626")
        self.anglabel.configure(compound='left')
        self.anglabel.configure(foreground="#ffffff")
        self.anglabel.configure(text='''2. angle(beam-spec)''')

        self.elearealabel = tk.Label(self)
        self.elearealabel.place(x=200, y=60, height=30, width=189)
        self.elearealabel.configure(activebackground="#f9f9f9")
        self.elearealabel.configure(anchor='w')
        self.elearealabel.configure(background="#262626")
        self.elearealabel.configure(compound='center')
        self.elearealabel.configure(foreground="#ffffff")
        self.elearealabel.configure(text='''        3.       element    &    area''')

        self.ele1label = tk.Label(self)
        self.ele1label.place(x=200, y=98, height=30, width=44)
        self.ele1label.configure(activebackground="#f9f9f9")
        self.ele1label.configure(anchor='w')
        self.ele1label.configure(background="#262626")
        self.ele1label.configure(compound='left')
        self.ele1label.configure(foreground="#ffffff")
        self.ele1label.configure(text='''ele1''')

        self.ele2label = tk.Label(self)
        self.ele2label.place(x=200, y=135, height=30, width=44)
        self.ele2label.configure(activebackground="#f9f9f9")
        self.ele2label.configure(anchor='w')
        self.ele2label.configure(background="#262626")
        self.ele2label.configure(compound='left')
        self.ele2label.configure(foreground="#ffffff")
        self.ele2label.configure(text='''ele2''')

        self.ele1density = tk.Label(self)
        self.ele1density.place(x=200, y=170, height=30, width=84)
        self.ele1density.configure(activebackground="#f9f9f9")
        self.ele1density.configure(anchor='w')
        self.ele1density.configure(background="#262626")
        self.ele1density.configure(compound='left')
        self.ele1density.configure(foreground="#ffffff")
        self.ele1density.configure(text='''density(ele1)''')

        self.ele2density = tk.Label(self)
        self.ele2density.place(x=200, y=205, height=30, width=84)
        self.ele2density.configure(activebackground="#f9f9f9")
        self.ele2density.configure(anchor='w')
        self.ele2density.configure(background="#262626")
        self.ele2density.configure(compound='left')
        self.ele2density.configure(foreground="#ffffff")
        self.ele2density.configure(text='''density(ele2)''')

        self.Entryphoton = tk.Entry(self)
        self.Entryphoton.place(x=20, y=95, height=23, width=70)
        self.Entryphoton.configure(background="#f2f2f2")
        self.Entryphoton.configure(font="TkFixedFont")
        self.Entryphoton.configure(foreground="#aa80bf")
        self.Entryphoton.configure(selectbackground="#c4c4c4")
        self.Entryphoton.insert(-1, 1486.6)

        self.Button1 = tk.Button(self)
        self.Button1.place(x=460, y=60, height=30, width=71)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(background="#3498DB")
        self.Button1.configure(borderwidth="2")
        self.Button1.configure(command=self.clicked)
        self.Button1.configure(compound='left')
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(text='''calculate''')

        self.Button3 = tk.Button(self)
        self.Button3.place(x=460, y=280, height=30, width=140)
        self.Button3.configure(activebackground="beige")
        self.Button3.configure(background="#3498DB")
        self.Button3.configure(borderwidth="2")
        self.Button3.configure(command=self.sfclicked)
        self.Button3.configure(compound='left')
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(text='''calculate (SF method)''')


        self.Labelresu2 = tk.Label(self)
        self.Labelresu2.place(x=445, y=320)
        #self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu2.configure(anchor='w')
        self.Labelresu2.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu2.configure(compound='left')
        self.Labelresu2.configure(foreground="#000000")

        #self.Labelele3 = tk.Label(self.top)
        #self.Labelele3.place(relx=0.623, rely=0.167, height=30, width=84)
        #self.Labelele3.configure(activebackground="#f9f9f9")
        #self.Labelele3.configure(anchor='w')
        #self.Labelele3.configure(background="#262626")
        ##self.Labelele3.configure(compound='left')
        #self.Labelele3.configure(foreground="#ffffff")
        #self.Labelele3.configure(text='''the result is:''')

        self.Labelresu = tk.Label(self)
        self.Labelresu.place(x=445, y=100)
        #self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu.configure(anchor='w')
        self.Labelresu.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu.configure(compound='left')
        self.Labelresu.configure(foreground="#000000")

        self.Labelele4 = tk.Label(self)
        self.Labelele4.place(x=20, y=225, height=30, width=159)
        self.Labelele4.configure(activebackground="#f9f9f9")
        self.Labelele4.configure(anchor='w')
        self.Labelele4.configure(background="#262626")
        self.Labelele4.configure(compound='left')
        self.Labelele4.configure(foreground="#ffffff")
        self.Labelele4.configure(text='''IMFP calculation (TPP-2M)''')

        self.Labelele5 = tk.Label(self)
        self.Labelele5.place(x=20, y=265, height=25, width=40)
        self.Labelele5.configure(activebackground="#f9f9f9")
        self.Labelele5.configure(anchor='w')
        self.Labelele5.configure(background="#262626")
        self.Labelele5.configure(compound='left')
        self.Labelele5.configure(foreground="#ffffff")
        self.Labelele5.configure(text='''Zavg''')

        self.Labelele6 = tk.Label(self)
        self.Labelele6.place(x=20, y=300, height=25, width=40)
        self.Labelele6.configure(activebackground="#f9f9f9")
        self.Labelele6.configure(anchor='w')
        self.Labelele6.configure(background="#262626")
        self.Labelele6.configure(compound='left')
        self.Labelele6.configure(foreground="#ffffff")
        self.Labelele6.configure(text='''egap''')

        self.Labelele7 = tk.Label(self)
        self.Labelele7.place(x=20, y=335, height=25, width=40)
        self.Labelele7.configure(activebackground="#f9f9f9")
        self.Labelele7.configure(anchor='w')
        self.Labelele7.configure(background="#262626")
        self.Labelele7.configure(compound='left')
        self.Labelele7.configure(foreground="#ffffff")
        self.Labelele7.configure(text='''a(nm)''')

        self.Labelele8 = tk.Label(self)
        self.Labelele8.place(x=20, y=370, height=25, width=40)
        self.Labelele8.configure(activebackground="#f9f9f9")
        self.Labelele8.configure(anchor='w')
        self.Labelele8.configure(background="#262626")
        self.Labelele8.configure(compound='left')
        self.Labelele8.configure(foreground="#ffffff")
        self.Labelele8.configure(text='''BE1''')

        self.Labelele9 = tk.Label(self)
        self.Labelele9.place(x=20, y=405, height=25, width=40)
        self.Labelele9.configure(activebackground="#f9f9f9")
        self.Labelele9.configure(anchor='w')
        self.Labelele9.configure(background="#262626")
        self.Labelele9.configure(compound='left')
        self.Labelele9.configure(foreground="#ffffff")
        self.Labelele9.configure(text='''BE2''')

        self.zavg = tk.Entry(self)
        self.zavg.place(x=70, y=265, height=23, width=70)
        self.zavg.configure(background="#f2f2f2")
        self.zavg.configure(font="TkFixedFont")
        self.zavg.configure(foreground="#aa80bf")
        self.zavg.configure(selectbackground="#c4c4c4")
        self.zavg.insert(-1, 4)

        self.egap = tk.Entry(self)
        self.egap.place(x=70, y=300, height=23, width=70)
        self.egap.configure(background="#f2f2f2")
        self.egap.configure(font="TkFixedFont")
        self.egap.configure(foreground="#aa80bf")
        self.egap.configure(selectbackground="#c4c4c4")
        self.egap.insert(-1, 3)

        self.anm = tk.Entry(self)
        self.anm.place(x=70, y=335, height=23, width=70)
        self.anm.configure(background="#f2f2f2")
        self.anm.configure(font="TkFixedFont")
        self.anm.configure(foreground="#aa80bf")
        self.anm.configure(selectbackground="#c4c4c4")
        self.anm.insert(-1, 0.25)

        self.be1 = tk.Entry(self)
        self.be1.place(x=70, y=370, height=23, width=70)
        self.be1.configure(background="#f2f2f2")
        self.be1.configure(font="TkFixedFont")
        self.be1.configure(foreground="#aa80bf")
        self.be1.configure(selectbackground="#c4c4c4")
        self.be1.insert(-1, 285)

        self.be2 = tk.Entry(self)
        self.be2.place(x=70, y=405, height=23, width=70)
        self.be2.configure(background="#f2f2f2")
        self.be2.configure(font="TkFixedFont")
        self.be2.configure(foreground="#aa80bf")
        self.be2.configure(selectbackground="#c4c4c4")
        self.be2.insert(-1, 395)

        self.Entryangle = tk.Entry(self)
        self.Entryangle.place(x=20, y=175, height=23, width=70)
        self.Entryangle.configure(background="#f2f2f2")
        self.Entryangle.configure(font="TkFixedFont")
        self.Entryangle.configure(foreground="#aa80bf")
        self.Entryangle.configure(selectbackground="#c4c4c4")
        self.Entryangle.insert(-1, 54.7)

        self.Entryele1 = tk.Entry(self)
        self.Entryele1.place(x=250, y=100, height=23, width=60)
        self.Entryele1.configure(background="#f2f2f2")
        self.Entryele1.configure(font="TkFixedFont")
        self.Entryele1.configure(foreground="#aa80bf")
        self.Entryele1.configure(selectbackground="#c4c4c4")
        self.Entryele1.insert(-1, "c1s")

        self.TCombobox2 = ttk.Combobox(self)
        self.TCombobox2.place(x=210, y=293, height=27, width=170)
        #self.TCombobox2.configure(textvariable=self.combobox)
        self.TCombobox2.configure(takefocus="")
        self.TCombobox2['values']=("layer1","layer2","layer3")
        #self.TCombobox1.current(0)
        self.TCombobox2.bind("<<ComboboxSelected>>",self.getim)

        self.Entryele2 = tk.Entry(self)
        self.Entryele2.place(x=250, y=135, height=23, width=60)
        self.Entryele2.configure(background="#f2f2f2")
        self.Entryele2.configure(font="TkFixedFont")
        self.Entryele2.configure(foreground="#aa80bf")
        self.Entryele2.configure(selectbackground="#c4c4c4")
        self.Entryele2.insert(-1, "c1s")

        self.Entryarea1 = tk.Entry(self)
        self.Entryarea1.place(x=320, y=100, height=23, width=70)
        self.Entryarea1.configure(background="#f2f2f2")
        self.Entryarea1.configure(font="TkFixedFont")
        self.Entryarea1.configure(foreground="#aa80bf")
        self.Entryarea1.configure(selectbackground="#c4c4c4")

        self.Entryarea2 = tk.Entry(self)
        self.Entryarea2.place(x=320, y=135, height=23, width=70)
        self.Entryarea2.configure(background="#f2f2f2")
        self.Entryarea2.configure(font="TkFixedFont")
        self.Entryarea2.configure(foreground="#aa80bf")
        self.Entryarea2.configure(selectbackground="#c4c4c4")

        self.Entrydensity1 = tk.Entry(self)
        self.Entrydensity1.place(x=290, y=170, height=23, width=90)
        self.Entrydensity1.configure(background="#f2f2f2")
        self.Entrydensity1.configure(font="TkFixedFont")
        self.Entrydensity1.configure(foreground="#aa80bf")
        self.Entrydensity1.configure(selectbackground="#c4c4c4")

        self.Entrydensity2 = tk.Entry(self)
        self.Entrydensity2.place(x=290, y=205, height=23, width=90)
        self.Entrydensity2.configure(background="#f2f2f2")
        self.Entrydensity2.configure(font="TkFixedFont")
        self.Entrydensity2.configure(foreground="#aa80bf")
        self.Entrydensity2.configure(selectbackground="#c4c4c4")

        self.Label1_1_1_2 = tk.Label(self)
        self.Label1_1_1_2.place(x=200, y=250, height=30, width=189)
        self.Label1_1_1_2.configure(activebackground="#f9f9f9")
        self.Label1_1_1_2.configure(anchor='w')
        self.Label1_1_1_2.configure(background="#262626")
        self.Label1_1_1_2.configure(compound='center')
        self.Label1_1_1_2.configure(foreground="#ffffff")
        self.Label1_1_1_2.configure(text='''                   4. XPS model''')


    # here start the defining the functions, define a simplified IMFP equation
    def tpp(self, KE,z,eg,a):
        return (a**1.7)*(4 + 0.44 *z**0.5 + 0.104 *KE**0.872)/((z**0.38)*(1 - 0.02 *eg))
    #this is the get crosssection function
    def getcs(self,penergy):
        #path="/home/qiankun/python/xpsquanti/tkmethod/cs"
        #os.chdir(path)
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path1 = dir_path+'/cs'
        try:
            os.chdir(path1)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        ele1cs = loadtxt(self.Entryele1.get())
        ele2cs = loadtxt(self.Entryele2.get())
        ele1csx = ele1cs[:,0]
        ele1csy = ele1cs[:,1]
        ele1csv = interp(penergy,ele1csx,ele1csy)  #linear interpolation
        ele2csx = ele2cs[:,0]
        ele2csy = ele2cs[:,1]
        ele2csv = interp(penergy,ele2csx,ele2csy)  #linear interpolation
        ele12csv = [ele1csv,ele2csv]
        return ele12csv
    ### here get image
    def getim(self,model):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path2 = dir_path +'/images'
        try:
            os.chdir(path2)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        
        self.modelfig2=ImageTk.PhotoImage(Image.open("layer1").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig3=ImageTk.PhotoImage(Image.open("layer2").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig4=ImageTk.PhotoImage(Image.open("layer3").resize((150, 150), Image.Resampling.LANCZOS))
        if self.TCombobox2.get()== "bulk":
            pass
        elif self.TCombobox2.get()== "layer1":
            self.model1=tk.Label(self, image=self.modelfig2).place(x=220, y=320, height=150, width=150)
        elif self.TCombobox2.get()== "layer2":
            self.model1=tk.Label(self, image=self.modelfig3).place(x=220, y=320, height=150, width=150)
        elif self.TCombobox2.get()== "layer3":
            self.model1=tk.Label(self, image=self.modelfig4).place(x=220, y=320, height=150, width=150)
    # get snsitivity factors
    def getsf(self,element):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path3 = dir_path +'/sf'
        try:
            os.chdir(path3)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        sfx, sfy = [], []
        if float(self.Entryangle.get())==54.7:
            for line in open('sf54_7', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        else:
            for line in open('sf90', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        return valp

     #### here define calculate   
    def clicked(self):
        ratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        ccs = self.getcs(self.Entryphoton.get())
        ccsele1=ccs[0]
        ccsele2=ccs[1]
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        #tfilm=float(self.fthick.get())
        ele1density=float(self.Entrydensity1.get())
        ele2density=float(self.Entrydensity2.get())
        ratiobulk2=(ratiobulk1*float(ccsele2)*imfp2*ele2density)/(float(ccsele1)*imfp1*ele1density)
        ratiobulk3=ratiobulk1*ele2density/ele1density
        #ratiolayer12=ratiobulk2*(1-exp(-tfilm/imfp2))/(1-exp(-tfilm/imfp1))
        #ratiolayer21=ratiobulk1*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        #ratiolayer22=ratiobulk2*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        #ratiolayer32=ratiobulk2*exp(-tfilm/imfp2)/exp(-tfilm/imfp1)
        if self.TCombobox2.get()== "bulk":
            pass
        elif self.TCombobox2.get()== "layer1":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu.configure(text="Area=N*cs*IMFP*(1-exp(-t/IMFP))\n"+"cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"thickness cannot be calculated\n" +"exp(-t/IMFP) is the same")
            else:
                thickness=symbols("thickness")
                solution1 = nsolve((1-exp(-thickness/imfp1))-ratiobulk2*(1-exp(-thickness/imfp2)), thickness, (0.1,10))
                self.Labelresu.configure(text="Area=N*cs*IMFP*(1-exp(-t/IMFP))\n"+"CS,IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*cs2*imfp2*(1-exp(-t/imf2))/(Area2*cs1*imfp1*(1-exp(-t/imfp1))) \n"+str(solution1))
        elif self.TCombobox2.get()== "layer2":
            if self.Entryele1.get()==self.Entryele2.get():
                thickness=symbols("thickness")
                solution2 = nsolve(1-exp(-thickness/imfp1)-ratiobulk3*exp(-thickness/imfp1), thickness, (0.1,10))
                self.Labelresu.configure(text="Area1(toplayer)=N1*cs*IMFP*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*cs*IMFP*exp(-t/IMFP2)\n"+"CS ignored, IMFP1=IMFP2\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*exp(-t/imfp2)/(Area2*(1-exp(-t/imfp1))) \n"+str(solution2))
            else:
                thickness=symbols("thickness")
                solution3 = nsolve(1-exp(-thickness/imfp1)-ratiobulk2*exp(-thickness/imfp2), thickness, (0.1,10))
                self.Labelresu.configure(text="Area1(toplayer)=N1*cs*IMFP*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*cs*IMFP*exp(-t/IMFP2)\n"+"CS,IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*cs2*imfp2*exp(-t/imfp2)/(Area2*cs1*imfp1*(1-exp(-t/imfp1))) \n"+str(solution3))
        elif self.TCombobox2.get()== "layer3":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu.configure(text="Area=N*cs*IMFP*exp(-t/IMFP)\n"+"CS, IMFP ignored\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"thickness cannot be calculated\n" +"exp(-t/IMFP) is the same")
            else:
                thickness=symbols("thickness")
                solution4 = nsolve(exp(-thickness/imfp1)-ratiobulk2*exp(-thickness/imfp2), thickness, (0.1,10))
                self.Labelresu.configure(text="Area1=N1*cs1*IMFP1*exp(-t/IMFP1)\n"+"Area2=N2*cs2*IMFP2*exp(-t/IMFP2)\n"+"CS, IMFP considered\n"+ "cs1= "+str(ccsele1)  +" "+ "IMFP1= " + str(imfp1) +"\n"+"cs2= "+str(ccsele2)  +" "+ "IMFP2= " + str(imfp2)+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*cs2*imfp2*exp(-t/imfp2)/(Area2*cs1*imfp1*exp(-t/imfp1)) \n"+str(solution4))
        else:
            pass

    ### sensitiity factor calculate
    def sfclicked(self):
        sfratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        #ccs = self.getcs(self.Entryphoton.get())
        #ccsele1=ccs[0]
        #ccsele2=ccs[1]
        sfele1 = self.getsf(self.Entryele1.get())
        sfele2 = self.getsf(self.Entryele2.get())
        sfele1density=float(self.Entrydensity1.get())
        sfele2density=float(self.Entrydensity2.get())
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        sfratiobulk2=sfratiobulk1*float(sfele2)*sfele2density/(float(sfele1)*sfele1density)
      
        if self.TCombobox2.get()== "bulk":
            pass
        elif self.TCombobox2.get()== "layer1":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area=N*sf*(1-exp(-t/IMFP))\n"+"sf,IMFP, ignored \n"+ "\n"+"thickness cannot be calculated\n" +"exp(-t/IMFP) is the same")
            else:
                thickness=symbols("thickness")
                solution5 = nsolve((1-exp(-thickness/imfp1))-sfratiobulk2*(1-exp(-thickness/imfp2)), thickness, (0.1,10))
                self.Labelresu2.configure(text="Area=N*sf*(1-exp(-t/IMFP))\n"+"sf,IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2) +"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*sf2*(1-exp(-t/imf2))/(Area2*sf1*(1-exp(-t/imfp1))) \n"+str(solution5))
        elif self.TCombobox2.get()== "layer2":
            if self.Entryele1.get()==self.Entryele2.get():
                thickness=symbols("thickness")
                solution6 = nsolve(1-exp(-thickness/imfp1)-sfratiobulk2*exp(-thickness/imfp1), thickness, (0.1,10))
                self.Labelresu2.configure(text="Area1(toplayer)=N1*sf1*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*sf2*exp(-t/IMFP2)\n"+"sf,IMFP1=IMFP2\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2) +"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*exp(-t/imfp2)/(Area2*(1-exp(-t/imfp1)))\n"+str(solution6))
            else:
                thickness=symbols("thickness")
                solution7 = nsolve(1-exp(-thickness/imfp1)-sfratiobulk2*exp(-thickness/imfp2), thickness, (0.1,10))
                self.Labelresu2.configure(text="Area1(toplayer)=N1*sf1*(1-exp(-t/IMFP1))\n"+"Area2(substrate)=N2*sf2*exp(-t/IMFP2)\n"+"sf,IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*sf2*exp(-t/imfp2)/(Area2*sf1*(1-exp(-t/imfp1)))\n"+str(solution7))
        elif self.TCombobox2.get()== "layer3":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="Area=N*sf*exp(-t/IMFP)\n"+"sf ignored\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"\n"+"thickness cannot be calculated\n" +"exp(-t/IMFP) is the same")
            else:
                thickness=symbols("thickness")
                solution8 = nsolve(exp(-thickness/imfp1)-sfratiobulk2*exp(-thickness/imfp2), thickness, (0.1,10))
                self.Labelresu2.configure(text="Area1=N1*sf1*exp(-t/IMFP1)\n"+"Area2=N2*sf2*exp(-t/IMFP2)\n"+"sf, IMFP considered\n"+ "sfele1= "+str(sfele1)  +"\n"+"sfele2= "+str(sfele2)+"\n"+"\n"+"film thickness is:\n" +"N1/N2=Area1*sf2*exp(-t/imfp2)/(Area2*sf1*exp(-t/imfp1))\n"+str(solution8))
        else:
            pass

        #self.Labelresu.configure(text="the result is: "+str(ccs))

## thin film partial coverage calculation panel
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.Label1 = tk.Label(self)
        self.Label1.place(x=20, y=60, height=30, width=80)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#262626")
        self.Label1.configure(compound='left')
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''1. Ephoton''')

        self.Label1_1 = tk.Label(self)
        self.Label1_1.place(x=20, y=140, height=30, width=132)
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(anchor='w')
        self.Label1_1.configure(background="#262626")
        self.Label1_1.configure(compound='left')
        self.Label1_1.configure(foreground="#ffffff")
        self.Label1_1.configure(text='''2. angle(beam-spec)''')

        self.Label1_1_1 = tk.Label(self)
        self.Label1_1_1.place(x=200, y=60, height=30, width=189)
        self.Label1_1_1.configure(activebackground="#f9f9f9")
        self.Label1_1_1.configure(anchor='w')
        self.Label1_1_1.configure(background="#262626")
        self.Label1_1_1.configure(compound='center')
        self.Label1_1_1.configure(foreground="#ffffff")
        self.Label1_1_1.configure(text='''        3.       element    &    area''')

        self.Labelele1 = tk.Label(self)
        self.Labelele1.place(x=200, y=98, height=30, width=44)
        self.Labelele1.configure(activebackground="#f9f9f9")
        self.Labelele1.configure(anchor='w')
        self.Labelele1.configure(background="#262626")
        self.Labelele1.configure(compound='left')
        self.Labelele1.configure(foreground="#ffffff")
        self.Labelele1.configure(text='''ele1''')

        self.Labelele2 = tk.Label(self)
        self.Labelele2.place(x=200, y=135, height=30, width=44)
        self.Labelele2.configure(activebackground="#f9f9f9")
        self.Labelele2.configure(anchor='w')
        self.Labelele2.configure(background="#262626")
        self.Labelele2.configure(compound='left')
        self.Labelele2.configure(foreground="#ffffff")
        self.Labelele2.configure(text='''ele2''')

        self.Entryphoton = tk.Entry(self)
        self.Entryphoton.place(x=20, y=95, height=23, width=70)

        self.Entryphoton.configure(background="#f2f2f2")
        self.Entryphoton.configure(font="TkFixedFont")
        self.Entryphoton.configure(foreground="#aa80bf")
        self.Entryphoton.configure(selectbackground="#c4c4c4")
        self.Entryphoton.insert(-1, 1486.6)

        self.Button1 = tk.Button(self)
        self.Button1.place(x=460, y=60, height=30, width=71)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(background="#3498DB")
        self.Button1.configure(borderwidth="2")
        self.Button1.configure(command=self.clicked)
        self.Button1.configure(compound='left')
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(text='''calculate''')

        self.Button3 = tk.Button(self)
        self.Button3.place(x=460, y=280, height=30, width=140)
        self.Button3.configure(activebackground="beige")
        self.Button3.configure(background="#3498DB")
        self.Button3.configure(borderwidth="2")
        self.Button3.configure(command=self.sfclicked)
        self.Button3.configure(compound='left')
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(text='''calculate (SF method)''')


        self.Labelresu2 = tk.Label(self)
        self.Labelresu2.place(x=445, y=320)
        #self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu2.configure(anchor='w')
        self.Labelresu2.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu2.configure(compound='left')
        self.Labelresu2.configure(foreground="#000000")

        #self.Labelele3 = tk.Label(self.top)
        #self.Labelele3.place(relx=0.623, rely=0.167, height=30, width=84)
        #self.Labelele3.configure(activebackground="#f9f9f9")
        #self.Labelele3.configure(anchor='w')
        #self.Labelele3.configure(background="#262626")
        ##self.Labelele3.configure(compound='left')
        #self.Labelele3.configure(foreground="#ffffff")
        #self.Labelele3.configure(text='''the result is:''')

        self.Labelresu = tk.Label(self)
        self.Labelresu.place(x=445, y=100)
        self.Labelresu.configure(activebackground="#f9f9f9")
        self.Labelresu.configure(anchor='w')
        self.Labelresu.configure(justify=LEFT)
        #self.Labelresu.configure(background="#ffffff")
        self.Labelresu.configure(compound='left')
        self.Labelresu.configure(foreground="#000000")

        self.Labelele4 = tk.Label(self)
        self.Labelele4.place(x=20, y=225, height=30, width=159)
        self.Labelele4.configure(activebackground="#f9f9f9")
        self.Labelele4.configure(anchor='w')
        self.Labelele4.configure(background="#262626")
        self.Labelele4.configure(compound='left')
        self.Labelele4.configure(foreground="#ffffff")
        self.Labelele4.configure(text='''IMFP calculation (TPP-2M)''')

        self.Labelele5 = tk.Label(self)
        self.Labelele5.place(x=20, y=265, height=25, width=40)
        self.Labelele5.configure(activebackground="#f9f9f9")
        self.Labelele5.configure(anchor='w')
        self.Labelele5.configure(background="#262626")
        self.Labelele5.configure(compound='left')
        self.Labelele5.configure(foreground="#ffffff")
        self.Labelele5.configure(text='''Zavg''')

        self.Labelele6 = tk.Label(self)
        self.Labelele6.place(x=20, y=300, height=25, width=40)
        self.Labelele6.configure(activebackground="#f9f9f9")
        self.Labelele6.configure(anchor='w')
        self.Labelele6.configure(background="#262626")
        self.Labelele6.configure(compound='left')
        self.Labelele6.configure(foreground="#ffffff")
        self.Labelele6.configure(text='''egap''')

        self.Labelele7 = tk.Label(self)
        self.Labelele7.place(x=20, y=335, height=25, width=40)
        self.Labelele7.configure(activebackground="#f9f9f9")
        self.Labelele7.configure(anchor='w')
        self.Labelele7.configure(background="#262626")
        self.Labelele7.configure(compound='left')
        self.Labelele7.configure(foreground="#ffffff")
        self.Labelele7.configure(text='''a(nm)''')

        self.Labelele8 = tk.Label(self)
        self.Labelele8.place(x=20, y=370, height=25, width=40)
        self.Labelele8.configure(activebackground="#f9f9f9")
        self.Labelele8.configure(anchor='w')
        self.Labelele8.configure(background="#262626")
        self.Labelele8.configure(compound='left')
        self.Labelele8.configure(foreground="#ffffff")
        self.Labelele8.configure(text='''BE1''')

        self.Labelele9 = tk.Label(self)
        self.Labelele9.place(x=20, y=405, height=25, width=40)
        self.Labelele9.configure(activebackground="#f9f9f9")
        self.Labelele9.configure(anchor='w')
        self.Labelele9.configure(background="#262626")
        self.Labelele9.configure(compound='left')
        self.Labelele9.configure(foreground="#ffffff")
        self.Labelele9.configure(text='''BE2''')

        self.Labelele10 = tk.Label(self)
        self.Labelele10.place(x=20, y=435, height=25, width=100)
        self.Labelele10.configure(activebackground="#f9f9f9")
        self.Labelele10.configure(anchor='w')
        self.Labelele10.configure(background="#262626")
        self.Labelele10.configure(compound='left')
        self.Labelele10.configure(foreground="#ffffff")
        self.Labelele10.configure(text='''thickness(nm)''')

        self.fthick = tk.Entry(self)
        self.fthick.place(x=130, y=435, height=23, width=70)
        self.fthick.configure(background="#f2f2f2")
        self.fthick.configure(font="TkFixedFont")
        self.fthick.configure(foreground="#aa80bf")
        self.fthick.configure(selectbackground="#c4c4c4")
        self.fthick.insert(-1, 0.4)

        
        self.zavg = tk.Entry(self)
        self.zavg.place(x=70, y=265, height=23, width=70)
        self.zavg.configure(background="#f2f2f2")
        self.zavg.configure(font="TkFixedFont")
        self.zavg.configure(foreground="#aa80bf")
        self.zavg.configure(selectbackground="#c4c4c4")
        self.zavg.insert(-1, 4)

        self.egap = tk.Entry(self)
        self.egap.place(x=70, y=300, height=23, width=70)
        self.egap.configure(background="#f2f2f2")
        self.egap.configure(font="TkFixedFont")
        self.egap.configure(foreground="#aa80bf")
        self.egap.configure(selectbackground="#c4c4c4")
        self.egap.insert(-1, 3)

        self.anm = tk.Entry(self)
        self.anm.place(x=70, y=335, height=23, width=70)
        self.anm.configure(background="#f2f2f2")
        self.anm.configure(font="TkFixedFont")
        self.anm.configure(foreground="#aa80bf")
        self.anm.configure(selectbackground="#c4c4c4")
        self.anm.insert(-1, 0.25)

        self.be1 = tk.Entry(self)
        self.be1.place(x=70, y=370, height=23, width=70)
        self.be1.configure(background="#f2f2f2")
        self.be1.configure(font="TkFixedFont")
        self.be1.configure(foreground="#aa80bf")
        self.be1.configure(selectbackground="#c4c4c4")
        self.be1.insert(-1, 285)

        self.be2 = tk.Entry(self)
        self.be2.place(x=70, y=405, height=23, width=70)
        self.be2.configure(background="#f2f2f2")
        self.be2.configure(font="TkFixedFont")
        self.be2.configure(foreground="#aa80bf")
        self.be2.configure(selectbackground="#c4c4c4")
        self.be2.insert(-1, 395)


        self.Entryangle = tk.Entry(self)
        self.Entryangle.place(x=20, y=175, height=23, width=70)
        self.Entryangle.configure(background="#f2f2f2")
        self.Entryangle.configure(font="TkFixedFont")
        self.Entryangle.configure(foreground="#aa80bf")
        self.Entryangle.configure(selectbackground="#c4c4c4")
        self.Entryangle.insert(-1, 54.7)

        self.Entryele1 = tk.Entry(self)
        self.Entryele1.place(x=250, y=100, height=23, width=60)
        self.Entryele1.configure(background="#f2f2f2")
        self.Entryele1.configure(font="TkFixedFont")
        self.Entryele1.configure(foreground="#aa80bf")
        self.Entryele1.configure(selectbackground="#c4c4c4")
        self.Entryele1.insert(-1, "c1s")

        self.TCombobox1 = ttk.Combobox(self)
        self.TCombobox1.place(x=210, y=290, height=27, width=170)
        #self.TCombobox1.configure(textvariable=self.combobox)
        self.TCombobox1.configure(takefocus="")
        self.TCombobox1['values']=("model1","model2","model3")
        #self.TCombobox1.current(0)
        self.TCombobox1.bind("<<ComboboxSelected>>",self.getim)

        self.Entryele2 = tk.Entry(self)
        self.Entryele2.place(x=250, y=135, height=23, width=60)
        self.Entryele2.configure(background="#f2f2f2")
        self.Entryele2.configure(font="TkFixedFont")
        self.Entryele2.configure(foreground="#aa80bf")
        self.Entryele2.configure(selectbackground="#c4c4c4")
        self.Entryele2.insert(-1, "c1s")

        self.Entryarea1 = tk.Entry(self)
        self.Entryarea1.place(x=320, y=100, height=23, width=70)
        self.Entryarea1.configure(background="#f2f2f2")
        self.Entryarea1.configure(font="TkFixedFont")
        self.Entryarea1.configure(foreground="#aa80bf")
        self.Entryarea1.configure(selectbackground="#c4c4c4")

        self.Entryarea2 = tk.Entry(self)
        self.Entryarea2.place(x=320, y=135, height=23, width=70)
        self.Entryarea2.configure(background="#f2f2f2")
        self.Entryarea2.configure(font="TkFixedFont")
        self.Entryarea2.configure(foreground="#aa80bf")
        self.Entryarea2.configure(selectbackground="#c4c4c4")

        self.Label1_1_1_2 = tk.Label(self)
        self.Label1_1_1_2.place(x=200, y=250, height=30, width=189)
        self.Label1_1_1_2.configure(activebackground="#f9f9f9")
        self.Label1_1_1_2.configure(anchor='w')
        self.Label1_1_1_2.configure(background="#262626")
        self.Label1_1_1_2.configure(compound='center')
        self.Label1_1_1_2.configure(foreground="#ffffff")
        self.Label1_1_1_2.configure(text='''                   4. XPS model''')

        self.ele1density = tk.Label(self)
        self.ele1density.place(x=200, y=170, height=30, width=84)
        self.ele1density.configure(activebackground="#f9f9f9")
        self.ele1density.configure(anchor='w')
        self.ele1density.configure(background="#262626")
        self.ele1density.configure(compound='left')
        self.ele1density.configure(foreground="#ffffff")
        self.ele1density.configure(text='''density(ele1)''')

        self.ele2density = tk.Label(self)
        self.ele2density.place(x=200, y=205, height=30, width=84)
        self.ele2density.configure(activebackground="#f9f9f9")
        self.ele2density.configure(anchor='w')
        self.ele2density.configure(background="#262626")
        self.ele2density.configure(compound='left')
        self.ele2density.configure(foreground="#ffffff")
        self.ele2density.configure(text='''density(ele2)''')

        self.Entrydensity1 = tk.Entry(self)
        self.Entrydensity1.place(x=290, y=170, height=23, width=90)
        self.Entrydensity1.configure(background="#f2f2f2")
        self.Entrydensity1.configure(font="TkFixedFont")
        self.Entrydensity1.configure(foreground="#aa80bf")
        self.Entrydensity1.configure(selectbackground="#c4c4c4")

        self.Entrydensity2 = tk.Entry(self)
        self.Entrydensity2.place(x=290, y=205, height=23, width=90)
        self.Entrydensity2.configure(background="#f2f2f2")
        self.Entrydensity2.configure(font="TkFixedFont")
        self.Entrydensity2.configure(foreground="#aa80bf")
        self.Entrydensity2.configure(selectbackground="#c4c4c4")




    # here start the defining the functions, define a simplified IMFP equation
    def tpp(self, KE,z,eg,a):
        return (a**1.7)*(4 + 0.44 *z**0.5 + 0.104 *KE**0.872)/((z**0.38)*(1 - 0.02 *eg))

    #this is the get crosssection function
    def getcs(self,penergy):
        #path="/home/qiankun/python/xpsquanti/tkmethod/cs"
        #os.chdir(path)
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path1 = dir_path+'/cs'
        try:
            os.chdir(path1)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        ele1cs = loadtxt(self.Entryele1.get())
        ele2cs = loadtxt(self.Entryele2.get())
        ele1csx = ele1cs[:,0]
        ele1csy = ele1cs[:,1]
        ele1csv = interp(penergy,ele1csx,ele1csy)  #linear interpolation
        ele2csx = ele2cs[:,0]
        ele2csy = ele2cs[:,1]
        ele2csv = interp(penergy,ele2csx,ele2csy)  #linear interpolation
        ele12csv = [ele1csv,ele2csv]
        return ele12csv
    ### here get image
    def getim(self,model):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path2 = dir_path +'/images'
        try:
            os.chdir(path2)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        self.modelfig1=ImageTk.PhotoImage(Image.open("model1").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig2=ImageTk.PhotoImage(Image.open("model2").resize((150, 150), Image.Resampling.LANCZOS))
        self.modelfig3=ImageTk.PhotoImage(Image.open("model3").resize((150, 150), Image.Resampling.LANCZOS))
        self.formulafig1=ImageTk.PhotoImage(Image.open("f1-model1").resize((523,70), Image.Resampling.LANCZOS))
        self.formulafig2=ImageTk.PhotoImage(Image.open("f2-model2").resize((588,70), Image.Resampling.LANCZOS))
        self.formulafig3=ImageTk.PhotoImage(Image.open("f3-model3").resize((624,70), Image.Resampling.LANCZOS))
        if self.TCombobox1.get()== "model1":
            self.model1=tk.Label(self, image=self.modelfig1).place(x=220, y=320, height=150, width=150)
            self.formula=tk.Label(self, image=self.formulafig1).place(x=40, y=490)
        elif self.TCombobox1.get()== "model2":
            self.model1=tk.Label(self, image=self.modelfig2).place(x=220, y=320, height=150, width=150)
            self.formula=tk.Label(self, image=self.formulafig2).place(x=40, y=490)
        elif self.TCombobox1.get()== "model3":
            self.model1=tk.Label(self, image=self.modelfig3).place(x=220, y=320, height=150, width=150)
            self.formula=tk.Label(self, image=self.formulafig3).place(x=40, y=490)

    # get snsitivity factors
    def getsf(self,element):
        global dir_path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path3 = dir_path +'/sf'
        try:
            os.chdir(path3)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except PermissionError:
            pass
        sfx, sfy = [], []
        if float(self.Entryangle.get())==54.7:
            for line in open('sf54_7', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        else:
            for line in open('sf90', 'r'):
                values = [s for s in line.split()]
                sfx.append(values[0])
                sfy.append(float(values[1]))
             #determine lenghth of the list
            elep=sfx.index(element)
            valp=sfy[elep]
        return valp

     #### here define calculate   
    def clicked(self):
        #ratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        filmarea=float(self.Entryarea1.get())
        subarea=float(self.Entryarea2.get())
        ccs = self.getcs(self.Entryphoton.get())
        ccsele1=ccs[0]
        ccsele2=ccs[1]
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        #ratiobulk2=(ratiobulk1*float(ccsele2)*imfp2)/(float(ccsele1)*imfp1)
        tfilm=float(self.fthick.get())
        #ratiolayer12=ratiobulk2*(1-exp(-tfilm/imfp2))/(1-exp(-tfilm/imfp1))
        #ratiolayer21=ratiobulk1*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        #ratiolayer22=ratiobulk2*exp(-tfilm/imfp2)/(1-exp(-tfilm/imfp1))
        #ratiolayer32=ratiobulk2*exp(-tfilm/imfp2)/exp(-tfilm/imfp1)
        ele1density=float(self.Entrydensity1.get())
        ele2density=float(self.Entrydensity2.get())
        #ratiobulk2=(ratiobulk1*float(ccsele2)*imfp2*ele2density)/(float(ccsele1)*imfp1*ele1density)
        #ratiobulk3=ratiobulk1*ele2density/ele1density


        if self.TCombobox1.get()== "model1":
            if self.Entryele1.get()==self.Entryele2.get():
                #tkinter.messagebox.showinfo('the answer is: ', 'CS and IMFP ignored\n' ,ccs)
                self.Labelresu.configure(text="coverage cannot be calculated\n"+ "details see the equation")
            else:
                self.Labelresu.configure(text="coverage cannot be calculated\n"+ "details see the equation")
        elif self.TCombobox1.get()== "model2":
            if self.Entryele1.get()==self.Entryele2.get():
                fcov=symbols("fcov")
                cover1 = nsolve(filmarea*ele2density/(subarea*ele1density*(1-exp(-tfilm/imfp1))+filmarea*ele2density*(1-exp(-tfilm/imfp2)))-fcov, fcov, (0.1,1))
                self.Labelresu.configure(text="CS ignored\n"+"film coverage is:\n" +str(cover1))
            else:
                fcov=symbols("fcov")
                cover2 = nsolve(filmarea*ele2density*imfp2*ccsele2/(subarea*ele1density*imfp1*ccsele1*(1-exp(-tfilm/imfp1))+filmarea*ele2density*imfp2*ccsele2*(1-exp(-tfilm/imfp2)))-fcov, fcov, (0.1,1))
                self.Labelresu.configure(text="CS, IMFP considered\n"+"film coverage is:\n" +str(cover2))
        elif self.TCombobox1.get()== "model3":
            if self.Entryele1.get()==self.Entryele2.get():
                fcov=symbols("fcov")
                cover3 = nsolve((filmarea*ele2density-subarea*ele1density)/(filmarea*ele2density-subarea*ele1density+subarea*ele1density*exp(-tfilm/imfp1)-filmarea*ele2density*exp(-tfilm/imfp2))-fcov, fcov, (0.1,1))
                self.Labelresu.configure(text="CS, IMFP ignored\n"+"film coverage is:\n" +str(cover3))
            else:
                fcov=symbols("fcov")
                cover4 = nsolve((filmarea*ele2density*ccsele2*imfp2-subarea*ele1density*ccsele1*imfp1)/(filmarea*ele2density*ccsele2*imfp2-subarea*ele1density*ccsele1*imfp1+subarea*ele1density*ccsele1*imfp1*exp(-tfilm/imfp1)-filmarea*ele2density*ccsele2*imfp2*exp(-tfilm/imfp2))-fcov, fcov, (0.1,1))
                self.Labelresu.configure(text="CS, IMFP considered\n"+"film coverage is:\n" +str(cover4))
        else:
            pass

    ### sensitiity factor calculate
    def sfclicked(self):
        #sfratiobulk1=float(self.Entryarea1.get())/float(self.Entryarea2.get()) #ratiolayer1 is the same as this
        filmarea=float(self.Entryarea1.get())
        subarea=float(self.Entryarea2.get())
        #ccs = self.getcs(self.Entryphoton.get())
        #ccsele1=ccs[0]
        #ccsele2=ccs[1]
        sfele1 = self.getsf(self.Entryele1.get())
        sfele2 = self.getsf(self.Entryele2.get())
        ke1=float(self.Entryphoton.get())-float(self.be1.get())
        ke2=float(self.Entryphoton.get())-float(self.be2.get())
        imfp1=self.tpp(ke1,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        imfp2=self.tpp(ke2,float(self.zavg.get()),float(self.egap.get()),float(self.anm.get()))
        #sfratiobulk2=sfratiobulk1*float(sfele2)/float(sfele1)
        tfilm=float(self.fthick.get())
        ele1density=float(self.Entrydensity1.get())
        ele2density=float(self.Entrydensity2.get())
        if self.TCombobox1.get()== "model1":
            if self.Entryele1.get()==self.Entryele2.get():
                self.Labelresu2.configure(text="coverage cannot be calculated\n"+ "details see the equation")
            else:
                self.Labelresu2.configure(text="coverage cannot be calculated\n"+ "details see the equation")
        elif self.TCombobox1.get()== "model2":
            if self.Entryele1.get()==self.Entryele2.get():
                fcov=symbols("fcov")
                cover5 = nsolve(filmarea*ele2density/(subarea*ele1density*(1-exp(-tfilm/imfp1))+filmarea*ele2density*(1-exp(-tfilm/imfp2)))-fcov, fcov, (0.1,1))
                self.Labelresu2.configure(text="sf ignored\n"+"film coverage is:\n" +str(cover5))
            else:
                fcov=symbols("fcov")
                cover6 = nsolve(filmarea*ele2density*sfele2/(subarea*ele1density*sfele1*(1-exp(-tfilm/imfp1))+filmarea*ele2density*sfele2*(1-exp(-tfilm/imfp2)))-fcov, fcov, (0.1,1))
                self.Labelresu2.configure(text="CS, IMFP considered\n"+"film coverage is:\n" +str(cover6))
        elif self.TCombobox1.get()== "model3":
            if self.Entryele1.get()==self.Entryele2.get():
                fcov=symbols("fcov")
                cover7 = nsolve((filmarea*ele2density-subarea*ele1density)/(filmarea*ele2density-subarea*ele1density+subarea*ele1density*exp(-tfilm/imfp1)-filmarea*ele2density*exp(-tfilm/imfp2))-fcov, fcov, (0.1,1))
                self.Labelresu2.configure(text="CS, IMFP ignored\n"+"film coverage is:\n" +str(cover7))
            else:
                fcov=symbols("fcov")
                cover8 = nsolve((filmarea*ele2density*sfele2-subarea*ele1density*sfele1)/(filmarea*ele2density*sfele2-subarea*ele1density*sfele1+subarea*ele1density*sfele1*exp(-tfilm/imfp1)-filmarea*ele2density*sfele2*exp(-tfilm/imfp2))-fcov, fcov, (0.1,1))
                self.Labelresu2.configure(text="CS, IMFP ignored\n"+"film coverage is:\n" +str(cover8))
        else:
            pass

        #self.Labelresu.configure(text="the result is: "+str(ccs))
    
    

## define main window
class MainView(tk.Frame):
    
    def __init__(self, top=None):
        tk.Frame.__init__(self, top=None)
        top.geometry("850x650+594+153")
        top.minsize(850, 650)
        #top.maxsize(1351, 738)
        top.resizable(1,  1)
        top.title("XPS quantification")
        #top.configure(background="black")
        top.configure(highlightcolor="black")

        self.top = top
        self.combobox = tk.StringVar()
         
        p0 = Page0(self)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
       

        buttonframe = tk.Frame(self)
        buttonframe.configure(background="#87762b")
        container = tk.Frame(self)
        #container.configure(background="#919190")
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p0.place(in_=container, x=0, y=0, width=1100, height=800)
        p1.place(in_=container, x=0, y=0, width=1100, height=800)
        p2.place(in_=container, x=0, y=0, width=1100, height=800)
        p3.place(in_=container, x=0, y=0, width=1100, height=800)


        self.Peakfitting = tk.Button(buttonframe)
        self.Peakfitting.place(x=0, y=10, height=30, width=91)
        #self.Peakfitting.configure(activebackground="#3498DB")
        self.Peakfitting.configure(background="#3498DB")
        self.Peakfitting.configure(borderwidth="2")
        self.Peakfitting.configure(command= lambda:[self.peclickcolr(), p0.show()])
        self.Peakfitting.configure(compound='left')
        self.Peakfitting.configure(foreground="#ffffff")
        self.Peakfitting.configure(text='''peak fitting''')
        self.Peakfitting.pack(side="left")
       

        self.atomratio = tk.Button(buttonframe)
        self.atomratio.place(x=150, y=10, height=30, width=91)
        #self.atomratio.configure(activebackground="#3498DB")
        self.atomratio.configure(background="#3498DB")
        self.atomratio.configure(borderwidth="2")
        self.atomratio.configure(command= lambda:[self.atclickcolr(),p1.show()])
        self.atomratio.configure(compound='left')
        self.atomratio.configure(foreground="#ffffff")
        self.atomratio.configure(text='''atomic ratio''')
        self.atomratio.pack(side="left")

        self.fthick = tk.Button(buttonframe)
        self.fthick.place(x=300, y=10, height=30, width=101)
        #self.fthick.configure(activebackground="#3498DB")
        self.fthick.configure(background="#3498DB")
        self.fthick.configure(borderwidth="2")
        self.fthick.configure(command= lambda:[self.ftclickcolr(), p2.show()])
        self.fthick.configure(compound='left')
        self.fthick.configure(foreground="#ffffff")
        self.fthick.configure(text='''film thickness''')
        self.fthick.pack(side="left")

        self.fcover = tk.Button(buttonframe)
        self.fcover.place(x=450, y=10, height=30, width=101)
        #self.fcover.configure(activebackground="#3498DB")
        self.fcover.configure(background="#3498DB")
        self.fcover.configure(borderwidth="2")
        self.fcover.configure(command= lambda:[self.fcovercolor(), p3.show()])
        self.fcover.configure(compound='left')
        self.fcover.configure(foreground="#ffffff")
        self.fcover.configure(text='''film coverage''')
        self.fcover.pack(side="left")

        self.closewindow = tk.Button(buttonframe)
        self.closewindow.place(x=550, y=10, height=30, width=71)
        #self.closewindow.configure(activebackground="beige")
        self.closewindow.configure(background="#641E16")
        self.closewindow.configure(borderwidth="2")
        self.closewindow.configure(command=self.quit)
        self.closewindow.configure(compound='left')
        self.closewindow.configure(foreground="#ffffff")
        self.closewindow.configure(text='''quit''')
        self.closewindow.pack(side="left")

        #p1.show()
    def peclickcolr(self):
        self.Peakfitting.configure(background="#918f8e")
        self.atomratio.configure(background = "#3498DB")
        self.fthick.configure(background="#3498DB")
        self.fcover.configure(background="#3498DB")

    def atclickcolr(self):
        self.atomratio.configure(background = "#918f8e")
        self.fthick.configure(background="#3498DB")
        self.Peakfitting.configure(background="#3498DB")
        self.fcover.configure(background="#3498DB")
    def ftclickcolr(self):
        self.fthick.configure(background = "#918f8e")
        self.atomratio.configure(background="#3498DB")
        self.Peakfitting.configure(background="#3498DB")
        self.fcover.configure(background="#3498DB")

    def fcovercolor(self):
        self.fthick.configure(background = "#3498DB")
        self.atomratio.configure(background="#3498DB")
        self.Peakfitting.configure(background="#3498DB")
        self.fcover.configure(background="#918f8e")
        


    ###quit function
    def quit(self):
        self.top.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()