from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re
import pandas as pd
from pandas import Series,DataFrame
import tktable

def trans_d(index,df):
    column_str=df.columns.tolist()[int(index[0])]
    row_num=int(index[2])-1
    return column_str, row_num

def trans_t(df,column_str,row_num):
    c_num=df.columns.tolist().index(column_str)
    r_num=row_num+1
    index_r='%i,%i'%(r_num,c_num)
    return index_r

def negative_set(df,Table):
    for item in df.columns.tolist():
        for num in range (len(df[item])):
            try:
                parament=float(df[item][num])
                if parament<0.000:
                    neg_index=trans_t(df, item, num)
                    Table.tag_cell('negative',neg_index)
                    Table.tag_configure('negative',bg='salmon')
                    
            except:
                str_index=trans_t(df, item, num)
                Table.tag_cell('table_str',str_index)

def get_file_path(entry):
    open_file = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    entry.delete(0,END)
    entry.insert(0,open_file)  

def drawtable(frame,df):
    
    var=tktable.ArrayVar()

    i = 0
    table_data = []
    for item in df.columns.tolist():
        table_data.append(df[item].tolist())
        table_data[i].insert(0,item)
        i+=1
    #print(table_data)


    col_count=0
    row_count=0
    for column in table_data:
        for row in column:
            index = "%i,%i" % (row_count,col_count)
            #print(index)
            var[index] = row
            row_count+=1
        col_count+=1
        row_count=0



    Table = tktable.Table(frame,
                        state='disabled',
                        rowstretch='all',
                        colstretch='all',
                        height=str(len(table_data[0])),
                        rows=len(table_data[0]),
                        cols=len(table_data),
                        # resizeborders='col',
                        borderwidth='2',
                        variable=var,
                        usecommand=0,
                        titlerows=1,
                        # selectmode='extended',
                        selecttitle=1,
                        selecttype='cell')
    Table.grid(row=0, column=0, padx=3, pady=3)

    j = 0
    columnwidth={}
    for item in table_data:
        for i in item:
            if (str(j) in columnwidth) == False:
                columnwidth[str(j)]= 15 
            elif (len(str(i).title())) > columnwidth[str(j)]:                   
                columnwidth[str(j)]= len(str(i).title())
        j+=1
    
    vbar = Scrollbar(frame,orient="vertical", command=Table.yview_scroll)
    Table.configure(yscrollcommand=vbar.set)
    #vbar.pack(side='right', fill='y',in_=frame)
    #Table.pack(expand=1,fill='both')
    Table.grid(row=0, column=0, padx=3, pady=3)
    vbar.grid(row=0, column=1,sticky=NS)
    Table.width(**columnwidth)
    Table.tag_configure('sel',bg='khaki')
    
    return var,Table

def Build_Detailed_Table(path_group,slack):
    global win_Detailed 
    def closeWindow():
        win_Detailed.destroy()
        #set for report

    read_Detailed=open(Detailed_QOR_report_path).read()
    Detailed_split=read_Detailed.split('\n\n\n')

    selected_report=''
    item_num=0
    for item in Detailed_split:
        if item_num==0:
            if re.search('\s*Path Group:\s%s\n(?:.*\n)*?\s*slack.*%s'%(path_group,slack),item):
                selected_report=item
                item_num+=1

    #print(selected_report)   
    Startpoint=re.search(r'Startpoint:(.*)\(?',selected_report).group()
    Endpoint=re.search(r'Endpoint:(.*)\(?',selected_report).group()
    Path_Group=re.search(r'Path Group:(.*)',selected_report).group()
    Path_Type=re.search(r'Path Type:(.*)',selected_report).group()
    #data_1st={'Startpoint':[Startpoint],'Endpoint':[Endpoint],'Path Group':[Path_Group],'Path Type':[Path_Type]}
    #df_1st=DataFrame(data_1st,columns=['Startpoint','Endpoint','Path Group','Path Type'])

    Point=[]
    Cap=[]
    Trans=[]
    Incr=[]
    Path=[]
    row_number=0
    s_report=selected_report.split('-\n')
    selected_report=''
    for num in range (len(s_report)-3,len(s_report)):
        selected_report=selected_report+'\n'+s_report[num]
    #print(selected_report)
    selected_report=selected_report.split('\n')
    for line in selected_report:
        abc=[]
        bcd=[]
        if not re.search('-{2,}',line):
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
                #print(bcd)
                Cap.append(bcd[0])
                Trans.append(bcd[1])
                Incr.append(bcd[2])
                Path.append(bcd[3])
                row_number+=1
            whole=whole.group()
            point=re.sub(whole,'',line)
            point=point.strip()
            if re.search(r'\S',point):
                Point.append(point)
    data_2nd={'Point':Point,'Cap':Cap,'Trans':Trans,'Incr':Incr,'Path':Path}
    df_2nd=DataFrame(data_2nd,columns=['Point','Cap','Trans','Incr','Path'])

    win_Detailed=Toplevel(win_QOR)
    frmUPL = Frame(win_Detailed,width=275, height=100)
    frmUPR = Frame(win_Detailed,width=275, height=100)
    frmCE = Frame(win_Detailed,width=550, height=450)
    frmLW = Frame(win_Detailed,width=550, height=35)
    frmUPL.grid(row=0, column=0, padx=3, pady=3,sticky=W)
    frmUPR.grid(row=0, column=1, padx=3, pady=3,sticky=E)
    frmCE.grid(row=1, column=0, columnspan=2, padx=3, pady=3,sticky=E+W)
    frmLW.grid(row=2, column=0,columnspan=2,sticky=E+W)

    btn =Button(frmLW, text='Confirm', width = 8, command=closeWindow)
    btn.grid(row=0, column=0,padx=3,pady=3,sticky=E)
    var_2nd,table_2nd=drawtable(frmCE,df_2nd)
    negative_set(df_2nd,table_2nd)
    label = ttk.Label(frmUPL, text=Startpoint,font = ('Times New Roman','10'))
    label.grid(row=0, column=0,padx=3,pady=3,sticky=W)
    label = ttk.Label(frmUPL, text=Endpoint,font = ('Times New Roman','10'))
    label.grid(row=1, column=0,padx=3,pady=3,sticky=W)
    label = ttk.Label(frmUPR, text=Path_Group,font = ('Times New Roman','10'))
    label.grid(row=0, column=1,padx=3,pady=3,sticky=W)
    label = ttk.Label(frmUPR, text=Path_Type,font = ('Times New Roman','10'))
    label.grid(row=1, column=1,padx=3,pady=3,sticky=W)

    win_Detailed.mainloop()

def special(df,Table):
    for item in df['Timing Path Group'].tolist():
        if re.search('Critical Path Slack',item):
            Slack_char=item
    no_slack=df['Timing Path Group'].tolist().index(Slack_char)+1
    Table.tag_row('slack', no_slack)   
    
    def DoubleClick(event):
        # global report_names
        index_a = Table.index('active')
        if Table.tag_includes('slack',index_a) == True:
            path_group_s=df.columns.tolist()[int(index_a[2])]
            slack_s=df[path_group_s][int(index_a[0])-1]
            #print(path_group_s)
            #print(slack_s)
            Build_Detailed_Table(path_group_s,slack_s)
    Table.bind("<Double-Button-1>",DoubleClick)

def QOR_analyze():
    global QOR_report_path,Detailed_QOR_report_path,win_QOR
    QOR_report_path=entry1.get()
    Detailed_QOR_report_path=entry2.get()
    read_QOR=open(QOR_report_path).read()
    read_QOR_str=read_QOR.split('\n\n')
    Timing_Path_Group_list=list(re.findall('Timing Path Group \'(.*)\'',read_QOR))
    QOR_col_list=['Timing Path Group']
    QOR_col_list.extend(Timing_Path_Group_list)
    QOR_df=DataFrame(columns=QOR_col_list)

    read_QOR_list_list=[]
    for item in read_QOR_str:
        for group in Timing_Path_Group_list:
            if re.search(r'Timing Path Group \'%s\''%group, item):
                read_QOR_list=re.findall(r'(-?\d+\.\d*)',item)
                QOR_df[group]=read_QOR_list
                character_list=re.findall(r'(.*)\:\s*-?\d+\.\d*',item)
    QOR_df['Timing Path Group']=character_list


    win_QOR=Toplevel(root)    
    win_QOR.title('QOR report')
    frame_QOR= Frame(win_QOR, width=850, height=400)
    frame_QOR.grid(row=0, column=0, padx=3, pady=3)

    var_QOR,table_QOR=drawtable(frame_QOR,QOR_df)
    table_QOR['titlecols']=1
    
    negative_set(QOR_df,table_QOR)
    special(QOR_df,table_QOR)
    


    win_QOR.mainloop()

root = Tk()
root.title('Digital Analysis')
root.geometry('700x200')
root.minsize(400,200)

text_label1 = Label(root,text='Please import QOR reports:',font=('New Times Roman',12))
text_label1.grid(row=0, column=0,pady=15,sticky=W)

entry1 = Entry(root,text=None,bg='white',highlightthickness=0,width=40)
entry1.grid(row=0, column=1,pady=15,sticky=W)
entry1.insert(0,'Please enter path here')

button1 = Button(root,text='Browser',command=lambda : get_file_path(entry1))
button1.grid(row=0, column=2,pady=15)

text_label2 = Label(root,text='Please import Detailed reports:',font=('New Times Roman',12))
text_label2.grid(row=1, column=0,pady=15,sticky=W)

entry2 = Entry(root,text=None,bg='white',highlightthickness=0,width=40)
entry2.grid(row=1, column=1,pady=15,sticky=W)
entry2.insert(0,'Please enter path here')

button2 = Button(root,text='Browser',command=lambda : get_file_path(entry2))
button2.grid(row=1, column=2,pady=15)

analyze_b = Button(root,text='Analyze',command=QOR_analyze)
analyze_b.grid(row=2, column=0,columnspan=3,pady=10)


root.mainloop()