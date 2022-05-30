#!/usr/bin/env python
# coding: utf-8
import Bio
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import pandas as pd
import numpy as np
from os.path import join

path_prefix = "/Users/eceulutas/Desktop/ENS491/"

fname = "PoSSuM.xlsx" 
df = pd.read_excel(join(path_prefix, fname))
df.head(32)


# In[3]:


pdbID=df['PDB ID'].tolist()
chains = df['Chain ID'].tolist()
chains_to_keep =  {}


# In[4]:


import requests
#%matplotlib inline
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import lxml.html as lh
import ssl


# In[5]:


def findseq(id,chain):
  seq=""
  url = "https://www.rcsb.org/fasta/entry/" + id + "/display"
  context = ssl._create_unverified_context()
  html = urlopen(url, context=context)
  soup = BeautifulSoup(html, 'lxml')
  type(soup)
  rows = soup.find('p')
  #print(rows.string)
  fasta = rows.string 
  fas_seq = fasta.split('\n')
  if len(fas_seq)>2:
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
    seq= fas_seq[1]
  return seq

  


# In[6]:


def compare(i,k,df,pdbID,uniprot):
    to_keep = 0
    if uniprot==True:
        rmsd_i = df['RMSD(Ca)'][i]
        rmsd_k = df['RMSD(Ca)'][k]
        if rmsd_i==rmsd_k:
            al_i = df['Aligned length'][i]
            al_k = df['Aligned length'][k]
            if al_i==al_k:
                cos_i = df['Cosine value'][i]
                cos_k = df['Cosine value'][k]
                if cos_i==cos_k:
                    p_i = df['p value'][i]
                    p_k = df['p value'][k]
                    minp = min(p_i,p_k)
                    if minp==p_i:
                        to_keep = i
                    else:
                        to_keep = k
                else:
                    maxcos= max(cos_i,cos_k)
                    if maxcos == cos_i:
                        to_keep=i
                    else:
                        to_keep=k
            else:
                maxal= max(al_i,al_k)
                if maxal == al_i:
                    to_keep=i
                else:
                    to_keep=k
        else:
            minrmsd = min(rmsd_i,rmsd_k)
            if minrmsd==rmsd_i:
                to_keep=i
            else:
                to_keep=k
        return to_keep
    chain_i = chains[i]
    chain_k = chains[k]
    seq_i = findseq(pdbID[i],chain_i)
    seq_k = findseq(pdbID[k],chain_k)
    if seq_i==seq_k:
        rmsd_i = df['RMSD(Ca)'][i]
        rmsd_k = df['RMSD(Ca)'][k]
        if rmsd_i==rmsd_k:
            al_i = df['Aligned length'][i]
            al_k = df['Aligned length'][k]
            if al_i==al_k:
                cos_i = df['Cosine value'][i]
                cos_k = df['Cosine value'][k]
                if cos_i==cos_k:
                    p_i = df['p value'][i]
                    p_k = df['p value'][k]
                    minp = min(p_i,p_k)
                    if minp==p_i:
                        to_keep = i
                    else:
                        to_keep = k
                else:
                    maxcos= max(cos_i,cos_k)
                    if maxcos == cos_i:
                        to_keep=i
                    else:
                        to_keep=k
            else:
                maxal= max(al_i,al_k)
                if maxal == al_i:
                    to_keep=i
                else:
                    to_keep=k
        else:
            minrmsd = min(rmsd_i,rmsd_k)
            if minrmsd==rmsd_i:
                to_keep=i
            else:
                to_keep=k
    else:
        to_keep=-1
    
    return to_keep
            


# In[7]:


def find_occurence(element,pdbID):
    occurences=[]
    for i in range(len(pdbID)):
        if pdbID[i]==element:
            occurences.append(i)
    return occurences


# In[8]:


to_keep= []
df_list= df.values.tolist()
for element in pdbID:
    #print(element)
    occurences = find_occurence(element,pdbID)
    #print(len(occurences))
    copyocc = find_occurence(element,pdbID)
    if len(occurences)==1:
        to_keep.append(df_list[occurences[0]])
    else:
        for a in range(0,len(occurences)):
            for b in range(a+1,len(occurences)):
                idx=compare(occurences[a],occurences[b],df,pdbID,False)
                if idx==occurences[a]:
                    if occurences[b] in copyocc:
                        copyocc.remove(occurences[b])
                elif idx==occurences[b]:
                    if occurences[a] in copyocc:
                        copyocc.remove(occurences[a])
        for x in copyocc:
            if df_list[x] not in to_keep:
                to_keep.append(df_list[x])
print(to_keep)
'''w = open("g_results.txt", "w",  encoding='utf-8')
w.write("PDB ID\tHET code\tChain ID\tRes. No.\tCosine value\tp value\tAligned length\tRMSD(Ca)\tProtein Name\tUniProt ID\tUniRef50\tAligned residues (Ca atoms)")
w.write("\n")
for y in to_keep:
    for e in y:
        w.write(str(e))
        w.write("\t")
    w.write("\n")'''


    





# In[11]:


#part for alignmen
df0 = pd.DataFrame(to_keep)

names = ['PDB ID','HET code','Chain ID','Res. No.','Cosine value','p value','Aligned length','RMSD(Ca)','Protein Name','UniProt ID','UniRef50','Aligned residues (Ca atoms)']
df0.columns=names


# In[14]:


'''pdbid=df0['PDB ID'].tolist()
res = df0['Aligned residues (Ca atoms)'].tolist()
bind_sites = []
search_seq=""
lst1=res[0].split(",")
for k in range(len(lst1)):
        str1 = str(lst1[k])
        idx = str1.find("_")
        search_seq = search_seq+str1[idx+1]
bind_sites.append(search_seq)
for i in range(len(res)):
    lst1=res[i].split(",")
    site_seq=""
    for k in range(len(lst1)):
        str1 = str(lst1[k])
        idx = str1.rfind("_")
        site_seq = site_seq+str1[idx+1]
    bind_sites.append(site_seq)
df0['Aligned residues (Ca atoms)']=bind_sites[1:]'''
to_keep2 = []
df_list2= df0.values.tolist()
uniprotID=df0['UniProt ID'].tolist()
for element in uniprotID:
    #print(element)
    occurences = find_occurence(element,uniprotID)
    #print(len(occurences))
    copyocc = find_occurence(element,uniprotID)
    if len(occurences)==1:
        to_keep.append(df_list2[occurences[0]])
    else:
        for a in range(0,len(occurences)):
            for b in range(a+1,len(occurences)):
                idx=compare(occurences[a],occurences[b],df0,uniprotID,True)
                if idx==occurences[a]:
                    if occurences[b] in copyocc:
                        copyocc.remove(occurences[b])
                elif idx==occurences[b]:
                    if occurences[a] in copyocc:
                        copyocc.remove(occurences[a])
        for x in copyocc:
            if df_list2[x] not in to_keep:
                to_keep2.append(df_list2[x])
print(to_keep2)
df_final = pd.DataFrame(to_keep2)

names = ['PDB ID','HET code','Chain ID','Res. No.','Cosine value','p value','Aligned length','RMSD(Ca)','Protein Name','UniProt ID','UniRef50','Aligned residues (Ca atoms)']
df_final.columns=names
df_final.to_excel(join(path_prefix,"result.xlsx"))

