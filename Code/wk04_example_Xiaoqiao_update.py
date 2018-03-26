#Find the number of times each cell appears in that report
#C:\Users\Administrator\Desktop\QORs_Detailed_Timing_Report

import linecache
import re

#file=input("The object file:")

file_object=open("C:/Users/Administrator/Desktop/QORs_Detailed_Timing_Report")

file_context=file_object.read()
file_context_1=file_object.readline()
#print(file_context)

s=file_context.split('\n')

z=[]

for str0 in s:
    if re.search('/.*\(.*\)',str0):
        #print(str0)
        z.append(str0)
x=[]
h=[]


for str0 in z:
    gate_1=re.search('\s*(.*)\s*\(.*\)',str0,re.I)
    gate=gate_1.group(1)
    if not gate in x:
        x.append(gate)
#print(x)
x.sort()
#print(x)
z.sort()
#print(z)
for str0 in x:
    number=0
    for str1 in z:
        if re.search(str0,str1):
               number+=1
    no=str(number)
    h.append(str0+':'+no)
h.sort()
#print(x)
num=0

for a in x:
    if re.search(r'wptr_full/wptr_reg[2]/D',a):
        #print(1)
        a=re.search(r'wptr_full/wptr_reg[2]/D',a)
        num=+1
        #print(a.group())
#print(num)




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
sth=[]
for str in s:
    if re.search(r'.*\([A-Z0-9]*\)\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?[a-z]',str):
        sth.append(str)
        #print(str)
        a=re.search(r'.*\([A-Z0-9]*\)\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?\s*(-?\d+\.\d*)?',str)
        #print(a.groups())
        s=a.groups()
        s=list(s)
        if None in s:
            s.remove(None)
        #print(s[len(s)-2])

