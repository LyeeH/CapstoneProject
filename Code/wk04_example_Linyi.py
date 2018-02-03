import linecache
import os
import sys
import tkinter as tk
import re
from tkinter import filedialog, ttk

import tktable

gl_file_path = ''
gl_add_file_path = ''
table_data = []
current_data = []
current_col_num = 0
sort_seq_flag = 0
sort_row_flag = 0
gl_report_num = 0
report_tag = {}
current_tag = []
report_color = {'1':'lemon chiffon','2':'pink2','3':'powder blue','4':'medium aquamarine'}

def findstr(file, str,record):
    
    f = open(file, "r+")
    i = 1
    for line in f:
        if line.find(str) != -1:
            #print(linecache.getline(gl_file_path,i+1))
            #print(f.next())
            record.append(i)
        i = i + 1

def tag_reconfigure(master,tag_color):
    global gl_report_num,report_tag,report_color
    # f = report_tag.items()
    for i in range(1,gl_report_num+1):
        master.tb.tag_configure('Report%i' % (i),bg=None)
        master.tb.tag_delete('Report%i' % (i))
    col_count = 1
    for j in tag_color:
        index = '%i' % (col_count)
        master.tb.tag_col('Report%i' % (j),index)
        col_count+=1
    for k in range(1,gl_report_num+1):
        master.tb.tag_configure('Report%i' % (k),bg=report_color['%i' % (k)])

def sortby_initial():
    global report_tag,current_data
    raw_tag_color = []
    for num in range(1,len(report_tag)+1):
        raw_tag_color.append(report_tag['%i' % (num)])
    tag_reconfigure(tb1,raw_tag_color)
    tb1.assign_var(current_data)   

def sortby_raw():
    global report_tag,current_data,current_tag
    new_tag_color = []
    for i in current_tag:
        new_tag_color.append(report_tag['%i' % (i)])
    tag_reconfigure(tb1,new_tag_color)
    tb1.assign_var(current_data) 

def sortby_htl(row_count):
    global report_tag,current_data
    new_data = []
    new_tag_color = []
    for i in range(1,len(current_data)):
        if new_data == []:
            new_data.append(current_data[i])
            new_tag_color.append(report_tag['%i' % (current_tag[0])])
        else:
            for j in range(0,len(new_data)):
                k = False
                if float(current_data[i][row_count]) >= float(new_data[j][row_count]):
                    new_data.insert(j,current_data[i])
                    new_tag_color.insert(j,report_tag['%i' % (current_tag[i-1])])
                    k = True
                    break
            if k == False:
                new_data.append(current_data[i])
                new_tag_color.append(report_tag['%i' % (current_tag[i-1])])
    new_data.insert(0,current_data[0])
    tag_reconfigure(tb1,new_tag_color)
    tb1.assign_var(new_data)

def sortby_lth(row_count):
    global report_tag
    new_data = []
    new_tag_color = []
    for i in range(1,len(current_data)):
        if new_data == []:
            new_data.append(current_data[i])
            new_tag_color.append(report_tag['%i' % (current_tag[0])])
        else:
            for j in range(0,len(new_data)):
                k = False
                if float(current_data[i][row_count]) <= float(new_data[j][row_count]):
                    new_data.insert(j,current_data[i])
                    new_tag_color.insert(j,report_tag['%i' % (current_tag[i-1])])
                    k = True
                    break
            if k == False:
                new_data.append(current_data[i])
                new_tag_color.append(report_tag['%i' % (current_tag[i-1])])
    new_data.insert(0,current_data[0])
    tag_reconfigure(tb1,new_tag_color)
    tb1.assign_var(new_data)

def sortby(coordinate):
    global sort_seq_flag, sort_row_flag,current_data
    '''sort_seq_flag: 0 is raw data, 1 is from A to Z or high to low,
    2 is from Z to A low to high'''
    row_count = int(coordinate.split(',')[0])
    if row_count == sort_row_flag:
        sort_seq_flag +=1
    else:
        sort_seq_flag = 1
        sort_row_flag = row_count
    if sort_seq_flag == 3:
        sort_seq_flag = 0
    if row_count == 0:
        print('No sort!')
    else:
        if sort_seq_flag == 0:
            sortby_raw()
        if sort_seq_flag == 1:
            sortby_htl(row_count)
        if sort_seq_flag == 2:
            sortby_lth(row_count)

class BuildTable:

    def __init__(self, master,data_array):
        self.master = master
        self.data = data_array
        self.var = tktable.ArrayVar(self.master)
        self._assign_var()
        self._buildtable()

    def assign_var(self,data):
        col_count=0
        row_count=0
        for column in data:
            for row in column:
                index = "%i,%i" % (row_count,col_count)
                self.var[index] = row
                row_count+=1
            col_count+=1
            row_count=0
        j=0
        columnwidth={}
        for item in data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= len(i.title()) + 4            
                elif (len(i.title())) > columnwidth[str(j)]: 
                    columnwidth[str(j)]= len(i.title()) + 4
            j+=1
        self.tb.width(**columnwidth)
        self.tb['variable']=self.var,

    def _assign_var(self):
        col_count=0
        row_count=0
        for column in self.data:
            for row in column:
                index = "%i,%i" % (row_count,col_count)
                self.var[index] = row
                row_count+=1
            col_count+=1
            row_count=0 
        
    def _buildtable(self):
           
        self.tb = tktable.Table(self.master,
                        state='disabled',
                        rowstretch='all',
                        colstretch='none',
                        height='1',
                        rows=len(self.data[0]),
                        cols=len(self.data),
                        resizeborders='col',
                        borderwidth='0.5',
                        variable=self.var,
                        flashmode='on',
                        usecommand=0,
                        titlecols=1,
                        titlerows=1,
                        selectmode='extended',
                        selecttitle=1,
                        selecttype='cell',)
        ysb = tk.Scrollbar(self.master,orient="vertical", command=self.tb.yview_scroll)
        xsb = tk.Scrollbar(self.master,orient="horizontal", command=self.tb.xview_scroll)
        self.tb.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        ysb.pack(side='right', fill='y',in_=self.master)
        xsb.pack(side='bottom',fill='x',in_=self.master)
        # tb['variable'] = self.var
        # adjust the width for the content
        j=0
        columnwidth={}
        for item in self.data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= len(i.title()) + 4            
                elif (len(i.title())) > columnwidth[str(j)]: 
                    columnwidth[str(j)]= len(i.title()) + 4
            j+=1
        self.tb.width(**columnwidth)
        self.tb.pack(expand=1,fill='both')
        self.tb.tag_configure('sel', bg='goldenrod1')
        # popupmenu code
        self.menu = tk.Menu(self.tb, tearoff=0)
        self.menu.add_command(label="Search Related Report")
        self.menu.add_separator()
        self.menu.add_command(label="Analyze",)
        self.menu.add_separator()
        self.menu.add_command(label="Hello!")
        def popupmenu(event):
            index = self.tb.index('active')
            if self.tb.tag_includes('title',index) == True:
                offset = self.menu.yposition(3)
                self.menu.post(event.x, event.y + offset)
        self.tb.bind("<Button-2>", popupmenu)

        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####s

        def DoubleClick(event):
            global current_data
            index = self.tb.index('active') 
            if self.tb.tag_includes('title',index) == True:
                #print(2)
                sortby(index)
                     
        self.tb.bind("<Double-Button-1>",DoubleClick)


def Got_data_first_table(master,table_data):
    global tb1,gl_file_path,gl_report_num,report_tag,current_col_num
    gl_report_num +=1
    keywords=[]
    _str = 'Timing Path Group'
    findstr(gl_file_path,_str,keywords)
    # create a data matrix to build the table
    # insert the first keywords matrix
    first_column = [_str]
    for i in range(2,10):
        title = linecache.getline(gl_file_path,keywords[0]+i).split(':')[0].split(' ',2)[2]
        first_column.append(title)
    # insert the data
    data_part = []
    i = 0
    for key in keywords:
        data_part.append([])
        line = linecache.getline(gl_file_path,key).split("'",)[1]
        data_part[i].append(line)
        for count in range(2,10):
            line = linecache.getline(gl_file_path,key+count).split(':',)[1].replace(' ','').replace('\n','')
            data_part[i].append(line)
        i += 1
    # insert the data into data matrix
    table_data.append(first_column)
    col_count = []
    for item in data_part:
        table_data.append(item)
        col_count.append(len(table_data)-1)
    for item in col_count:
        report_tag['%i' % (item)] = gl_report_num
    tb1 = BuildTable(master,table_data)
    # give report1 a tag
    for j in col_count:
        index = "%i" % (j)
        tb1.tb.tag_col('Report1',index)
    tb1.tb.tag_configure('Report1',bg=report_color['1'])
    current_col_num = len(table_data)
    current_data.clear()
    current_data.extend(table_data)
    current_tag.clear()
    current_tag.extend(col_count)


def open_more_report():
    global table_data
    global gl_add_file_path
    gl_add_file_path = ''
    gl_add_file_path = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    if gl_add_file_path == '':
        print('Nothing Add!')
    else:
        Got_data_add_column(root,table_data)


def Restore_table():
    global current_col_num,table_data
    master = tb1
    master.tb['state']='normal'
    master.tb.insert_cols(current_col_num,count=len(table_data)-current_col_num)
    master.tb['state']='disabled'
    current_col_num = len(table_data)
    current_data.clear()
    current_data.extend(table_data)
    sortby_initial()

def open_file():
    global table_data
    global gl_file_path,entry1
    gl_file_path = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    bt1.pack_forget()
    Got_data_first_table(frm1,table_data)
    bt2 = tk.Button(root,text='Compare More report',command=open_more_report)
    bt2.pack()
    entry1 = tk.Entry(root)
    entry1.pack()
    entry1.insert(0,'Enter filter word')
    def filter_data(event):
        global current_data,entry1,current_col_num
        master = tb1
        filter_word = entry1.get()
        new_data = []
        new_data.append(current_data[0])
        new_tag_color = []
        col_count = []
        for i in range(1,len(current_data)):
            str_ = current_data[i][0]
            if str_.find(filter_word) != -1:
                new_data.append(current_data[i])
                col_count.append(i)
                new_tag_color.append(report_tag['%i' % (i)])
        if new_data == []:
            print('Nothing')
        else:
            master.tb['state']='normal'
            master.tb.delete_cols(len(new_data),count=current_col_num-len(new_data))
            master.tb['state']='disabled'
            tag_reconfigure(master,new_tag_color)
            master.assign_var(new_data)
            current_col_num = len(new_data)
            current_data.clear()
            current_data.extend(new_data)
            current_tag.clear()
            current_tag.extend(col_count)
    entry1.bind('<KeyPress-Return>',filter_data)
    def Entry1_Callback(event):
        entry1.selection_range(0,'end')
    entry1.bind("<FocusIn>", Entry1_Callback)
    bt3 = tk.Button(root,text='Back',command=Restore_table)
    bt3.pack()

def Got_data_add_column(master,table_data):
    global tb1,gl_add_file_path,gl_report_num,report_tag,current_col_num
    gl_report_num +=1
    keywords=[]
    _str = 'Timing Path Group'
    findstr(gl_add_file_path,_str,keywords)
    # create a data matrix to build the table
    # insert the first keywords matrix
    data_part = []
    i = 0
    for key in keywords:
        data_part.append([])
        line = linecache.getline(gl_add_file_path,key).split("'",)[1]
        data_part[i].append(line)
        for count in range(2,10):
            line = linecache.getline(gl_add_file_path,key+count).split(':',)[1].replace(' ','').replace('\n','')
            data_part[i].append(line)
        i += 1
    # insert the data into data matrix
    col_count = []
    for item in data_part:
        table_data.append(item)
        col_count.append(len(table_data)-1)
        current_col_num+=1
    for item in col_count:
        report_tag['%i' % (item)] = gl_report_num
    tb1.tb['state'] = 'normal'
    tb1.tb.insert_cols('end',len(data_part))
    tb1.tb['state'] = 'disabled'
    j=0
    columnwidth={}
    for item in table_data:
        for i in item:
            if (str(j) in columnwidth) == False:
                columnwidth[str(j)]= len(i.title()) + 4            
            elif (len(i.title())) > columnwidth[str(j)]: 
                columnwidth[str(j)]= len(i.title()) + 4
        j+=1
    tb1.tb.width(**columnwidth)
    tb1.assign_var(table_data)
    current_data.clear()
    current_data.extend(table_data)
    current_tag.extend(col_count)
    # give report1 a tag
    for i in col_count:
        index = "%i" % (i)
        tb1.tb.tag_col('Report%i' % (gl_report_num),index)
    tb1.tb.tag_configure('Report%i' % (gl_report_num),bg=report_color['%i' % (gl_report_num)])


root = tk.Tk()
root.geometry('600x400')  
root.minsize(600, 300)
root.title('DC Analysis')
bt1 = tk.Button(root,text='Open File',command=open_file)
bt1.pack()
frm1 = tk.Frame(root)
frm1.pack(fill='both',expand=1)
#tb1.tb.insert_rows('end',1)
root.mainloop()


#Fix the sort function in filter mode
# right click menu
