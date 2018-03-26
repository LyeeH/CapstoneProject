from tkinter import *
from tkinter import ttk
import re
import pandas as pd
from pandas import Series,DataFrame


def gosp(*args):
    global sp
    sp=comboxlistsp.get()
    
def goep(*args):
    global ep
    ep=comboxlistep.get()

def separated_report_data(startp,endp,Detailed_QOR_report):
    startp=startp.replace('[','\[')
    startp=startp.replace(']','\]')
    endp=endp.replace('[','\[')
    endp=endp.replace(']','\]')
    selected_report=re.search(r'Startpoint:\s%s.*\n(?:.*\n)*?.*Endpoint:\s%s.*(?:.*\n)*?.*slack.*'%(startp,endp),Detailed_QOR_report)    
    selected_report=selected_report.group()

    Point=[]
    Cap=[]
    Trans=[]
    Incr=[]
    Path=[]
    #print(selected_report)
    data = {"Point":[],"Cap":[],"Trans":[],"Incr":[],"Path":[]}
    pretable=DataFrame(data,columns=['Point','Cap','Trans','Incr','Path'])
    #print(pretable)
    selected_report=selected_report.split('-\n')
    selected_report=selected_report[len(selected_report)-3]
    #print(selected_report)
    selected_report=selected_report.split('\n')
    for line in selected_report:
        abc=[]
        bcd=[]
        if not re.search('time|delay|slack|-',line):
            whole=re.search(r'(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*[a-z]?$',line)
            s=whole.groups()
            s=list(s)
            for str2 in s:
                if str2!=None:
                    abc.append(str2)
            if abc!=[]:
                for i in range(0,4-len(abc)):
                    bcd.append("")
                bcd.extend(abc)
                Cap.append(bcd[0])
                Trans.append(bcd[1])
                Incr.append(bcd[2])
                Path.append(bcd[3])
            whole=whole.group()
            point=re.sub(whole,'',line)
            point=point.strip()
            if re.search(r'\S',point):
                Point.append(point)
    pretable["Point"]=Series(Point)
    pretable["Cap"]=Series(Cap)
    pretable["Trans"]=Series(Trans)
    pretable["Incr"]=Series(Incr)
    pretable["Path"]=Series(Path)
    return pretable

def comparison_pretable(table1,table2,op):
    if op=='Cap':
        ptdata='Cap'
    elif op=='Slope':
        ptdata='Trans'
    elif op=='Incr Delay':
        ptdata='Incr'
    elif op=='Path Delay':
        ptdata='Path'
    table1_op=op+' '+'from 1st report'
    table2_op=op+' '+'from 2nd report'
    diff='Diff_'+op
    _table = {"Cell or net name":[],table1_op:[],table2_op:[],diff:[]}
    table=DataFrame(_table,columns=['Cell or net name',table1_op,table2_op,diff])
    table['Cell or net name']=table1['Point']
    table[table1_op]=table1[ptdata]
    table[table2_op]=table2[ptdata]
    table[table1_op]=pd.to_numeric(table[table1_op])
    table[table2_op]=pd.to_numeric(table[table2_op])
    table[diff]=pd.to_numeric(table[diff])
    table[diff]=table[table1_op]-table[table2_op]
#    table[[table1_op,table2_op,diff]]=table[[table1_op,table2_op,diff]].astype(object)
    #print(table)
    return table
def convert1():
    option='Cap'
    drawtable(sp,ep,option)
def convert2():
    option='Slope'
    drawtable(sp,ep,option)
def convert3():
    option='Incr Delay'
    drawtable(sp,ep,option)
def convert4():
    option='Path Delay'
    drawtable(sp,ep,option)
def drawtable(Sp,Ep,option):
    frame1.grid_forget()
    pretable1=separated_report_data(Sp,Ep,Detailed_QOR_report1)
    pretable2=separated_report_data(Sp,Ep,Detailed_QOR_report2)
    comtable=comparison_pretable(pretable1,pretable2,option)
    #print(comtable)
    comtable=comtable.fillna(0)
    #print(comtable.dtypes)
    #print(comtable[comtable.columns[0]])
    frame= Frame(win,width=800, height=400)
    frame.grid(row=0, column=0, padx=3, pady=3)
    frame.grid_propagate(0)
    tree1 = ttk.Treeview(frame, show=["headings"], height=19,columns=("content0", "content1", "content2", "content3"))
    tree1.column("content0",width=350)   
    tree1.column("content1",width=170)  
    tree1.column("content2",width=170)
    tree1.column("content3",width=95)
    tree1.heading("content0",text=comtable.columns[0]) 
    tree1.heading("content1",text=comtable.columns[1])  
    tree1.heading("content2",text=comtable.columns[2])  
    tree1.heading("content3",text=comtable.columns[3])
    ttk.Style().configure("Treeview.Heading", foreground='green')
    for i in range(len(comtable)):  
        tree1.insert("",i,values=(comtable[comtable.columns[0]][i],"%.3f"%comtable[comtable.columns[1]][i],"%.3f"%comtable[comtable.columns[2]][i],"%.3f"%comtable[comtable.columns[3]][i]))
    vbar = ttk.Scrollbar(frame, orient=VERTICAL, command = tree1.yview)
    tree1.configure(yscrollcommand=vbar.set)
    tree1.grid(row=0)
    vbar.grid(row=0, column=1,sticky=NS)


Detailed_QOR_report_path1="C:/Users/Ting Wang/Desktop/tool/QORs_Detailed_Timing_Report.txt"
Detailed_QOR_report_path2="C:/Users/Ting Wang/Desktop/tool/QORs_Detailed_Timing_Report1.txt"
Detailed_QOR_report1=open(Detailed_QOR_report_path1).read()
Detailed_QOR_report2=open(Detailed_QOR_report_path2).read()
spset=re.findall(r'Startpoint:\s(\S*)',Detailed_QOR_report1+Detailed_QOR_report2)
spset=list(set(spset))
#print(spset)
spset.sort()
epset=re.findall(r'Endpoint:\s(\S*)',Detailed_QOR_report1+Detailed_QOR_report2)
epset=list(set(epset))
epset.sort()
#print(epset)
win=Tk()
win.title('comparison option')
frame1= Frame(win, width=850, height=400)
frame1.grid(row=0, column=0, padx=3, pady=3)
frame1.grid_propagate(0)
labelsp = ttk.Label(frame1, text='Startpoint:',font = ('Times New Roman','14'),foreground='gray')
labelsp.grid(row=0, column=0, pady=100)
win.resizable(False, False)


comvalue1=StringVar()
comboxlistsp=ttk.Combobox(frame1,textvariable=comvalue1,width=30)
comboxlistsp["values"]= (spset)
comboxlistsp.bind("<<ComboboxSelected>>",gosp)
comboxlistsp.grid(row=0, column=1, pady=100)



labelep = ttk.Label(frame1, text='Endpoint:',font = ('Times New Roman','14'),foreground='gray')
labelep.grid(row=0, column=2, pady=100)


comvalue2=StringVar()
comboxlistep=ttk.Combobox(frame1,textvariable=comvalue2,width=30)
comboxlistep["values"]= (epset)
comboxlistep.grid(row=0, column=3,pady=100)
comboxlistep.bind("<<ComboboxSelected>>",goep)
#comboxlistep.grid(row=0, column=3,pady=100)


label = ttk.Label(frame1, text='Comparison Option:',font = ('Times New Roman','14'),foreground='gray')
label.grid(row=1, column=0,padx=25)
btncap = Button(frame1, text='Cap',font = ('Times New Roman','10'),width=19,command=convert1)
btncap.grid(row=2, column=0,pady=25)
btnslope= Button(frame1, text='Slope',font = ('Times New Roman','10'),width=19,command=convert2)
btnslope.grid(row=2, column=1,pady=25)
btnidelay = Button(frame1, text='Incr Delay',font = ('Times New Roman','10'),width=19,command=convert3)
btnidelay.grid(row=2, column=2,pady=25)
btnpdelay = Button(frame1, text='Path Delay',font = ('Times New Roman','10'),width=19,command=convert4)
btnpdelay.grid(row=2, column=3,pady=25)
win.mainloop()
