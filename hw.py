import re
import random
import shutil
from numpy import array
#from sklearn.model_selection import KFold
from os import listdir
from os.path import isfile, join
import numpy as np
import json
import pickle
from collections import Counter
#from clint.textui import progress

def hash_tags(title,car):
  ts =  shutil.get_terminal_size()
  terminal_col=ts[0]
  stringa=''
  if(len(title)>0):
    title=' '+title+' '
    for i in range(int((terminal_col-len(title))/2)):
      stringa+=car
    
    stringa+=title
    for i in range(int((terminal_col-len(title))/2)):
     stringa+=car
    stringa+='\n\n' 
    print(stringa)
  else:
   for i in range(terminal_col):
     stringa+=car
   stringa+='\n\n'
   print(stringa)

def csv_read(path):
     F = open (path,'r')
     line = F.readline()
     hash_def=[]
     type_def=[]
     a=[]
     while line!='' :
                a=line.split(',')
                hash_def.append(a[0])
                type_def.append(a[1])
                line = F.readline()

     F.close()           
     return (hash_def,type_def)

path_feature = '/Users/alessandro/Desktop/Homework/drebin/feature_vectors/'
#path_feature = '/home/parallels/Documents/Homework/drebin/prova/'
path_csv  = '/Users/alessandro/Desktop/Homework/drebin/sha256_family.csv'

list_files = [f for f in listdir(path_feature) if isfile(join(path_feature, f))]
print("\n\nLOADING CVS ...  ",end='')

out = csv_read(path_csv)
hash_def = out[0]
type_def = out[1]

print("FATTO\n\n")
percent_learning = 1
percent_testing = 1 - percent_learning

total_set = len(list_files)

num_learn =int(percent_learning * total_set)
num_test = int(percent_testing * total_set)


malware_content_list=[]
goodware_content_list=[]
malware_diction=dict()
goodware_diction=dict()
malware_diction_prob=dict()
goodware_diction_prob=dict()



hash_tags("LEARNING TRIP START",'#')
mw=0
gw=0
hash_tags("LOADING DATA",'-')
for i in range(num_learn):
    
    path=path_feature+list_files[i]
  
    F = open (path,'r')
     
    if  list_files[i] in hash_def :
       mw+=1
       line=F.readline()
       while(line!=''):
                malware_content_list.append(line.replace("\n",""))
                line = F.readline()

    else:
       gw+=1
       line=F.readline()
       while(line!=''):
                goodware_content_list.append(line.replace("\n",""))
                line = F.readline()
   
    F.close()
print("\n")

hash_tags('','-')
boi_malware = len(malware_content_list)           

print("Dictionary Elaboration Malware: ",end='')
malware_diction=Counter(malware_content_list)
print("FATTO")

print("\n")

print("Dictionary Elaboration Goodware: ",end='')
boi_goodware = len(goodware_content_list)            
goodware_diction=Counter(goodware_content_list)
print("FATTO")

print("\n")
'''
with open('goodware_diction.json', 'w') as f:
    json.dump(goodware_diction, f)
with open('malware_diction.json', 'w') as f:
    json.dump(malware_diction, f)
'''
hash_tags("LEARNING TRIP END",'#')

if( "" in goodware_diction):goodware_diction.pop("")
if( "" in malware_diction):malware_diction.pop("")
count_wrong = 0
count_right = 0

TN = 0
TP = 0
FN = 0
FP = 0

hash_tags('TESTING','*')
#if num_test==0: num_test = 10000
num_test=len(list_files)
print(num_test)
for i in range(len(list_files)):
  path=path_feature+list_files[i]
  if list_files[i] in hash_def: real = True
  else: real=False
  
  F = open (path,'r')
  line=F.readline()
   
  prob_mal= 1
  prob_good= 1


  while(line!=''):
   line=line.replace("\n","")
   if line in goodware_diction: prob_good *= (goodware_diction[line]+1)/(boi_goodware+2)
   if line in malware_diction:  prob_mal *= (malware_diction[line]+1)/(boi_malware+2)
   line = F.readline()
   

  prob_mal *= mw/(mw+gw)
  prob_good *= gw/(mw+gw)

  if prob_mal == 1: prob_mal=0
  if prob_good == 1: prob_good=0

  if prob_good > prob_mal : res=False
  else:  res=True

  if res==True and real==False  :  FN += 1 
  if res==True and real==True   :  TP += 1
  if res==False and real==True  :  FN += 1
  if res==False and real==False :  TN += 1

  if res!=real : 
    count_wrong+=1 
  else:
    count_right+=1
  
  
 
print("Testing on: ", num_test) 
print("Wrong-Error: "+str(count_wrong)+" [{:.2%}]".format((count_wrong/num_test)))
print("Accuracy: "+str(count_right)+" [{:.2%}]".format((count_right/num_test)))
print("\n")

print('TN, TP, FN, FP', TN, TP, FN, FP)


hash_tags('END','*')
print("\n\n")