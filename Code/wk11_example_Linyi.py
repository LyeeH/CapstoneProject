import pandas as pd
import linecache
import numpy as np
import tkinter as tk
from tkinter import ttk
import tktable
import re

filepath = '/Users/Felix/Desktop/QORs_Detailed_Timing_Report.txt'
sortflag = 0

file = open(filepath,'r+')

file_read = file.read()
report_names = re.findall(r'Startpoint\: ([a-z].*)(?:.*\n)*?.*Endpoint\: ([a-z].*)(?:.*\n)*?.*Path Group\: ([a-zA-Z0-9].*)(?:.*\n)*?.*slack \([A-Z]*\).*?([[0-9].*)',file_read)
report_details = re.findall(r'(.*Startpoint\: [a-z].*(?:.*\n)*?.*Endpoint\: [a-z].*(?:.*\n)*?.*Path Group\: [a-zA-Z0-9].*(?:.*\n)*?.*slack \([A-Z]*\).*?[[0-9].*)',file_read)

# print(table_content)
# print(len(table_content))
# print(table_content[0])

report_names_list = []
for item in report_names:
    report_names_list.append(list(item))

for item in report_names_list:
    item[0] = item[0].split('(')[0].replace(' ','')
    item[1] = item[1].split('(')[0].replace(' ','')
df = pd.DataFrame(report_names_list,columns=['Startpoint','Endpoint','Path Group','Timing Slack'])

def table_raw_data(dataframe):
    data = dataframe.tolist()
    return data

# x=[]
# for j in _str[2]:
#     x.append(j.replace('[','\[').replace(']','\]').replace('(','\(').replace(')','\)'))
# print(_str[2])
# print(x)
# print(x[0])
# _str1 = re.finditer(r'(Startpoint\: %s.*(?:\n.*){0,3}.*Endpoint\: %s.*(?:\n.*){0,3}.*Path Group\: %s.*(?:\n.*){0,40}.*slack \(MET\).*)' % (x[0],x[1],x[2]),lines,re.M)
# i=0
# for item in _str1:
#     print(1)
#     print(item.group()) 
#     i+=1
# print(i)


class Build_report_names:

    def __init__(self,master,dataframe):
        self.master = master
        self.masterframe = tk.Frame(master)
        self.var = tktable.ArrayVar(self.masterframe)
        self.showflag = 0
        self.sortflag = 0
        self.detail_flag = False
        self.raw_df = dataframe.copy()
        self.cur_df = dataframe.copy()
        self.data = self.to_table(self.cur_df)
        self._assign_var()
        self._build_table(master)
        self.masterframe.pack(expand=1,fill='both',side='top')

    def to_table(self,dataframe,first_add=0):
        # def color_tag(master,index,report_num):
        #     global report_color
        #     master.Table.tag_cell(report_num,'0,%i' % (index))
        table_data = []
        if(first_add):
        # color tag debug part (adjust the cols and rows number when add table)
            self.Table['state']='normal'
            self.Table['cols']=len(dataframe.columns.tolist())+1
            self.Table['rows']=len(dataframe.index.tolist())+1
            self.Table['state']='disabled'
        i = 0
        for item in dataframe.columns.tolist():
            table_data.append(dataframe[item].tolist())
            table_data[i].insert(0,item)
            i+=1
            # print(table_data)
        return table_data

    def assign_var(self,dataframe):
        self.cur_df = dataframe.copy()
        data = self.to_table(self.cur_df)
        # Change table cols&rows number to fit the data
        self.Table['state']='normal'
        self.Table['cols']=len(data)
        self.Table['rows']=len(data[0])
        self.Table['state']='disabled'
        col_count=0
        row_count=0
        for column in data:
            for row in column:
                index = "%i,%i" % (row_count,col_count)
                self.var[index] = row
                row_count+=1
            col_count+=1
            row_count=0
        j = 0
        columnwidth={}
        for item in data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= 10  
                elif (len(i.title())) > columnwidth[str(j)]:                   
                    columnwidth[str(j)]= len(i.title())
            j+=1
        self.Table.width(**columnwidth)
        self.Table['variable']=self.var


    def sortdata(self,index):
        def sortby(self,index):
            # index = 1 -> axis = 1 -> dataframe's index
            # index = 0 -> axis = 0 -> dataframe's values(first row) 
            if self.sortflag == 2:
                self.sortflag = 0
            if self.sortflag == 0:
                self.cur_df.sort_values(by=[_str],axis=index,inplace=True)
                self.sortflag+=1
            elif self.sortflag == 1:
                self.cur_df.sort_values(by=[_str],axis=index, ascending=False, inplace=True)
                self.sortflag+=1
            # print(cur_df)
            # print(cur_tabledata)s
            self.assign_var(self.cur_df)

        index_x = int(index.split(',')[0])
        index_y = int(index.split(',')[1])       
        _str = self.cur_df.columns.tolist()[index_y]
        sortby(self,0)

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

    def _build_table(self,master):        
        self.Table = tktable.Table(self.masterframe,
                        state='disabled',
                        rowstretch='all',
                        colstretch='all',
                        height='1',
                        rows=len(self.data[0]),
                        cols=len(self.data),
                        # resizeborders='col',
                        borderwidth='1',
                        variable=self.var,
                        usecommand=0,
                        titlerows=1,
                        # selectmode='extended',
                        selecttitle=1,
                        selecttype='row',)
        ysb = tk.Scrollbar(self.masterframe,orient="vertical", command=self.Table.yview_scroll)
        xsb = tk.Scrollbar(self.masterframe,orient="horizontal", command=self.Table.xview_scroll)
        self.Table.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        ysb.pack(side='right', fill='y',in_=self.masterframe)
        xsb.pack(side='bottom',fill='x',in_=self.masterframe)
        j=0
        columnwidth={}
        for item in self.data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= 10      
                elif (len(i.title())) > columnwidth[str(j)]: 
                    columnwidth[str(j)]= len(i.title())
            j+=1
        # self.Table.delete_rows(1,count=1)
        # self.Table['state']='disabled'
        self.Table.width(**columnwidth)
        self.Table.pack(expand=1,fill='both')
        self.Table.tag_configure('sel', bg='goldenrod1')

        # # popupmenu code
        # self.menu = tk.Menu(self.Table, tearoff=0)
        # self.menu.add_command(label="Search Related Report")
        # self.menu.add_separator()
        # self.menu.add_command(label="Analyze",)
        # self.menu.add_separator()
        # self.menu.add_command(label="Hello!")

        # def popupmenu(event):
        #     index = self.Table.index('active')
        #     if self.Table.tag_includes('title',index) == True:
        #         # offset = self.menu.yposition(3)
        #         self.menu.post(event.x_root, event.y_root)
        # self.Table.bind("<Button-2>", popupmenu)

        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####s

        def DoubleClick(event):
            global report_names
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                self.sortdata(index)
            else:
                index_x = int(index.split(',')[0]) 
                # print(index_x)
                index = self.cur_df.index.tolist()[index_x-1]
                keyword_raw = self.cur_df.ix[(index)].tolist()
                keyword = []
                for item in keyword_raw:
                    keyword.append(item.replace('[','\[').replace(']','\]'))
                for item in report_details:
                    content = re.match(r'(.*Startpoint\: %s.*(?:.*\n)*?.*Endpoint\: %s.*(?:.*\n)*?.*Path Group\: %s.*(?:.*\n)*?.*slack \([A-Z]*\).*?%s.*)' % (keyword[0],keyword[1],keyword[2],keyword[3]),item)
                    if content != None:
                        _str = content.group()
                        print(_str)
                        break
                if self.detail_flag == False:
                    self.Table_details = Build_report_details(self.master,_str)
                    self.detail_flag =True
                elif self.detail_flag == True:
                    self.Table_details.update_content(_str)

        self.Table.bind("<Double-Button-1>",DoubleClick)

class Build_report_details:

    def __init__(self,master,report_details):
        self.master = master
        self.masterframe = tk.Frame(master)
        self.tableframe = tk.Frame(self.masterframe)
        self.var = tktable.ArrayVar(self.tableframe)
        self._str_path_detail_t = tk.StringVar()
        self.text_box_t = tk.Label(self.masterframe,textvariable=self._str_path_detail_t,justify='left',anchor='w')
        self._str_path_detail_b = tk.StringVar()
        self.text_box_b = tk.Label(self.masterframe,textvariable=self._str_path_detail_b,justify='left',anchor='w')
        self.showflag = 0
        self.sortflag = 0
        self.convert_details(report_details)
        self.raw_df = self.cur_df.copy()
        self.data = self.to_table(self.cur_df)
        self._assign_var()
        self._build_table()
        self.text_box_t.pack(side='top')
        self.text_box_b.pack(side='bottom')
        self.tableframe.pack(side='bottom',after=self.text_box_b,expand=1,fill='both')
        self.masterframe.pack(expand=1,fill='both',side='bottom')

    def to_table(self,dataframe,first_add=0):
        # def color_tag(master,index,report_num):
        #     global report_color
        #     master.Table.tag_cell(report_num,'0,%i' % (index))
        table_data = []
        if(first_add):
        # color tag debug part (adjust the cols and rows number when add table)
            self.Table['state']='normal'
            self.Table['cols']=len(dataframe.columns.tolist())+1
            self.Table['rows']=len(dataframe.index.tolist())+1
            self.Table['state']='disabled'
        i = 0
        table_data = []
        table_data.append(dataframe.index.tolist())
        table_data[0].insert(0,'Point')
        i = 1
        for item in dataframe.columns.tolist():
            table_data.append(dataframe[item].tolist())
            table_data[i].insert(0,item)
            i+=1
        print(table_data)
        return table_data

    def assign_var(self,dataframe):
        self.cur_df = dataframe.copy()
        data = self.to_table(self.cur_df)
        # Change table cols&rows number to fit the data
        self.Table['state']='normal'
        self.Table['cols']=len(data)
        self.Table['rows']=len(data[0])
        self.Table['state']='disabled'
        col_count=0
        row_count=0
        for column in data:
            for row in column:
                index = "%i,%i" % (row_count,col_count)
                self.var[index] = row
                row_count+=1
            col_count+=1
            row_count=0
        j = 0
        columnwidth={}
        for item in data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= 10  
                elif (len(i.title())) > columnwidth[str(j)]:                   
                    columnwidth[str(j)]= len(i.title())
            j+=1
        self.Table.width(**columnwidth)
        self.Table['variable']=self.var

    def sortdata(self,index):
        def sortby(self,index):
            # index = 1 -> axis = 1 -> dataframe's index
            # index = 0 -> axis = 0 -> dataframe's values(first row) 
            if self.sortflag == 2:
                self.sortflag = 0
            if self.sortflag == 0:
                if index == 0:
                    self.cur_df.sort_index(inplace=True)
                else:
                    self.cur_df.sort_values(by=[_str],axis=0,inplace=True)
                self.sortflag+=1
            elif self.sortflag == 1:
                if index == 0:
                    self.cur_df.sort_index(ascending=False,inplace=True)
                else:
                    self.cur_df.sort_values(by=[_str],axis=0, ascending=False, inplace=True)
                self.sortflag+=1
            # print(cur_df)
            # print(cur_tabledata)s
            self.assign_var(self.cur_df)

        index_x = int(index.split(',')[0])
        index_y = int(index.split(',')[1])      
        _str = self.cur_df.columns.tolist()[index_y-1]
        sortby(self,index_y)

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
        
    def convert_details(self,report_details):
        self.details = report_details
        _str = re.match(r'(.*Startpoint: (?:.*\n)*?)(.*Endpoint: (?:.*\n)*?)(.*Path Group: (?:.*\n)*?)\n.*Point \s*Cap',self.details)
        self._str_path_detail_t.set('%s'%(re.sub(r'\s*\n\s+',r' ',_str.group(1))+re.sub(r'\s*\n\s+',r' ',_str.group(2))+_str.group(3)))
        _str = re.search(r'-{5,}\n(.*data required time(?:.*\n)*?.+?-{5,}\n.*slack \([A-Z]*\).*)',self.details)
        self._str_path_detail_b.set('%s'%(_str.group(1)))
        _str = re.search(r'.*Point \s*Cap.*\n.*\n((?:.*\n)*?).*?-{5,}',self.details)
        # path_names = []
        # for line in _str.group(1).split('\n'):
        #     print(line,end='\n\n')
        # use re.sub here since there are some cases the path name is too long to fit in the same row with the data
        path_names = re.findall(r'.*?([a-zA-Z]{2,}.*?)\s\s+',re.sub(r'(.*?[a-zA-Z]{2,}.*?)(\))(\n)',r'\1)  \3',_str.group(1)))
        fillin_data = []
        for line in _str.group(1).split('\n'):
            data = re.findall(r'([0-9]*\.[0-9]+)\s?([rf]?)',line)
            if data !=[]: 
                fillin_data.append(data)
        table_data = []
        for item in path_names:
            table_data.append([item])
        i = 0
        for item in fillin_data:
            for j in range(0,4-len(item)):
                table_data[i].append('')
            for value in item:
                table_data[i].append(value[0]+value[1])
            i += 1
        dataframe1 = pd.DataFrame(table_data,columns=('Point','Cap','Trans','Incr','Path'))
        dataframe1.set_index('Point',inplace=True)
        self.cur_df = dataframe1.copy()

    def update_content(self,details):
        self.convert_details(details)
        self.data = self.to_table(self.cur_df)
        self._assign_var()
        self.Table['variable']=self.var

    def _build_table(self):
           
        self.Table = tktable.Table(self.tableframe,
                        state='disabled',
                        rowstretch='all',
                        colstretch='all',
                        height='1',
                        rows=len(self.data[0]),
                        cols=len(self.data),
                        # resizeborders='col',
                        borderwidth='1',
                        variable=self.var,
                        usecommand=0,
                        titlerows=1,
                        # selectmode='extended',
                        selecttitle=1,
                        selecttype='row',)
        ysb = tk.Scrollbar(self.tableframe,orient="vertical", command=self.Table.yview_scroll)
        xsb = tk.Scrollbar(self.tableframe,orient="horizontal", command=self.Table.xview_scroll)
        self.Table.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        ysb.pack(side='right', fill='y',in_=self.tableframe)
        xsb.pack(side='bottom',fill='x',in_=self.tableframe)
        j=0
        columnwidth={}
        for item in self.data:
            for i in item:
                if (str(j) in columnwidth) == False:
                    columnwidth[str(j)]= 10      
                elif (len(i.title())) > columnwidth[str(j)]: 
                    columnwidth[str(j)]= len(i.title())
            j+=1
        # self.Table.delete_rows(1,count=1)
        # self.Table['state']='disabled'
        self.Table.width(**columnwidth)
        self.Table.pack(expand=1,fill='both')
        self.Table.tag_configure('sel', bg='goldenrod1')

        # # popupmenu code
        # self.menu = tk.Menu(self.Table, tearoff=0)
        # self.menu.add_command(label="Search Related Report")
        # self.menu.add_separator()
        # self.menu.add_command(label="Analyze",)
        # self.menu.add_separator()
        # self.menu.add_command(label="Hello!")

        # def popupmenu(event):
        #     index = self.Table.index('active')
        #     if self.Table.tag_includes('title',index) == True:
        #         # offset = self.menu.yposition(3)
        #         self.menu.post(event.x_root, event.y_root)
        # self.Table.bind("<Button-2>", popupmenu)

        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####s

        def DoubleClick(event):
            global report_names
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                self.sortdata(index)
            else:
                index_x = int(index.split(',')[0]) 
                # print(index_x)
                index = self.cur_df.index.tolist()[index_x-1]
                keyword_raw = self.cur_df.ix[(index)].tolist()
                keyword = []
                for item in keyword_raw:
                    keyword.append(item.replace('[','\[').replace(']','\]'))
                for item in report_details:
                    content = re.match(r'(.*Startpoint\: %s.*(?:.*\n)*?.*Endpoint\: %s.*(?:.*\n)*?.*Path Group\: %s.*(?:.*\n)*?.*slack \([A-Z]*\).*?%s.*)' % (keyword[0],keyword[1],keyword[2],keyword[3]),item)
                    if content != None:
                        _str = content.group()
                

        self.Table.bind("<Double-Button-1>",DoubleClick)


root = tk.Tk()
root.geometry('600x800')
root.minsize(600,600)
root.title('DC Analysis')

tb = Build_report_names(root,df)





root.mainloop()