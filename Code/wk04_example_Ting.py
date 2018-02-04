from tkinter import *
import re

def detail_report_window(report):
    root = Tk()
    root.title('Detail Timing Report')
    root.geometry('800x600')
    atext=Text(root,width='600', height='600',bg='yellow')
    atext.insert(INSERT, report)
    atext.pack()


def match_detail(path1,path2,path_group):
    QOR_report=open(path1).read()
    Detailed_QOR_report=open(path2).read()
    for str in QOR_report.split('\n\n'):
        if re.search(path_group ,str, re.M|re.I):
            fact=re.search(r'Critical Path Slack:(.*)',str,re.M|re.I)
            slack=fact.group(1)
            for str in Detailed_QOR_report.split('\n\n\n'):
                if re.search(r'Path Group: '+path_group,str,re.M|re.I):
                    if re.search(r'slack.*'+slack,str,re.M|re.I):
                        detail = re.search(r'Startpoint:.*slack.*\d', str, re.M|re.I|re.S|re.DOTALL)
                        detail_report_window(detail.group())
            
Detailed_QOR_report_path="C:/Users/Ting Wang/Desktop/tool/QORs_Detailed_Timing_Report.txt"
QOR_report_path="C:/Users/Ting Wang/Desktop/tool/QOR_Report_File.txt"
Path_Group=input("Path_Group: ")
match_detail(QOR_report_path, Detailed_QOR_report_path, Path_Group)


    
