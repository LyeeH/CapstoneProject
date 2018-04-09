#Find the number of times each cell appears in that report
#C:\Users\Administrator\Desktop\QORs_Detailed_Timing_Report

import linecache
import re
import tkinter  
from  tkinter import ttk  #导入内部包  
from tkinter import Tk, Scrollbar, Frame

from tkinter.ttk import Treeview
import tkinter as tk

#file=input("The object file:")

file_object=open("/Users/mu/Desktop/ECE412/CAPSTONE_GUI_2018/scripts/QORs_Detailed_Timing_Report")
#/Users/mu/Desktop/ECE412/CAPSTONE_GUI_2018/scripts/QORs_Detailed_Timing_Report
#/Users/mu/Desktop/ECE412/wk1/shiyan.txt
file_context=file_object.read()
#print(file_context)
file_context_1=file_object.readline()
#print(file_context)
s=file_context.split('\n')
#print(s)
#将所有带有门的行找到存进矩阵
#find all the line with gates
gate_line_array=[]
gate_line_array_gate=[]
gate_line_array_numb=[]
gate_line_other=[]
for gate_line in s:
    if re.search(r'.*(\([A-Z0-9]*\))\s*(\d\.\d\d\d)\s*(\d\.\d\d\d)\s*(\d\.\d\d\d)\s*(\d\.\d\d\d).*',gate_line):
        #print(gate_line)
        gate_line_array.append(gate_line)
    if re.search(r'.*(\([A-Z0-9]*\))$',gate_line):
        gate_line_array_gate.append(gate_line)
        #print(gate_line)
    if re.search(r'^\s*(-?\d+\.\d*)\s*(-?\d+\.\d*)\s*(-?\d+\.\d*)\s*(-?\d+\.\d*)\s*',gate_line):
        #print(gate_line)
        gate_line_array_numb.append(gate_line)

for i in range(len(gate_line_array_gate)):
    gate_line_other=gate_line_array_gate[i]+gate_line_array_numb[i]

#print(len(gate_line_array))
    #gate_line_array_gate.extend(gate_line_array_numb)
#print(gate_line_array_gate)
#print(gate_line_other)
gate_line_array.append(gate_line_other)
gate_line_array.sort()
#print(gate_line_array)
#print(gate_line_array)
    #print(gate_line_array.sort())

#将所有门提出存进矩阵
#find all the gate and put them into an array
gate_name_array=[]
for gate_name in gate_line_array:
    gate_name_1=re.findall(r'.*\(.*\)',gate_name)
    #print(gate_name_1)
    gate_name_array.append(gate_name_1)
#print("gate_name_array",gate_name_array)

#将门进行排序
#sort the gate by name
gate_name_array.sort()
#print(gate_name_array)

#计算每个门出现了几次
#calculate how many times does the gate show
h=[]
for i in gate_name_array:
    h.append(gate_name_array.count(i))
#print(h)


#计算slack为负数的和，一小块一小块报告的
#calculate the negative slack
neslack=''
total_s=0.000
t=file_context.split('\n\n\n')
for str0 in t:
    if re.search('slack.*\-[0-9]+',str0):
        slack=re.findall('slack.*(\-.*)',str0)
        #print(slack)
        #print(float(slack.group(1)))
        for i in slack:
            total_s=(total_s*1000+float(i)*1000)/1000
#print(total_s)


#计算total delay/每一个门的
#calculate total delay        
#gate_line_1=[]
#gate_line_name=[]
#for gate_line in s:
    #if re.search(r'.*(\([A-Z0-9]*\))\s*(\d\.\d\d\d)\s*(\d\.\d\d\d)\s*(\d\.\d\d\d)\s*(\d\.\d\d\d).*',gate_line):
        #gate_line_1.append(gate_line)
#print(gate_line_1)
#gate_line_1.sort()
#print(gate_line_1)

total_delay_array=[]
for c in gate_line_array:
    a=re.search(r'.*(\([A-Z0-9]*\))\s*(-?\d\.\d\d\d)\s*(-?\d\.\d\d\d)\s*(-?\d\.\d\d\d)\s*(-?\d\.\d\d\d).*',c)
    s=a.groups()
    s=list(s)
    #print(s)
    column_2=float(s[len(s)-3])*1000
    column_3=float(s[len(s)-2])*1000
    #print(s[len(s)-3])
    total_delay=(column_2+column_3)/1000
    total_delay_array.append(total_delay)
#print(total_delay_array)

        
#print("The cell names %s\n their delays in -ve paths is %s\n and the total -ve slack in all paths is %s\n the cells appear and how many times the cells appeared is %s\n."
    #%(gate_name_array,total_s,total_delay_array,h))


win=tkinter.Tk()
win.geometry('500x300+400+300')
win.title('Timing_Report')
frame = Frame(win)
frame.place(x=0, y=10, width=480, height=280)

tree=ttk.Treeview(win)#表格  
tree["columns"]=("cell names","delays in -ve paths","total -ve slack","times")  
tree.column("cell names",width=200)   #表示列,不显示  
tree.column("delays in -ve paths",width=200)  
tree.column("total -ve slack",width=200)
tree.column("times",width=200) 
  
tree.heading("cell names",text="cell names")  #显示表头  
tree.heading("delays in -ve paths",text="delays in -ve paths")  
tree.heading("total -ve slack",text="total -ve slack")  
tree.heading("times",text="times")  

 #插入数据， 
#print(gate_line_array)
#print(total_delay_array)
#print(gate_name_array)

#print(len(gate_name_array))
#print(len(total_delay_array))
#print(len(h))
for i in range(len(gate_name_array)):  
    tree.insert("",i,text="context" ,values=(gate_name_array[i],total_s,total_delay_array[i],h[i]))
    #i=i+1
    
tree.pack()  
win.mainloop()
