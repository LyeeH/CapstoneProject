# week 2 example
# show different data in two table and highlight them
# or highlight specific content

import tkinter as tk
import tktable
import xlrd
from tkinter import ttk
gl_file_path = 'demo1.xlsx'

root = tk.Tk()
root.geometry('800x600')
root.title('Digital Analysis')
root.resizable(width=False,height=False)

def read_excel():
    global gl_file_path
    global Header_1, List_1,Header_2,List_2
    Header_1 = []
    Header_2 = []
    List_1 = []
    List_2 = []
    # 打开文件
    workbook = xlrd.open_workbook(gl_file_path)
    # get all the sheet name
    # print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
    sheet1 = workbook.sheet_by_index(0)  # sheet index is begin with 0
    sheet1 = workbook.sheet_by_name('sheet1')
    # print(sheet1.name,sheet1.nrows,sheet1.ncols)
    Header_1 = sheet1.col_values(0)
    Header_2 = Header_1
    # for i in range(1, sheet1.ncols):
    for i in range(1, 3):
        List_1.append(sheet1.col_values(i))
    for i in range(3, 5):
        List_2.append(sheet1.col_values(i))

class BuildTable:

    def __init__(self, master,title_column,data):
        self.var = tktable.ArrayVar(master)

        self.num_cols = 1 + len(data)
        self.num_rows = len(title_column)

        row_count=0
        col_count=0
        #SETTING COLUMNS
        for row in title_column:
            index = "%i,%i" % (row_count,col_count)
            self.var[index] = row
            row_count+=1
        col_count=1
        row_count=0
        #SETTING DATA IN ROWS
        for col in data:
            for item in col:
                #print(item)
                index = "%i,%i" % (row_count,col_count)
                ## PLACING THE VALUE IN THE INDEX CELL POSITION ##
                self.var[index] = item
                #### IGNORE THIS IF YOU WANT, JUST SETTING SOME CELL COLOR ####
                ''' try:
                    if int(item) > 999:
                        tb.tag_cell('green',index)
                except:
                    pass'''
                ###############################################################
                row_count+=1       
            row_count=0
            col_count+=1
        #### ABOVE CODE SETS THE DOG INTO THE TABLE ####

        self.tb = tktable.Table(master,
                        state='disabled',
                        rowstretch='all',
                        colstretch='all',
                        height='1',
                        rows=self.num_rows,
                        cols=self.num_cols,
                        resizeborders='col',
                        borderwidth='0.5',
                        variable=self.var,
                        flashmode='on',
                        usecommand=0,
                        titlerows=1,
                        titlecols=1,)
        # columns0 = ['Timing Path Group', 'Levels of Logic', 'Critical Path Length', 'Critical Path Slack', 'Critical Path Clk Period', 'Total Negative Slack', 'No. of Violating Paths', 'Worst Hold Violation', 'Total Hold Violation', 'No. of Hold Violations']
        #### LIST OF LISTS DEFINING THE ROWS AND VALUES IN THOSE ROWS ####
        # values = [['INPUTS', '1.000', '0.238', '0.643', '1.000', '0.000', '0.000', '0.000', '0.000', '0.000'], ['OUTPUTS', '1.000', '0.108', '0.292', '0.500', '0.000', '0.000', '0.000', '0.000', '0.000'], ['rclk', '7.000', '0.543', '-0.066', '0.500', '-0.106', '2.000', '0.000', '0.000', '0.000'], ['wclk', '5.000', '0.946', '0.035', '1.000', '0.000', '0.000', '0.000', '0.000', '0.000']]
        #### SETS THE DOGS INTO THE TABLE ####
        #### VVVVVVVVVVVVVVVVVVVVVVVVVVV ####
        #DEFINING THE VAR TO USE AS DATA IN TABLE
        ################################################
        #### VARIABLE PARAMETER SET BELOW ON THE 'TB' USES THE DATA DEFINED ABOVE ####
        ysb = tk.Scrollbar(master,orient="vertical", command=self.tb.yview_scroll)
        xsb = tk.Scrollbar(master,orient="horizontal", command=self.tb.xview_scroll)
        self.tb.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        ysb.pack(side='right', fill='y',in_=master)
        xsb.pack(side='bottom',fill='x',in_=master)
        # tb['variable'] = self.var
        # adjust the width for the content
        j=1
        columnwidth={}
        for item in data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= len(i.title())            
                elif (len(i.title())) > columnwidth[str(j)]: 
                    columnwidth[str(j)]= len(i.title())
            j+=1
        for item in title_column:
            if (str(0) in columnwidth) == False:
                columnwidth[str(0)]= len(item.title())            
            elif (len(item.title())) > columnwidth[str(0)]: 
                columnwidth[str(0)]= len(item.title())
        self.tb.width(**columnwidth)
        #for col in columns:
        #   tb.columnconfigure(col, width=tkFont.Font().measure(col.title()))
        #   tb.columnconfigure(col, width=tkFont.Font().measure(col.title()))
        self.tb.pack(expand=1,fill='both')
        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####

# a sign label
tk.Label(root,text='DC Analysis',font=('Arial',24),bg='red',height=3).pack(side='top',fill='both')
# top frame and bottom frame
frm_t = tk.Frame(root)
frm_t.pack(side='top',fill='both',expand=1)
frm_b = tk.Frame(root,height=100)
frm_b.pack(side='bottom',fill='x')
frm_b.pack_propagate(0)
frm_b.grid_propagate(0)
frm1 = tk.Frame(frm_t)
frm1.pack(side='left',fill='both',expand=1)
frm2 = tk.Frame(frm_t)
frm2.pack(side='right',fill='both',expand=1)
frm1.pack_propagate(0)
frm2.pack_propagate(0)


def HighlightContent(master):
    master.tb.tag_configure('green', background=None)
    master.tb.tag_delete('green')
    master.tb.tag_configure('pink', background=None)
    master.tb.tag_delete('pink')
    highlight = param_entry.get()
    # cb and param_entry may need to be golbal variable if move to another file
    if cb.get()=='above':
        col_count=1
        row_count=1
        for col in range(1,master.num_cols):
            for row in range(1,master.num_rows):
                index = "%i,%i" % (row_count,col_count)
                try: 
                    if float(master.var[index]) > float(highlight):
                        master.tb.tag_cell('green',index)
                except:
                    pass
                row_count+=1
            row_count=1
            col_count+=1
        master.tb.tag_configure('green', background='green')
    # cb may need to be golbal variable if move to another file
    if cb.get()=='below':
        col_count=1
        row_count=1
        for col in range(1,master.num_cols):
            for row in range(1,master.num_rows):
                index = "%i,%i" % (row_count,col_count)
                try: 
                    if float(master.var[index]) < float(highlight):
                        master.tb.tag_cell('pink',index)
                except:
                    pass
                row_count+=1
            row_count=1
            col_count+=1
        master.tb.tag_configure('pink', background='pink')

def bt_getparam_func(master1,master2):
    HighlightContent(master1)
    HighlightContent(master2)

Showdifferent_flag = True
def Showdifferent(master1,master2):
    global Showdifferent_flag
    if Showdifferent_flag == False:
        master1.tb.tag_configure('blue', background=None)
        master1.tb.tag_delete('blue')
        master2.tb.tag_configure('blue', background=None)
        master2.tb.tag_delete('blue')
        Showdifferent_flag = True
    else:
        col_count=1
        row_count=1
        for col in range(1,master1.num_cols):
            for row in range(1,master1.num_rows):
                index = "%i,%i" % (row_count,col_count)
                try: 
                    if float(master1.var[index]) != float(master2.var[index]):
                        master1.tb.tag_cell('blue',index)
                        master2.tb.tag_cell('blue',index)
                except:
                    pass
                row_count+=1
            row_count=1
            col_count+=1
        master1.tb.tag_configure('blue', background='blue')   
        master2.tb.tag_configure('blue', background='blue') 
        Showdifferent_flag = False              
# weight in bottom frame

frm_b1 = tk.Frame(frm_b)
frm_b1.pack(side='top',fill='x')
frm_b2 = tk.Frame(frm_b)
frm_b2.pack()
frm_b3 = tk.Frame(frm_b)
frm_b3.pack(fill='x')
frm_b4 = tk.Frame(frm_b)
frm_b4.pack()
param_entry = tk.Entry(frm_b2,width=10)
param_entry.pack(side='left',padx=10)
choose_list = tk.StringVar()
cb = ttk.Combobox(frm_b2,width=12, state='readonly',textvariable=choose_list,value=('above','below'),foreground='red')
cb.pack(side='left',padx=10)
cb.current(0)    # set the default showup information, 0 is the beginning
bt_getparam = tk.Button(frm_b2,text='Highlight Content',command=lambda:bt_getparam_func(tb1,tb2))
bt_getparam.pack(side='bottom',padx=10)
tk.Label(frm_b1,text="Enter a number, then choose 'below' or 'above', click right side button",bg='yellow').pack(expand=1,fill='x')
tk.Label(frm_b3,text="Or compare table content and blue the differnt",bg='yellow').pack(fill='x')
bt_compare = tk.Button(frm_b3,text='Comapre different',command=lambda:Showdifferent(tb1,tb2))
bt_compare.pack(side='top')

read_excel()
print(Header_1)
print(List_1)
tb1 = BuildTable(frm1,Header_1,List_1)
tb2 = BuildTable(frm2,Header_2,List_2)
#table_test(frm2,Header_2ss,List_2)
#table_test1(frm2,Header_2,List_2)

root.mainloop()