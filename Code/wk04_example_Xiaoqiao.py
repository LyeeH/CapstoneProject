#Find the number of times each cell appears in that report
#C:\Users\Administrator\Desktop\QORs_Detailed_Timing_Report

import linecache
import re

#file=input("The object file:")

file_object=open("C:/Users/Administrator/Desktop/QORs_Detailed_Timing_Report")

file_context=file_object.read()
file_context_1=file_object.readline()


s=file_context.split('\n')

z=[]

for str0 in s:
    if re.search('/.*\(.*\)',str0):
        #print(str)
        z.append(str0)
x=[]
h=[]


for str0 in z:
    gate_1=re.search('\s*(.*)\s*\(.*\)',str0,re.I)
    gate=gate_1.group(1)
    if not gate in x:
        x.append(gate)
#print(x)

for str0 in x:
    number=0
    for str1 in z:
        if re.search(str0,str1):
               number+=1
    no=str(number)
    h.append(str0+':'+no)
h.sort()
print(h)

neslack=''
total_s=0.000
t=file_context.split('\n\n\n')
for str0 in t:
    if re.search('slack.*\-[0-9]+',str0):
        slack=re.search('slack.*(\-.*)',str0)
        #print(float(slack.group(1)))
        total_s=total_s+ float(slack.group(1))
        neslack=neslack+str0
print(total_s)
#print(neslack)

nes=neslack.split('\n')
#for str0 in x:
    #for str1 in nes:
        #if re.search(str0,str1):
            #print(str1)
            #num1=re.search('\).*([0-9]+)\s+[0-9].*$',str1)
            #print(num1.group(1))
    

