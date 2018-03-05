
from tkinter import *
from tkinter import ttk

import re

def detail_report_window(report):
    #the confirm botton command
    def closeWindow():
        t.destroy()
    #set for report
    report_s=report.split('\n')
    report_p=report.split('\n\n')

    # the first table data
    Startpoint=(re.search('Startpoint:(.*)\n\s*E',report_p[0],re.S)).group(1)
    Endpoint=(re.search('Endpoint:(.*)\n\s*Path Group',report_p[0],re.S)).group(1)
    Path_Group=(re.search('Path Group:(.*)',report_p[0])).group(1)
    Path_Type=(re.search('Path Type:(.*)',report_p[0])).group(1)
    # the second table data
    Point=[]
    Cap=[]
    Trans=[]
    Incr=[]
    Path=[]
    row_number=0
    for str1 in report_s:
        abc=[]
        bcd=[]
        if re.search(r'-?\d+\.\d*',str1):
            letter=re.split('\s\s\s',str1)
            Point.append(letter[0])
            a=re.search(r'\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*[a-z]?$',str1,re.I)
            s=a.groups()
            s=list(s)
            for str2 in s:
               if str2!=None:
                   abc.append(str2)
            for i in range(0,4-len(abc)):
                bcd.append("")
            bcd.extend(abc)
            Cap.append(bcd[0])
            Trans.append(bcd[1])
            Incr.append(bcd[2])
            Path.append(bcd[3])
            row_number+=1
    
    t = Tk()
    t.title('the detailed report')

    # The Frame set
    frmUP = Frame(width=550, height=100, bg='white')
    frmCE = Frame(width=550, height=450, bg='white')
    frmLW = Frame(width=550, height=35)
    frmUP.grid(row=0, column=0, padx=3, pady=3)
    frmCE.grid(row=1, column=0, padx=3, pady=3)
    frmLW.grid(row=2, column=0)
    frmUP.grid_propagate(0)
    frmCE.grid_propagate(0)
    frmLW.grid_propagate(0)

    # The Confirm botton
    btn =Button(frmLW, text='Confirm', width = 8, command=closeWindow)
    btn.grid(row=2)
    btn.place(x=480)


   # Put the data in the first table
    tree1 = ttk.Treeview(frmUP, show=["tree"], height=5, columns=("title1"))   
    tree1.column("title1",width=347) 
    tree1.insert('',0, text="Startpoint",values=(Startpoint),tags = ["display"])
    tree1.insert('',1, text="Endpoint",values=(Endpoint),tags = ["display"])
    tree1.insert('',2, text="Path Group",values=(Path_Group),tags = ["display"])
    tree1.insert('',3, text="Path Type",values=(Path_Type),tags = ["display"])
    tree1.tag_configure("display", foreground='blue')
    tree1.grid(row=0,column=0)

    # Put the data in the second table
    tree2 = ttk.Treeview(frmCE, show=["headings"], height=21,columns=("content0", "content1", "content2", "content3", "content4"))
    tree2.column("content0",width=330)   
    tree2.column("content1",width=50)  
    tree2.column("content2",width=50)
    tree2.column("content3",width=50)
    tree2.column("content4",width=50)

    tree2.heading("content0",text="Point") 
    tree2.heading("content1",text="Cap")  
    tree2.heading("content2",text="Trans")  
    tree2.heading("content3",text="Incr")
    tree2.heading("content4",text="Path")
    ttk.Style().configure("Treeview.Heading", foreground='green')
    for i in range(row_number):  
        tree2.insert("",i,values=(Point[i],Cap[i],Trans[i],Incr[i],Path[i]))

    # set the rollbar for second table
    vbar = ttk.Scrollbar(frmCE, orient=VERTICAL, command = tree2.yview)
    tree2.configure(yscrollcommand=vbar.set)
    tree2.grid(row=0)
    vbar.grid(row=0, column=1,sticky=NS)
    t.resizable(False, False)


# search for the detailed report
def match_detail(path1,path2,path_group):
    QOR_report=open(path1).read()
    Detailed_QOR_report=open(path2).read()
    for str in QOR_report.split('\n\n'):
        if re.search(path_group ,str, re.M|re.I):
            fact=re.search(r'Critical Path Slack:(.*)',str,re.M|re.I)
            slack=fact.group(1)
            i=0
            for str in Detailed_QOR_report.split('\n\n\n'):
                if re.search(r'Path Group: '+path_group,str,re.M|re.I):
                    if re.search(r'slack.*'+slack,str,re.M|re.I):
                        if i<1:
                            detail = re.search(r'Startpoint:.*slack.*\d', str, re.M|re.I|re.S|re.DOTALL)
                            detail_report_window(detail.group())
                            i+=1
            
Detailed_QOR_report_path="C:/Users/Ting Wang/Desktop/tool/QORs_Detailed_Timing_Report.txt"
QOR_report_path="C:/Users/Ting Wang/Desktop/tool/QOR_Report_File.txt"
Path_Group=input("Path_Group: ")
match_detail(QOR_report_path, Detailed_QOR_report_path, Path_Group)


    
