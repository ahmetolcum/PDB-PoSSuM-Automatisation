#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from os.path import join
import requests
#%matplotlib inline
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import lxml.html as lh
import ssl
import os


# In[2]:


folderpath="/Users/eceulutas/Desktop/ENS491/alignment" #dosya pathi
dest = folderpath+"/resultfiles"
arr = [f for f in os.listdir(folderpath) if not f.startswith('.')]#os.listdir(folderpath)
#os.mkdir(dest)


# In[3]:


def findseq(id,chain):
  seq=""
  #https://www.uniprot.org/uniprot/P31572.fasta
  url = "https://www.uniprot.org/uniprot/"+id+".fasta"
  
  context = ssl._create_unverified_context()
  html = urlopen(url, context=context)
  soup = BeautifulSoup(html, 'lxml')
  type(soup)
  rows = soup.find('p')
  #print(rows.string)
  fasta = rows.string 
  fas_seq = fasta.split('\n')
  #print(len(fas_seq))
  #print(fas_seq)
  for k in range(1,len(fas_seq)-1):
    seq = seq + str(fas_seq[k])
  '''if len(fas_seq)>2:
    i=0
    k=0
    isfound = False
    while i < len(fas_seq) and isfound==False:
      header = fas_seq[i].split('|')
      if header!=['']:
        chain_info=header[1]
        #chain_info=chain_info.replace(',', '')
        chain_lst = chain_info.split(',')
        #chain_lst = chain_lst[1:]
        #print(chain_lst)
        if len(chain_lst)==1 and chain== "Chain " + chain:
          k=i
        else:
          for item in chain_lst:
            if item == chain_lst[0]:
              item = item.replace("Chains","")
              idx = item.find("auth")
              if idx!=-1:
                new_item = item.split('[')
                #print(new_item)
                for it in new_item:
                  if it == "auth " + str(chain) + "]":
                    k=i
                    #print("here")
                    isfound=True
                  elif it==chain:
                    k=i
                  elif item != chain_lst[0]:
                    idx = item.find("auth")
                    #print(idx)
                    if idx!=-1:
                      new_item = item.split('[')
                      #print(new_item)
                      for it in new_item:
                        if it== "auth " + str(chain) + "]":
                          k=i
                          isfound=True
                        elif it==chain:
                          k=i
                    elif item == " " + str(chain):
                      k=i
      i+=2
    seq= fas_seq[k+1]
  else:
    seq= fas_seq[1]'''
  return seq


# In[4]:



bind_sites=[]

item="1XVT.xlsx" # dosya adını değiştir
df1= pd.read_excel(join(folderpath, item)) #açılacak dosya adı 
uniprotID= df1['UniProt ID'].tolist()
print(uniprotID[0])
orig_protein = findseq(uniprotID[0],"A")
bind_sites.append(orig_protein)
#print(orig_protein)


pdbID=df1['PDB ID'].tolist()
#print(len(pdbID))
res = df1['Aligned residues (Ca atoms)\n'].tolist()
for k in range(len(pdbID)):
    stri = ""
    for i in range(len(orig_protein)):
        stri = stri + "-"
    lst1 = lst1=res[k].split(",")
    for m in range(len(lst1)):
        str1 = lst1[m]
        idx = str1.rfind("_")
        aa = str1[idx+1]
        idx_ = str1.find("_")
        idxline = str1.find("-")
        loc = int(str1[idx_+2:idxline])
        #print(loc)
        stri = stri[:loc-1] + aa + stri[loc:]
    bind_sites.append(stri)
#print(bind_sites)
                


# In[5]:


df1['Binding Site Alignment']=bind_sites[1:]
df1


# In[6]:


w = open("aligned_results.txt", "w",  encoding='utf-8')
w.write(item.strip(".xlsx")+"\t"+orig_protein+"\n")
for key in range(len(bind_sites[1:])):
    w.write(pdbID[key]+"\t"+bind_sites[key+1]+"\n")
w.close()

