#C:\Users\Administrator\Desktop\QORs_Detailed_Timing_Report

#C:\Users\Administrator\Desktop\QORs_Detailed_Timing_Report
#import pandas as pd
#import numpy as np
import linecache
import re
import tkinter  
from  tkinter import ttk  #导入内部包  
from tkinter import Tk, Scrollbar, Frame
import tktable
from tkinter.ttk import Treeview
import tkinter as tk

#file=input("The object file:")
file_object=open("C:/Users/Administrator/Desktop/QORs_Detailed_Timing_Report")

file_context=file_object.read()
file_context_1=file_object.readline()
#print(file_context)
s=file_context.split('\n')
#print(s)
t=file_context.split('\n\n\n')

#a=re.search(r'Path\sGroup\:.\w*.',file_context)
#print(a.group())
# b=re.findall(r'Startpoint\:.([a-z].*)','Startpoint: wdata[0] (input port clocked by wclk)')
# print(b)

#提取Startpoint
Startpoint1=[]
for str0 in t:
    if re.search(r'Startpoint\:.[a-z].*',str0):
        Startpoint=re.findall(r'Startpoint\:.([a-z].*)',str0)
        #print(Startpoint)
        
        for item in Startpoint:
            Startpoint1.append(item.split('(')[0].replace(' ',''))
            #print(item.split('(')[0],end=',')
#print("Startpoint:\n",Startpoint1)

#提取Endpoint
Endpoint1=[]
for str1 in t:
    if re.search(r'Endpoint\:.[a-z].*',str1):
        Endpoint=re.findall(r'Endpoint\:.([a-z].*)',str1)
        Endpoint1.append(Endpoint)
#print("Endpoint:\n",Endpoint1)
        #Endpoint1=[]
        #for item in Endpoint1:
            #Endpoint1.append(item.split('(')[0].replace(' ',''))
            #print(item.split('(')[0],end=',')
        #print(Endpoint1)

#提取slack部分的数据
slack1=[]
for str3 in t:
    if re.search(r'slack.*[0-9]+',str3):
        slack=re.findall(r'slack.*(.\d\.\d*)',str3)
        slack1.append(slack)
#print("slack:\n",slack1)

#提取clock group
clock_group1=[]
for str4 in t:
    if re.search(r'Path\sGroup\:.\w*.',str4):
        clock_group=re.findall(r'Path\sGroup\:.(\w*)',str4)
        clock_group1.append(clock_group)
#print("clock_group:\n",clock_group1)


win=tkinter.Tk()
win.geometry('500x300+400+300')
win.title('Timing_Report')
frame = Frame(win)
frame.place(x=0, y=10, width=480, height=280)

tree=ttk.Treeview(win)#表格  
tree["columns"]=("Startpoint","Endpoint","slack","clock_group")  
tree.column("Startpoint",width=200)   #表示列,不显示  
tree.column("Endpoint",width=200)  
tree.column("slack",width=200)
tree.column("clock_group",width=200) 
  
tree.heading("Startpoint",text="Startpoint")  #显示表头  
tree.heading("Endpoint",text="Endpoint")  
tree.heading("slack",text="slack")  
tree.heading("clock_group",text="clock_group")  

 #插入数据， 
#print(gate_name_array)
#print(total_delay_array)
a=len(Startpoint1)
#print(a)
for i in range(0,a):  
    tree.insert("",i,text="context" ,values=(Startpoint1[i],Endpoint1[i],slack1[i],clock_group1[i]))
    i=i+1
    
tree.pack()  
win.mainloop()
