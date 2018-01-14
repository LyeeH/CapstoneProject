# This code is a simple example showing how to use tkinter
# Including locate the file, write and read excel, build Menubar, and build a table by Treeview

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import xlrd
import xlwt
import os
import sys
import linecache
import tkinter.font as tkFont
import tkinter.ttk as ttk
# Global Variable
gl_Mode = 0
global root

def get_file_path(entry):
    open_file = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    entry.delete(0,tk.END)
    entry.insert(0,open_file)

def findstr(file, str,record):
    # f = open(file, "r+")
    # if f.read().find(str) != -1:
    #     s = os.getcwd() + "\\" + file
    # else:
    #     s = "None"
    # f.close()
    i = 1
    global s

    for line in open(file):
            # return is index of the str start position.
        if line.find(str) != -1:
            s = os.getcwd() + '\\' + file + "------>line:%d" % (i)
            #print(s)
            record.append(i)
        i = i + 1
    return s

def set_style(name,height,bold=False):
  style = xlwt.XFStyle() # Format Initialization
 
  font = xlwt.Font()
  font.name = name
  font.bold = bold
  font.color_index = 4
  font.height = height
 
  # borders= xlwt.Borders()
  # borders.left= 6
  # borders.right= 6
  # borders.top= 6
  # borders.bottom= 6
 
  style.font = font
  # style.borders = borders
 
  return style

def write_excel(path):
    global read_file_path
    global column
    # only works for Timing Path Group
    keywords = []
    filepath = path
    _str = 'Timing Path Group'
    findstr(filepath,_str,keywords)
    row0 = ['Timing Path Group',]
    column0 = ['Levels of Logic','Critical Path Length','Critical Path Slack','Critical Path Clk Period','Total Negative Slack','No. of Violating Paths','Worst Hold Violation','Total Hold Violation','No. of Hold Violations']
    b = 0
    column=[]
    for i in keywords:
        the_line = linecache.getline(filepath,i)
        x = [str(i) for i in the_line.split("'")]
        row0.append(x[1])
        column.append([])
        for j in range(2,11):
            the_line = linecache.getline(filepath,i+j)
            new_line = the_line.replace(" ","").replace("\n","").strip()
            y = [str(i) for i in new_line.split(':')]
            column[b].append(y[1])
        b += 1
    # create a workbook
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # create sheet
    # create the first row
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Arial', 220, True))
    # create the first column
    i = 0
    while i < len(column0):
        sheet1.write(i+1,0,column0[i])
        i += 1
    # fill in all the content
    j = 0
    k = 0
    while j < len(column):
        while k < len(column[j]):
            sheet1.write(k+1,j+1,column[j][k])
            k += 1
        j += 1
        k = 0
    read_file_path = 'demo1.xlsx'
    f.save(read_file_path) # save the workbook

def read_excel():
    global Header_, List_
    List_ = []
    # 打开文件
    workbook = xlrd.open_workbook(read_file_path)
    # get all the sheet name
    # print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
    sheet1 = workbook.sheet_by_index(0)  # sheet index is begin with 0
    sheet1 = workbook.sheet_by_name('sheet1')
    # print(sheet1.name,sheet1.nrows,sheet1.ncols)
    Header_ = sheet1.col_values(0)
    for i in range(1, sheet1.ncols):
        List_.append(sheet1.col_values(i))

class BuildTable(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self,frm, element_header, element_list):
        self.element_header = element_header
        self.element_list = element_list
        self.tree = None
        self.frame = frm
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        container = ttk.Frame(self.frame, height=400, width=800)
        container.pack(fill='both', expand=True)
        # create a treeview with scrollbar
        self.tree = ttk.Treeview(self.frame,columns=self.element_header, show="headings")
        ysb = ttk.Scrollbar(self.frame,orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame,orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        ysb.grid(column=1, row=0, sticky='ns', in_=container)
        xsb.grid(column=0, row=1, sticky='nsew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.tree.bind("<Double-Button-1>", self.OnClick)

    def _build_tree(self):
        for col in self.element_header:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        for item in self.element_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.element_header[ix], width=None) < col_w:
                    self.tree.column(self.element_header[ix], width=col_w)

    def OnClick(self, event):
        row = self.tree.identify_row(event.y)
        vals = self.tree.item(row, 'values')
        print(vals)
        #global return_index
        #item = self.tree.identify('item',event.x,event.y)
        # print(str(item))
        #return_index = (int((item[1:4]),16) - 1)
        # print(str(return_index))
        # reload_tree(return_index,self)

def isnumeric(s):
    """test if a string is numeric"""
    for c in s:
        if c in "1234567890-.":
            numeric = True
        else:
            return False
    return numeric

def change_numeric(data):
    """if the data to be sorted is numeric change to float"""
    new_data = []
    if isnumeric(data[0][0]):
        # change child to a float
        for child, col in data:
            new_data.append((float(child), col))
            # float(child.split('-')[0]
        return new_data
    return data

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    data = change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so that it will sort in the opposite direction
    tree.heading(col,
                 command=lambda col=col: sortby(tree, col, int(not descending)))

def newwindow():
    # m0_entry here may change to a pass variable
    file_path = m0_entry.get()
    print(file_path)
    write_excel(file_path)
    read_excel()
    root1 = tk.Toplevel()
    root1.geometry('600x400')
    tk.Label(root1,text='ANALYSIS',bg='red',font=('Arial',30),height=3).pack(fill='both')
    # BuildTable(Header_, List_)
    frm1 = tk.Frame(root1, height=150)
    frm1.pack(fill='x')
    frm1.pack_propagate(0)
    BuildTable(frm1, Header_, List_)
    tk.Label(root1, text='ANALYSIS', bg='red',font=('Arial', 30),).place(x=0, y=300)

def New_window(file_path):
    write_excel(file_path)
    read_excel()
    root1 = tk.Toplevel()
    root1.geometry('600x400')
    tk.Label(root1,text='ANALYSIS',bg='red',font=('Arial',30),height=3).pack(fill='both')
    # BuildTable(Header_, List_)
    frm1 = tk.Frame(root1, height=150)
    frm1.pack(fill='x')
    frm1.pack_propagate(0)
    BuildTable(frm1, Header_, List_)
    tk.Label(root1, text='ANALYSIS', bg='red',font=('Arial', 30),).place(x=0, y=300)

def do_job():
    f = 1

# main window build
root = tk.Tk()
root.title('DC analyser')
root.geometry('600x200')
root.resizable(width=False,height=False)
m0_canvas = tk.Canvas(root,width='600', height='200',bg='grey', highlightthickness=0,)
m0_canvas.place(x=0, y=0, anchor='nw')      
m0_label = tk.Label(root, text='Welcome to DC Anlayser.\n Entry file path below or\n Click File to add a new document.', font=(
    'Arial', 22), bg='grey')
m0_label.place(x=300, y=80, anchor='center')
m0_entry = tk.Entry(root,text=None,bg='grey',highlightthickness=0,width=40)
m0_entry.place(x=220,y=150,anchor='center')
m0_entry.insert(0,'Please enter the file path here')
m0_button1 = tk.Button(root,text='Browser',bg='grey',highlightthickness=0,command=lambda : get_file_path(m0_entry))
m0_button1.place(x=480,y=150,anchor='e')
#m0_button = tk.Button(root, text='translate the file',command=lambda: translate()).pack()
m0_button2 = tk.Button(root,text='Analysis',bg='grey',highlightthickness=0,command=newwindow)
m0_button2.place(x=570,y=150,anchor='e')

def New_():
    # opne a file dialog window
    open_file = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    New_window(open_file)
    # lb1 = tk.Button(mainfrm,text='File Location',width=20,command=file_location,) #lb = Location Button
    # lb1.place(x=10,y=10,anchor='nw')

def Menubar():
    # Menubar
    menubar = tk.Menu()
    filemenu = tk.Menu(menubar, tearoff=0)
    # what is tear off
    menubar.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New', command=lambda: New_())
    filemenu.add_command(label='Open', command=do_job)
    filemenu.add_command(label='Save', command=do_job)
    # submenu1
    submenu = tk.Menu(filemenu)
    filemenu.add_cascade(label='Import', menu=submenu, underline=0)
    submenu.add_command(label='Submenu1', command=do_job)
    # submenu1 end
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    editmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=editmenu)
    editmenu.add_command(label='Cut', command=do_job)
    editmenu.add_command(label='Copy', command=do_job)
    editmenu.add_command(label='Paste', command=do_job)

    # add the meunbar to mainwindow
    root.config(menu=menubar)

Menubar()
root.mainloop()
