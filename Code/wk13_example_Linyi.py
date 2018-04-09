import linecache
import re
import tkinter as tk
from tkinter import filedialog,ttk
import numpy as np
import pandas as pd
import tktable

file_path = {}
reports_num = 0


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    def __init__(self, *args, **kwargs):
        self.__initialized = False
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")
            if self.tabs() == ():
                self.master.forget(self)
                
        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        try:
            style.element_create("close", "image", "img_close",
                                ("active", "pressed", "!disabled", "img_closepressed"),
                                ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        except:
            pass
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

class Search_section():

    def __init__(self,master,report_num,startpoint_list,endpoint_list,pathgroup_list,timingslack_list,all_list):
        self.mainframe = tk.LabelFrame(master,text='Search',font=('Arial',18),width=215)
        self.report_num = report_num
        self.startpoint_list = startpoint_list
        self.endpoint_list = endpoint_list
        self.pathgroup_list = pathgroup_list
        self.timingslack_list = timingslack_list
        self.all_list = all_list
        self._build_frame()
        self.content_list_flag = None

    def _build_frame(self):
        self.search_frame = tk.Frame(self.mainframe)
        self.search_frame.pack(expand=1,fill='both',side='top')
        self.reference_frame = tk.Frame(self.mainframe)
        self.reference_frame.pack(fill='both',side='bottom')
        self._search_frame_setup()
        self._build_keyword_list()

    def _search_frame_setup(self):
        def filter_list(self,value,objective):
            new_content_list = []
            if objective == 'startpoint':
                for item in self.startpoint_list:
                    if re.match(r'.*%s.*'%(value.replace('[','\[').replace(']','\]').replace('.','\.')),item,re.I) != None:
                        if new_content_list.count(item) == 0:
                            new_content_list.append(item)
                self.content_list_flag = 'startpoint'
            if objective == 'endpoint':
                for item in self.endpoint_list:
                    if re.match(r'.*%s.*'%(value.replace('[','\[').replace(']','\]').replace('.','\.')),item,re.I) != None:
                        if new_content_list.count(item) == 0:
                            new_content_list.append(item)
                self.content_list_flag = 'endpoint'
            if objective == 'pathgroup':
                for item in self.pathgroup_list:
                    if re.match(r'.*%s.*'%(value.replace('[','\[').replace(']','\]').replace('.','\.')),item,re.I) != None:
                        if new_content_list.count(item) == 0:
                            new_content_list.append(item)
                self.content_list_flag = 'pathgroup'
            if objective == 'timingslack':
                for item in self.timingslack_list:
                    if re.match(r'.*%s.*'%(value.replace('[','\[').replace(']','\]').replace('.','\.')),item,re.I) != None:
                        if new_content_list.count(item) == 0:
                            new_content_list.append(item)
                self.content_list_flag = 'timingslack'
            if objective == 'searchall':
                for item in self.all_list:
                    if re.match(r'.*%s.*'%(value.replace('[','\[').replace(']','\]').replace('.','\.')),item,re.I) != None:
                        if new_content_list.count(item) == 0:
                            new_content_list.append(item)
                self.content_list_flag = 'searchall'
            return(new_content_list)

        def callback_startpoint(event):
            value = self.startpoint_entry.get()
            self.content_var.set(filter_list(self,value,'startpoint'))
        def callback_endpoint(event):
            value = self.endpoint_entry.get()
            self.content_var.set(filter_list(self,value,'endpoint'))
        def callback_pathgroup(event):
            value = self.pathgroup_entry.get()
            self.content_var.set(filter_list(self,value,'pathgroup'))
        def callback_timingslack(event):
            value = self.timingslack_entry.get().replace('>','').replace('<','').replace('=','')
            self.content_var.set(filter_list(self,value,'timingslack'))
        def callback_searchall(event):
            value = self.searchall_entry.get().replace('>','').replace('<','').replace('=','')
            self.content_var.set(filter_list(self,value,'searchall'))    
            
        startpoint_frame = tk.Frame(self.search_frame)
        startpoint_label = tk.Label(startpoint_frame,text='Startpoint')
        self.startpoint_entry = tk.Entry(startpoint_frame,width=12)
        startpoint_label.grid(row=0,sticky='e')
        self.startpoint_entry.grid(row=0,column=1,sticky='e')
        self.startpoint_entry.bind('<KeyPress-F2>',callback_startpoint)
        self.startpoint_entry.bind('<KeyPress-Return>',self.highlight_search)
        def callback_startpoint_focusin(event):
            self.startpoint_entry.selection_range(0,'end')
        self.startpoint_entry.bind("<FocusIn>", callback_startpoint_focusin)

        endpoint_frame = tk.Frame(self.search_frame)
        endpoint_label = tk.Label(endpoint_frame,text='Endpoint')
        self.endpoint_entry = tk.Entry(endpoint_frame,width=12)
        endpoint_label.grid(row=0,sticky='e')
        self.endpoint_entry.grid(row=0,column=1,sticky='e')
        self.endpoint_entry.bind('<KeyPress-F2>',callback_endpoint)
        self.endpoint_entry.bind('<KeyPress-Return>',self.highlight_search)
        def callback_endpoint_focusin(event):
            self.endpoint_entry.selection_range(0,'end')
        self.endpoint_entry.bind("<FocusIn>", callback_endpoint_focusin)

        pathgroup_frame = tk.Frame(self.search_frame)
        pathgroup_label = tk.Label(pathgroup_frame,text='Path Group')
        self.pathgroup_entry = tk.Entry(pathgroup_frame,width=12)
        pathgroup_label.grid(row=0,sticky='wn')
        self.pathgroup_entry.grid(row=0,column=1,sticky='e')
        self.pathgroup_entry.bind('<KeyPress-F2>',callback_pathgroup)
        self.pathgroup_entry.bind('<KeyPress-Return>',self.highlight_search)
        def callback_pathgroup_focusin(event):
            self.pathgroup_entry.selection_range(0,'end')
        self.pathgroup_entry.bind("<FocusIn>", callback_pathgroup_focusin)

        timingslack_frame = tk.Frame(self.search_frame)
        timingslack_label = tk.Label(timingslack_frame,text='Timing Slack')
        self.timingslack_entry = tk.Entry(timingslack_frame,width=12)
        timingslack_label.grid(row=0,sticky='e')
        self.timingslack_entry.grid(row=0,column=1,sticky='e')
        self.timingslack_entry.insert('0','(>value or else)')
        self.timingslack_entry.bind('<KeyPress-F2>',callback_timingslack)
        self.timingslack_entry.bind('<KeyPress-Return>',self.highlight_search)
        def callback_timingslack_focusin(event):
            self.timingslack_entry.selection_range(0,'end')
        self.timingslack_entry.bind("<FocusIn>", callback_timingslack_focusin)

        searchall_frame = tk.Frame(self.search_frame)
        searchall_label = tk.Label(searchall_frame,text='Keyword')
        self.searchall_entry = tk.Entry(searchall_frame,width=12)
        searchall_label.grid(row=0,sticky='e')
        self.searchall_entry.grid(row=0,column=1,sticky='e')
        self.searchall_entry.bind('<KeyPress-F2>',callback_searchall)
        self.searchall_entry.bind('<KeyPress-Return>',self.highlight_search)
        searchall_frame.grid(row=2,columnspan=2,sticky='ne')
        def callback_searchall_focusin(event):
            self.searchall_entry.selection_range(0,'end')
        self.searchall_entry.bind("<FocusIn>", callback_searchall_focusin)

        def set_startpoint_button():
            if startpoint_var.get():
                startpoint_frame.grid(row=3,columnspan=2,sticky='ne')
            if startpoint_var.get() == 0:
                startpoint_frame.grid_forget()
        def set_endpoint_button():
            if endpoint_var.get():
                endpoint_frame.grid(row=4,columnspan=2,sticky='ne')
            if endpoint_var.get() == 0:
                endpoint_frame.grid_forget()
        def set_pathgroup_button():
            if pathgroup_var.get():
                pathgroup_frame.grid(row=5,columnspan=2,sticky='ne')
            if pathgroup_var.get() == 0:
                pathgroup_frame.grid_forget()
        def set_timingslack_button():
            if timingslack_var.get():
                timingslack_frame.grid(row=6,columnspan=2,sticky='ne')
            if timingslack_var.get() == 0:
                timingslack_frame.grid_forget() 

        startpoint_var = tk.IntVar()
        endpoint_var = tk.IntVar()
        pathgroup_var = tk.IntVar()
        timingslack_var = tk.IntVar()

        startpoint_b = tk.Checkbutton(self.search_frame,text='Startpoint',font=('Arial',14),justify='left',variable=startpoint_var,command=set_startpoint_button)
        endpoint_b = tk.Checkbutton(self.search_frame,text='Endpoint',font=('Arial',14),justify='left',variable=endpoint_var,command=set_endpoint_button)
        pathgroup_b = tk.Checkbutton(self.search_frame,text='Path Group',font=('Arial',14),justify='left',variable=pathgroup_var,command=set_pathgroup_button)
        timingslack_b = tk.Checkbutton(self.search_frame,text='Timing Slack',font=('Arial',14),justify='left',variable=timingslack_var,command=set_timingslack_button)
        search_b = tk.Button(self.search_frame,text='Search',command=self.highlight_search)
        clear_b = tk. Button(self.search_frame,text='Clear',command=self.clear_search)
        search_b.grid(row=7,column=0)
        clear_b.grid(row=7,column=1)
        startpoint_b.grid(row=0,column=0,sticky='nesw')
        endpoint_b.grid(row=0,column=1,sticky='nesw')
        pathgroup_b.grid(row=1,column=0,sticky='nesw',padx=1)
        timingslack_b.grid(row=1,column=1,sticky='nesw')
        
    def _build_keyword_list(self):

        def callback_keyword_list(event):
            _str = content_listbox.get(content_listbox.curselection())
            if self.content_list_flag == 'startpoint':
                self.startpoint_entry.delete(0,'end')
                self.startpoint_entry.insert(0,_str)
            if self.content_list_flag == 'endpoint':
                self.endpoint_entry.delete(0,'end')
                self.endpoint_entry.insert(0,_str)
            if self.content_list_flag == 'pathgroup':
                self.pathgroup_entry.delete(0,'end')
                self.pathgroup_entry.insert(0,_str)
            if self.content_list_flag == 'timingslack':
                if re.match(r'[<>].*',self.timingslack_entry.get()) != None:
                    if re.match(r'[<>]=.*',self.timingslack_entry.get()) != None:
                        self.timingslack_entry.delete(2,'end')
                        self.timingslack_entry.insert(2,_str)
                    else:
                        self.timingslack_entry.delete(1,'end')
                        self.timingslack_entry.insert(1,_str)
                else:
                    self.timingslack_entry.delete(0,'end')
                    self.timingslack_entry.insert(0,_str)
            if self.content_list_flag == 'searchall':
                if re.match(r'[<>].*',self.searchall_entry.get()) != None:
                    if re.match(r'[<>]=.*',self.searchall_entry.get()) != None:
                        self.searchall_entry.delete(2,'end')
                        self.searchall_entry.insert(2,_str)
                    else:
                        self.searchall_entry.delete(1,'end')
                        self.searchall_entry.insert(1,_str)
                else:
                    self.searchall_entry.delete(0,'end')
                    self.searchall_entry.insert(0,_str)

        def callback_keyword_list_and_updated(event):
            callback_keyword_list(event)
            self.highlight_search()
        self.content_var = tk.StringVar()
        content_listbox = tk.Listbox(self.reference_frame,listvariable=self.content_var,height=20)
        content_listbox.pack(side='bottom',expand=1,fill='both',padx=2,pady=2)
        content_listbox.bind('<ButtonRelease-1>',callback_keyword_list)
        content_listbox.bind('<KeyRelease-Return>',callback_keyword_list_and_updated)

    def highlight_search(self,event=None):
        global reports_num
        self.searchflag = [0,0,0,0,0]
        def match(master_ss,master_tb,_str,column,equal=''):       
            i = 0
            index_t = index.copy()
            if equal == '':
                _string = _str.replace('[','\[').replace(']','\]').replace('.','\.')
                if master_ss.first_fill_flag:
                    for item in master_tb.cur_df[column]:
                        if re.match(r'.*%s.*'%(_string),item,re.I) != None:
                            index.append(i)
                        i += 1
                else:
                    for item in index_t:
                        if re.match(r'.*%s.*'%(_string),master_tb.cur_df[column].iloc[item],re.I) == None:
                            index.remove(item)
            elif equal == '>':
                if master_ss.first_fill_flag:
                    for item in master_tb.cur_df[column]:
                        if float(item) > float(_str):
                            index.append(i)
                        i += 1
                else:
                    for item in index_t:
                        if float(master_tb.cur_df[column].iloc[item]) <= float(_str):
                            index.remove(item)
            elif equal == '<':
                if master_ss.first_fill_flag:
                    for item in master_tb.cur_df[column]:
                        if float(item) < float(_str):
                            index.append(i)
                        i += 1
                else:
                    for item in index_t:
                        if float(master_tb.cur_df[column].iloc[item]) >= float(_str):
                            index.remove(item)
            elif equal == '>=':
                if master_ss.first_fill_flag:
                    for item in master_tb.cur_df[column]:
                        if float(item) >= float(_str):
                            index.append(i)
                        i += 1
                else:
                    for item in index_t:
                        if float(master_tb.cur_df[column].iloc[item]) < float(_str):
                            index.remove(item)
            elif equal == '<=':
                if master_ss.first_fill_flag:
                    for item in master_tb.cur_df[column]:
                        if float(item) <= float(_str):
                            index.append(i)
                        i += 1
                else:
                    for item in index_t:
                        if float(master_tb.cur_df[column].iloc[item]) > float(_str):
                            index.remove(item)

        if self.search_frame.grid_slaves(row=3) != []: 
            if self.startpoint_entry.get() != '':
                self.searchflag[0]=1   
        if self.search_frame.grid_slaves(row=4) != []:
            if self.endpoint_entry.get() != '':
                self.searchflag[1]=1
        if self.search_frame.grid_slaves(row=5) != []:
            if self.pathgroup_entry.get() != '':
                self.searchflag[2]=1
        if self.search_frame.grid_slaves(row=6) != []:
            if self.timingslack_entry.get() != '':
                if self.timingslack_entry.get() != '(>value or else)':
                    self.searchflag[3]=1
        if self.search_frame.grid_slaves(row=2) != []:
            if self.searchall_entry.get() != '':
                self.searchflag[4]=1
        for i in range(1,reports_num+1):
            try:
                search_section = globals()['window'+str(i)+'_search']
                table = globals()['window'+str(i)+'_tb']
                table.Table.tag_delete('Highlight')
                index = []
                index_y = []
                index_xy = []
                columns_flag = self.searchflag.copy()
                columns_flag.pop()
                search_section.first_fill_flag = True
                columns = table.cur_df.columns.tolist()          
                if self.searchflag[0]:
                    _str = self.startpoint_entry.get()
                    match(search_section,table,_str,columns[0])
                    search_section.first_fill_flag = False
                if self.searchflag[1]:
                    _str = self.endpoint_entry.get()
                    match(search_section,table,_str,columns[1])
                    search_section.first_fill_flag = False
                if self.searchflag[2]:
                    _str = self.pathgroup_entry.get()
                    match(search_section,table,_str,columns[2])
                    search_section.first_fill_flag = False
                if self.searchflag[3]:
                    _str = self.timingslack_entry.get()
                    if re.match(r'[<>].*',_str) == None:
                        match(search_section,table,_str,columns[3])
                    else:
                        if re.match(r'<-*[0-9].*',_str) != None:
                            sign = '<'
                            match(search_section,table,_str.split('<')[1],columns[3],equal=sign)
                        elif re.match(r'>-*[0-9].*',_str) != None:
                            sign = '>'
                            match(search_section,table,_str.split('>')[1],columns[3],equal=sign)
                        elif re.match(r'<=.*',_str) != None:
                            sign = '<='
                            match(search_section,table,_str.split('=')[1],columns[3],equal=sign)
                        elif re.match(r'>=.*',_str) != None:
                            sign = '>='
                            match(search_section,table,_str.split('=')[1],columns[3],equal=sign)
                    search_section.first_fill_flag = False
                if self.searchflag[4]:
                    columns_forall = columns.copy()
                    timingslack_flag = False
                    for i in (3,2,1,0):
                        if self.searchflag[i] == 1:
                             columns_forall.pop(i)
                    _str = self.searchall_entry.get()
                    i = 0
                    if re.match(r'[<>].*',_str) != None:
                        for item in table.cur_df[columns[3]]:
                            if re.match(r'<(?!=).*',_str) != None:
                                if float(item) < float(_str.split('<')[1]):
                                    index_y.append(i)
                            elif re.match(r'>(?!=).*',_str) != None:
                                if float(item) > float(_str.split('>')[1]):
                                    index_y.append(i)
                            elif re.match(r'<=.*',_str) != None:
                                if float(item) <= float(_str.split('=')[1]):
                                    index_y.append(i)
                            elif re.match(r'>=.*',_str) != None:
                                if float(item) >= float(_str.split('=')[1]):
                                    index_y.append(i)
                            i += 1
                        timingslack_flag = True
                    else:
                        for col in columns_forall:
                            i = 0
                            for item in table.cur_df[col]:
                                if re.match(r'.*%s.*'%(_str).replace('[','\[').replace(']','\]').replace('.','\.'),item,re.I) != None:
                                    if index_xy.count('%i,%i'%(i+1,columns.index(col))) == 0:
                                        index_xy.append('%i,%i'%(i+1,columns.index(col)))
                                        index_y.append(i)
                                i += 1
                if index == []:
                    if index_y != []:
                        if timingslack_flag:
                            for item in index_y: 
                                index_xy.append('%i,3'%(item+1))
                elif self.searchflag[4]:
                    index_t = index.copy()
                    for item in index_t:
                        if index_y.count(item) == 0:
                            index.remove(item)
                    if timingslack_flag:
                        for item in index:
                            i = 0
                            for col in columns_flag:
                                if col == 1:
                                    index_xy.append('%i,%i'%(item+1,i))
                                i += 1
                            if index_xy.count('%i,3'%(item+1)) == 0:
                                index_xy.append('%i,3'%(item+1))
                    else:
                        index_t = index_xy.copy()
                        for item in index_t:
                            if int(item.split(',')[0])-1 not in index:
                                index_xy.remove(item)
                        for item in index:
                            i = 0
                            for col in columns_flag:
                                if col == 1:
                                    index_xy.append('%i,%i'%(item+1,i))
                                i += 1
                else:
                    for item in index:
                        i = 0
                        for col in columns_flag:
                            if col == 1:
                                index_xy.append('%i,%i'%(item+1,i))
                            i += 1
                index = index_xy.copy()

                for item in index:
                    table.Table.tag_cell('Highlight',item)
                    table.Table.tag_configure('Highlight',bg='pale green')
            except:
                pass
                # table.Table.selection_set('%i,0'%(item+1))
        # for indexs in cur_df.index:  
        # for  i in range(len(cur_df.loc[indexs].values)):  
        #     if(float(cur_df.loc[indexs].values[i]) > float(param)): 

    def clear_search(self):
        global reports_num
        for i in range(1,reports_num+1):
            try:
                ss = globals()['window'+str(i)+'_search']
                ss.startpoint_entry.delete(0,'end')
                ss.endpoint_entry.delete(0,'end')
                ss.pathgroup_entry.delete(0,'end')
                ss.timingslack_entry.delete(0,'end')
                ss.timingslack_entry.insert(0,'(>value or else)')
                ss.searchall_entry.delete(0,'end')
                ss.content_var.set('')
                table = globals()['window'+str(i)+'_tb']
                table.Table.tag_delete('Highlight')
            except:
                pass

class Build_report_names:

    def __init__(self,master,dataframe,report_details,report_num):
        self.master = master
        self.panedwindow = tk.PanedWindow(master,orient='vertical',sashrelief='sunken',sashwidth=8,showhandle=True,handlepad=400,handlesize=9)
        self.panedwindow.pack(expand=1,fill='both')
        self.masterframe = tk.Frame(self.panedwindow)
        self.notebook = CustomNotebook(self.panedwindow)
        self.var = tktable.ArrayVar(self.masterframe)
        self.report_details = report_details
        self.report_num = report_num
        self.report_detail_num = 0
        self.showflag = 0
        self.sortflag = 0
        self.report_detail_dic = {}
        self.detail_flag = False
        self.raw_df = dataframe.copy()
        self.cur_df = dataframe.copy()
        self.data = self.to_table(self.cur_df)
        self._assign_var()
        self._build_table()
        # self.Table.selection_set('2,2','3,3')
        self.panedwindow.add(self.masterframe,sticky='news',minsize=200)

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
        try:
            self.Table.tag_delete('Highlight')
        except:
            pass

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

        # index_x = int(index.split(',')[0])
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

    def _build_table(self):        
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

        def addtab_report():
            content = self.Table.selection_get()
            keyword = []
            for item in self.Table.selection_get().split(' '):
                keyword.append(item.replace('{','').replace('}','').replace('[','\[').replace(']','\]'))
            for item in self.report_details:
                content = re.match(r'(.*Startpoint\: %s.*(?:.*\n)*?.*Endpoint\: %s.*(?:.*\n)*?.*Path Group\: %s.*(?:.*\n)*?.*slack \([A-Z]*\).*?%s.*)' % (keyword[0],keyword[1],keyword[2],keyword[3]),item)
                if content != None:
                    _str = content.group()
                    break
            '''the following code can be modified without if statement'''
            if len(self.panedwindow.panes()) == 1:
                self.report_detail_num = 1
                self.report_detail_dic['Table_details%i' % (self.report_detail_num)] = Build_report_details(self.notebook,_str,self.report_detail_num)
            else:
                self.report_detail_num += 1
                self.report_detail_dic['Table_details%i' % (self.report_detail_num)] = Build_report_details(self.notebook,_str,self.report_detail_num)
                self.notebook.select(self.notebook.index('end')-1)
            try:
                self.panedwindow.panecget(self.notebook,'width')
                pass
            except:
                self.panedwindow.add(self.notebook,sticky='nesw')

            

        # popupmenu code
        self.menu = tk.Menu(self.Table, tearoff=0)
        self.menu.add_command(label="Open Detail Report in Tab",command=addtab_report)
        # self.menu.add_separator()
        # self.menu.add_command(label="Hello!")

        def popupmenu(event):
            self.Table.selection_clear('all')
            self.Table.selection_set('@%i,%i'%(event.x,event.y))
            self.Table.activate('@%i,%i'%(event.x,event.y))
            index = self.Table.index('active')

            if self.Table.tag_includes('title',index) == False:
                # offset = self.menu.yposition(3)
                self.menu.post(event.x_root, event.y_root)
        self.Table.bind("<Button-2>", popupmenu)

        #tb.tag_cell('green',index)
        # tb.tag_configure('green', background='green')
        #### MAINLOOPING ####s

        def DoubleClick(event):
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                self.sortdata(index)
                self.Table.selection_clear('all')
            else:
                index_x = int(index.split(',')[0]) 
                # print(index_x)
                index = self.cur_df.index.tolist()[index_x-1]
                keyword_raw = self.cur_df.ix[(index)].tolist()
                keyword = []
                for item in keyword_raw:
                    keyword.append(item.replace('[','\[').replace(']','\]'))
                for item in self.report_details:
                    content = re.match(r'(.*Startpoint\: %s.*(?:.*\n)*?.*Endpoint\: %s.*(?:.*\n)*?.*Path Group\: %s.*(?:.*\n)*?.*slack \([A-Z]*\).*?%s.*)' % (keyword[0],keyword[1],keyword[2],keyword[3]),item)
                    if content != None:
                        _str = content.group()
                        break
                if len(self.panedwindow.panes()) == 1:
                    self.report_detail_num = 1
                    self.report_detail_dic['Table_details%i' % (self.report_detail_num)] = Build_report_details(self.notebook,_str,self.report_detail_num)
                else:
                    index = self.notebook.index(self.notebook.select())
                    self.report_detail_dic['Table_details%i' % (index+1)].update_content(_str)
                try:
                    self.panedwindow.panecget(self.notebook,'width')
                    pass
                except:
                    self.panedwindow.add(self.notebook,sticky='nesw')
                
        self.Table.bind("<Double-Button-1>",DoubleClick)

class Build_report_details:

    def __init__(self,master,report_details,report_num):
        self.master = master
        self.masterframe = tk.Frame(self.master)
        self.tableframe = tk.Frame(self.masterframe)
        self.var = tktable.ArrayVar(self.tableframe)
        self._str_path_detail_t = tk.StringVar()
        self.text_box_t = tk.Label(self.masterframe,textvariable=self._str_path_detail_t,justify='left',anchor='w')
        self._str_path_detail_b = tk.StringVar()
        self.text_box_b = tk.Label(self.masterframe,textvariable=self._str_path_detail_b,justify='left',anchor='w')
        self.showflag = 0
        self.sortflag = 0
        self.report_num = report_num
        self.convert_details(report_details)
        self.raw_df = self.cur_df.copy()
        self.data = self.to_table(self.cur_df)
        self._assign_var()
        self._build_table()
        self.text_box_t.pack(side='top')
        self.text_box_b.pack(side='bottom')
        self.tableframe.pack(side='bottom',after=self.text_box_b,expand=1,fill='both')
        self.master.add(self.masterframe,sticky='nesw',text=' Report%i'%(self.report_num))

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

        # index_x = int(index.split(',')[0])
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
            data = re.findall(r'(-?[0-9]*\.[0-9]+)\s?([rf]?)',line)
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
            # global report_names
            index = self.Table.index('active')
            if self.Table.tag_includes('title',index) == True:
                self.sortdata(index)
            # else:
            #     index_x = int(index.split(',')[0]) 
            #     # print(index_x)
            #     index = self.cur_df.index.tolist()[index_x-1]
            #     keyword_raw = self.cur_df.ix[(index)].tolist()
            #     keyword = []
            #     for item in keyword_raw:
            #         keyword.append(item.replace('[','\[').replace(']','\]'))
            #     for item in report_details:
            #         content = re.match(r'(.*Startpoint\: %s.*(?:.*\n)*?.*Endpoint\: %s.*(?:.*\n)*?.*Path Group\: %s.*(?:.*\n)*?.*slack \([A-Z]*\).*?%s.*)' % (keyword[0],keyword[1],keyword[2],keyword[3]),item)
            #         if content != None:
            #             _str = content.group()
                

        self.Table.bind("<Double-Button-1>",DoubleClick)

def open_report():
    global file_path,reports_num
    reports_num += 1
    file_path['Report%i'%(reports_num)] = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    if file_path['Report%i'%(reports_num)] == '':
        reports_num -=1
    else:
        file = open(file_path['Report%i'%(reports_num)],'r+')

        file_read = file.read()
        report_names = re.findall(r'Startpoint\: ([a-z].*)(?:.*\n)*?.*Endpoint\: ([a-z].*)(?:.*\n)*?.*Path Group\: ([a-zA-Z0-9].*)(?:.*\n)*?.*slack \([A-Z]*\).*?(-?[0-9].*)',file_read)
        startpoint_list = []
        endpoint_list = []
        pathgroup_list = []
        timingslack_list = []
        all_list = []
        for item in report_names:
            if startpoint_list.count(item[0].split('(')[0].replace(' ','')) == 0:
                startpoint_list.append(item[0].split('(')[0].replace(' ',''))
        for item in report_names:
            if endpoint_list.count(item[1].split('(')[0].replace(' ','')) == 0:
                endpoint_list.append(item[1].split('(')[0].replace(' ',''))
        for item in report_names:
            if pathgroup_list.count(item[2]) == 0:
                pathgroup_list.append(item[2])
        for item in report_names:
            if timingslack_list.count(item[3]) == 0:    
                timingslack_list.append(item[3])
        for item in startpoint_list:
            if all_list.count(item) == 0:
                all_list.append(item)
        for item in endpoint_list:
            if all_list.count(item) == 0:
                all_list.append(item)
        for item in pathgroup_list:
            if all_list.count(item) == 0:
                all_list.append(item)
        for item in timingslack_list:
            if all_list.count(item) == 0:
                all_list.append(item)

        report_details = re.findall(r'(.*Startpoint\: [a-z].*(?:.*\n)*?.*Endpoint\: [a-z].*(?:.*\n)*?.*Path Group\: [a-zA-Z0-9].*(?:.*\n)*?.*slack \([A-Z]*\).*?[[0-9].*)',file_read)

        report_names_list = []
        for item in report_names:
            report_names_list.append(list(item))

        for item in report_names_list:
            item[0] = item[0].split('(')[0].replace(' ','')
            item[1] = item[1].split('(')[0].replace(' ','')
        df = pd.DataFrame(report_names_list,columns=['Startpoint','Endpoint','Path Group','Timing Slack'])

        window = tk.Toplevel(root)
        # window = globals()['window'+str(reports_num)]
        window.geometry('800x700')
        window.minsize(800,600)
        window.title('DC Analysis')

        pw = tk.PanedWindow(window)
        pw.pack(expand=1,fill='both')
        globals()['window'+str(reports_num)+'_search'] = Search_section(pw,reports_num,startpoint_list,endpoint_list,pathgroup_list,timingslack_list,all_list)
        ss = globals()['window'+str(reports_num)+'_search']
        pw.add(ss.mainframe,sticky='nesw',minsize=215,padx=2)
        right_frame = tk.Frame(pw)
        globals()['window'+str(reports_num)+'_tb'] = Build_report_names(right_frame,df,report_details,reports_num)
        tb = globals()['window'+str(reports_num)+'_tb']
        pw.add(right_frame,sticky='nesw')


root = tk.Tk()
root.title('Digital Analysis Tool')
root.geometry('600x200')
root.minsize(400,200)

text_label = tk.Label(root,text='Please import reports',font=('Arial',22))
text_label.pack(expand=1,fill='both')
open_file_b = tk.Button(root,text='Load Report',command=open_report)
open_file_b.pack(side='bottom',pady=10)

root.mainloop()

