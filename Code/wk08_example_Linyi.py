import pandas as pd
import linecache
import numpy as np
import tkinter as tk
from tkinter import ttk
import tktable

# to run the code successfuly, you need to change the file path here
# this is easy for testing, but will add openfile window later
filepath = '/Users/Felix/Desktop/QOR_Report_File.txt'
add_filepath = '/Users/Felix/Desktop/QOR_Report_File_2.txt'
# to run the code successfuly, you need to change the file path here

_str = 'Timing Path Group'
sortflag = 0
num_report = 0
report_color = {'Report1':'DarkOrange2','Report2':'medium aquamarine','Report3':'pink2','Report4':'PaleGreen4'}

def findstr(file, str):

    f = open(file, "r+")
    record = []
    i = 1
    for line in f:
        if line.find(str) != -1:
            # print(linecache.getline(gl_file_path,i+1))
            # print(f.next())
            record.append(i)
        i = i + 1
    return(record)

def Get_dataframe(path):
    global  _str, num_report
    # Set a error or false detect if openfile is turn false, otherwise 
    # num_report+=1
    num_report += 1
    keywords = findstr(path, _str)
    Data = {_str:[]}
    for i in range(2, 10):
        title = linecache.getline(
            path, keywords[0] + i).split(':')[0].split(' ', 2)[2]
        Data[_str].append(title)
    # insert the data
    i = 0
    level = [['Report%i' % (num_report)],[]]
    # label = [[],[]]
    for key in keywords:
        title = linecache.getline(path, key).split("'",)[1]
        level[1].append(title)
        # label[0].append(num_report-1)
        # label[1].append(i)
        Data[title] = []
        for count in range(2, 10):
            content = linecache.getline(
                path, key + count).split(':',)[1].replace(' ', '').replace('\n', '')
            Data[title].append(content)
        i += 1

    temporary_df = pd.DataFrame(Data)
    temporary_df.set_index(_str,inplace=True)
    headings = pd.MultiIndex.from_product(level, names=['Report flag','Cell Name'])
    df = pd.DataFrame(np.array(temporary_df),index=temporary_df.index,columns=headings)
    return(df)

def table_raw_data(dataframe):
    data = dataframe.tolist()
    return data

def to_table(dataframe,master=None,first_add=0):
    global num_report
    def color_tag(master,index,report_num):
        global report_color
        master.Table.tag_cell(report_num,'0,%i' % (index))

    if master == None:
        # data part
        table_data = []
        table_data.append(dataframe.index.tolist())
        table_data[0].insert(0,'')
        i = 1
        for item in dataframe.columns.tolist():
            table_data.append(dataframe[item].tolist())
            table_data[i].insert(0,item[1])
            i+=1
    elif(master.showflag):
        if(first_add):
        # color tag debug part (adjust the cols and rows number when add table)
            master.Table['state']='normal'
            master.Table['cols']=len(dataframe.columns.tolist())+1
            master.Table['rows']=len(dataframe.index.tolist())+1
            master.Table['state']='disabled'
        for i in range(1,num_report+1):
            master.Table.tag_delete('Report%i' % (i))
        table_data = []
        table_data.append(dataframe.index.tolist())
        table_data[0].insert(0,'')
        table_data[0].insert(1,'Report Name')
        i = 1
        for item in dataframe.columns.tolist():
            table_data.append(dataframe[item].tolist())
            table_data[i].insert(0,item[1])
            table_data[i].insert(1,item[0])
            color_tag(master,i,item[0])
            i+=1      
    else:
        if(first_add):
        # color tag debug part (adjust the cols and rows number when add table)
            master.Table['state']='normal'
            master.Table['cols']=len(dataframe.columns.tolist())+1
            master.Table['rows']=len(dataframe.index.tolist())+1
            master.Table['state']='disabled'
        for i in range(1, num_report+1):
            master.Table.tag_delete('Report%i' % (i))
        table_data = []
        table_data.append(dataframe.index.tolist())
        table_data[0].insert(0,'')
        i = 1
        for item in dataframe.columns.tolist():
            table_data.append(dataframe[item].tolist())
            table_data[i].insert(0,item[1])
            color_tag(master,i,item[0])
            i+=1
        # print(table_data)
    return table_data

# def Click():
#     T1.insert_rows('end',count=1)
#     T1.configure()

# def Click2():
#     T1.delete_rows('end',count=1)
#     T1.delete_active('3')

# def Return():
#     #T1.tag_col('Report',0)
#     #T1.tag_configure('Report',background='blue')
#     T1.spans(index='3,3',xy='0,1')

# def Return2():
#     global df
#     global code
#     data = to_table(df)
#     if code ==2:
#         code =0
#     if code ==0:
#         X=1
#         code+=1
#     else:
#         for y in range(0,8):
#             for x in range(0,8):
#                 index = "%i,%i" % (y,x)
#                 var[index] = '1,1'
#         T1.tag_configure('Report',bg='green')
#         T1['variable']=var  
#         code+=1      

    #T1.set('row','3,1',data)
    #T1.tag_lower('Report',"title")

def sortdata(index,master):
    def sortby(index,master):
        # index = 1 -> axis = 1 -> dataframe's index
        # index = 0 -> axis = 0 -> dataframe's values(first row) 
        global sortflag, raw_df, cur_df, cur_tabledata
        if sortflag == 2:
            sortflag = 0
        if sortflag == 0:
            cur_df.sort_values(by=[_str],axis=index,inplace=True)
            sortflag+=1
        elif sortflag == 1:
            cur_df.sort_values(by=[_str],axis=index, ascending=False, inplace=True)
            sortflag+=1
        cur_tabledata = to_table(cur_df,master)
        # print(cur_df)
        # print(cur_tabledata)s
        master.assign_var(cur_tabledata)

    index_x = int(index.split(',')[0])
    index_y = int(index.split(',')[1])       
    if master.showflag == 1:
        if index_x == 1:
            pass 
        else:
            if index_x == 0:
                if index_y == 0:
                    pass
                else:
                    _str = cur_df.columns.tolist()[index_y-1]
                    sortby(0,master)
            elif index_y == 0:
                _str = cur_df.index.tolist()[index_x-2]
                sortby(1,master)
    else:
        if index_x == 0: 
            if index_y == 0:
                pass
            else:
                _str = cur_df.columns.tolist()[index_y-1]
                sortby(0,master)
        elif index_y == 0:
            _str = cur_df.index.tolist()[index_x-1]
            sortby(1,master)

class BuildTable:

    def __init__(self,master,data):
        self.master = tk.Frame(master)
        self.var = tktable.ArrayVar(self.master)
        self.showflag = 0
        self.data = data
        self._assign_var()
        self._buildtable()
        self.master.pack(expand=1,fill='both')

    def assign_var(self,data):
        global report_color
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
        # change the tag color
        for i in range(0,num_report):
            self.Table.tag_lower('report_num',belowthis='title')
            self.Table.tag_configure('Report%i' % (i+1),bg=report_color['Report%i' % (i+1)])
            # maybe can put the tag_lower command another place to reduce times that it execute
        # if showflag == 0:
        #     self.Table['state']='normal'
        #     self.Table.delete_rows(1)
        #     self.Table['state']='disabled'
        # else:
        #     pass
            

        # j=0
        # columnwidth={}
        # for item in self.data:
        #     for i in item:
        #         if (str(j) in columnwidth) == False:
        #             columnwidth[str(j)]= len(i.title()) + 4            
        #         elif (len(i.title())) > columnwidth[str(j)]: 
        #             columnwidth[str(j)]= len(i.title()) + 4
        #     j+=1
        # self.Table.width(**columnwidth)
        # self.Table['variable']=self.var 

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
           
        self.Table = tktable.Table(self.master,
                        state='disabled',
                        rowstretch='all',
                        colstretch='none',
                        height='3',
                        rows=len(self.data[0]),
                        cols=len(self.data),
                        # resizeborders='col',
                        borderwidth='1',
                        variable=self.var,
                        usecommand=0,
                        titlecols=1,
                        titlerows=1,
                        selectmode='extended',
                        selecttitle=1,
                        selecttype='cell',)
        ysb = tk.Scrollbar(self.master,orient="vertical", command=self.Table.yview_scroll)
        xsb = tk.Scrollbar(self.master,orient="horizontal", command=self.Table.xview_scroll)
        self.Table.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        ysb.pack(side='right', fill='y',in_=self.master)
        xsb.pack(side='bottom',fill='x',in_=self.master)
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
        # change the tag color
        for i in range(1,len(self.data)):
            self.Table.tag_cell('Report1','0,%i' % (i))
        self.Table.tag_lower('Report1',belowthis='title')
        self.Table.tag_configure('Report1',bg=report_color['Report1'])

        # popupmenu code
        self.menu = tk.Menu(self.Table, tearoff=0)
        self.menu.add_command(label="Search Related Report")
        self.menu.add_separator()
        self.menu.add_command(label="Analyze",)
        self.menu.add_separator()
        self.menu.add_command(label="Hello!")

        def popupmenu(event):
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                # offset = self.menu.yposition(3)
                self.menu.post(event.x_root, event.y_root)
        self.Table.bind("<Button-2>", popupmenu)

        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####s

        def DoubleClick(event):
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                sortdata(index,self)
                     
        self.Table.bind("<Double-Button-1>",DoubleClick)

root = tk.Tk()
root.geometry('600x400')  
root.minsize(600, 300)
root.title('DC Analysis')

def hightlightdata(master,do_operate,param):
    global cur_df
    master.Table.tag_delete('Highlight')
    if master.showflag == 1:
        num = 2
    else:
        num = 1
    try: 
        float(param)
        tag_index = []
        if do_operate == 'above':
            j = num
            for indexs in cur_df.index:  
                for  i in range(len(cur_df.loc[indexs].values)):  
                    if(float(cur_df.loc[indexs].values[i]) > float(param)): 
                        tag_index.append('%i,%i' % (j,i+1))
                j += 1
        if do_operate == 'below':
            j = num
            for indexs in cur_df.index:  
                for  i in range(len(cur_df.loc[indexs].values)):  
                    if(float(cur_df.loc[indexs].values[i]) < float(param)):  
                        tag_index.append('%i,%i' % (j,i+1))
                j += 1
        for item in tag_index:
            master.Table.tag_cell('Highlight',item)
        master.Table.tag_configure('Highlight',bg='peach puff')
    except:
        pass

def Clear_tag(master):
    master.Table.tag_delete('Highlight')    

raw_df = Get_dataframe(filepath)
cur_df = raw_df.copy()
raw_tabledata = to_table(raw_df)
cur_tabledata = to_table(raw_df)
tb = BuildTable(root,cur_tabledata)


# kind of terribel label names here, again, only for testing, will use organize name for the real one
# the l1, b1 cb, b2 and so on here is just some simply GUI stuff
frm = tk.Frame(root)
l1 = tk.Label(frm,text='Enter Number to Filter: ',font=('Lucida Fax',14))
l1.pack(side='right')
choose_list = tk.StringVar()
cb = ttk.Combobox(frm,width=6, state='readonly',textvariable=choose_list,value=('above','below'))
cb.pack(side='right',padx=10,before=l1)
cb.current(0)    # set the default showup information, 0 is the beginning
entry1 = tk.Entry(frm)
entry1.pack(side='right',before=l1,after=cb)
entry1.insert(0,'Enter filter word')
entry1.bind('<KeyPress-Return>',hightlightdata(tb,cb.get(),entry1.get()))
def Entry1_Callback(event):
    entry1.selection_range(0,'end')
entry1.bind("<FocusIn>", Entry1_Callback)
b2=tk.Button(frm,text='Filter',command=lambda:hightlightdata(tb,cb.get(),entry1.get()))
b2.pack(side='right',before=cb,padx='1m')
tk.Button(frm,text='Clear',command=lambda: Clear_tag(tb)).pack(side='right',before=b2,padx='1m')
frm.pack(before=tb.master,fill='x')


'''df_new = df.sort_values(by=['Critical Path Length'], axis=1)
print(df_new)
df_new = df.sort_values(by=['Critical Path Length'], axis=1, ascending=False)
print(df_new)'''

#print(to_table(df))
#print(np.array(df))


'''
def add_new_data(*args):
    #test.config(state='normal')
    T1.insert_rows('end', 1)
    r = T1.index('end').split(',')[0] #get row number <str>
    args = (r,) + args
    idx = r + ',-1'
    T1.set('row', idx, *args)
    T1.see(idx)'''

def show_report_number(master):
    master.showflag+=1
    if master.showflag>1:
        master.showflag = 0
    cur_tabledata = to_table(cur_df,master)
    master.assign_var(cur_tabledata)

def Add_moreReport(master):
    global add_filepath, raw_df, cur_df
    if num_report == 4:
        print('Limit!')
    else:
        new_df = Get_dataframe(add_filepath)
        raw_df = raw_df.join(new_df).copy()
        cur_df = cur_df.join(new_df).copy()
        cur_tabledata = to_table(cur_df,master,1)
        master.assign_var(cur_tabledata)

def Back_to_raw(master):
    global sortflag, cur_df
    cur_df = raw_df.copy()
    sortflag = 0
    cur_tabledata = to_table(cur_df,master)
    master.assign_var(cur_tabledata)

tk.Button(root,text='Show Report Number',command=lambda:show_report_number(tb)).pack()
tk.Button(root,text='Add More Report',command=lambda:Add_moreReport(tb)).pack()
tk.Button(root,text='Back to Raw',command=lambda: Back_to_raw(tb)).pack()

#tb1.tb.insert_rows('end',1)

root.mainloop()