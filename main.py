#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:49:23 2018

@author: james
"""
from pandas import DataFrame, Series
import numpy as np
import pandas as pd


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()



txt_data = pd.read_csv(args.source, header=None)
dic_data = pd.read_csv(args.query, header=None)
df = txt_data.iloc[:,1]
df = pd.DataFrame(df)
dq = dic_data.iloc[:,0]
dq = pd.DataFrame(dq.str.split(' ').tolist())


#solution 1: using trie tree for query

#first make trie tree
class Trie(object):
    def __init__(self, char:str):
        self.data = char
        self.child = []
        self.isfinish = False
        self.titleli = []

def insert_dic(root, word:str):
    node = root
    for letter in word:
        founded = False
        for child in node.child:
            if letter == child.data:
                node = child
                founded = True
                break
        if not founded:
            newnode = Trie(letter)
            node.child.append(newnode)
            node = newnode
                
    node.isfinish = True

def search_trie(root, num, word:str):
    #if num < 20200 and num > 20100:
    #    print(word)
    node = root
    #print(word)
    ind = 0
    while ind < len(word):
        #if num == 20105:
        #    print(ind)
        #    print(word[ind])
        #print('letter in')
        foundd = False
        for child in node.child:
            if word[ind] == child.data:
                foundd = True
                if child.isfinish == True:
                    repeatnum = False
                    for titnum in child.titleli:
                        if titnum == num:
                            repeatnum = True
                            break
                    if not repeatnum:
                        child.titleli.append(num)
                        #if num == 20105:
                        #    print(word[ind])
                    node = root
                    break
                else:
                    #if num == 20105:
                    #    print(word[ind])
                    node = child
                    break
            #node = root
        if foundd == False and node != root: 
             #if num == 20105:
             #     print("GAN")
             ind = ind-1
             node = root
        ind = ind + 1     
         
def boolean_search(root, word:str):
    node = root
    for letter in word:
        for child in node.child:
            #print(child.data)
            if letter == child.data:
                if child.isfinish == True:
                    return child.titleli
                node = child
                break
            
                  

        
root = Trie('朤')
file = open(args.output, 'w')

for i in range(len(dq)):
    for j in range(0,len(dq.columns),2):
        if dq.iloc[i,j] == None:
            break
        insert_dic(root, dq.iloc[i,j])


#put text in search tree
for i in range(len(df)):
    search_trie(root, i+1, df.iloc[i,0])
#debuging = boolean_search(root, "美國")
    
    
#do boolean search and print result
sets = []

for i in range(len(dq)):
    for j in range(0,len(dq.columns),2):
        if dq.iloc[i,j] == None:
            break
        sets.append(set(boolean_search(root, dq.iloc[i,j])))
        
    if len(dq.columns)<2:  #no boolean cases
        sorted(set(sets), key=sets.index)
        if len(sets) > 0 :
            result = list(sets)
            result.sort()
            counting = 0
            for st in result:
                counting = counting + 1
                txt_res = ''.join(str(st))
                if counting != len(result):
                    txt_res = ''.join(', ')
            file.write(txt_res)
        else:
            file.write("0")
    else:
        tmp = set()
        for k in range (1, len(dq.columns), 2):
            if dq.iloc[i,k] == "and":
                tmp = set.intersection(*sets)
            elif dq.iloc[i,k] == "or":
                tmp = set.union(*sets)
            elif dq.iloc[i,k] == "not":
                tmp = set.difference(*sets)
        if len(tmp) > 0 :
            result = list(tmp)
            result.sort()
            counting = 0
            txt_res = ''
            for st in result:
                #print(txt_res)
                counting = counting + 1
                txt_res += str(st)
                if counting != len(result):
                    txt_res += ','
            file.write(txt_res)
            if i != len(dq)-1:
                file.write('\n')
        else:
            file.write("0" + '\n')
    sets.clear()
                   
file.close()