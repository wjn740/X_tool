#!/usr/bin/python

from database import database

import numpy as np
import pandas as pd

class status_matrix():
    def __init__(self):
        self.q_kernel = ""
        self.q_product = ""
        self.q_release = ""
        self.r_kernel = ""
        self.r_product = ""
        self.r_release = ""
        self.category = ""

    def __repr__(self):
        return "<status_matrix>"



cnx = database.open_reportdb()

cursor = cnx.cursor()

query = ("select distinct q_release, q_build , q_kernel from report_view;")

cursor.execute(query)

i=0
table=list()
for p,r,k in cursor:
    table.append([p,r,k])
    print(i,table[i])
    i+=1


l = input("Please input the NO. product to compare(eg, 1):")
if l:
    q_release = table[int(l)][0]
    q_build  = table[int(l)][1]
    q_kernel = table[int(l)][2]

query = ("select distinct r_release, r_build , r_kernel from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"';")
print(query)
cursor.execute(query)
i=0
table=list()
for p,r,k in cursor:
    table.append([p,r,k])
    print(i,table[i])
    i+=1

l = input("Please input the NO. product to compare(eg, 1):")
if l:
    r_release = table[int(l)][0]
    r_build  = table[int(l)][1]
    r_kernel = table[int(l)][2]

#question + reference#
query = ("select distinct `category` from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"'" + " and "+ "`r_release` = '"+r_release+"'" + " and "+ "`r_build` = '"+ r_build + "' and " + "`r_kernel` = '" + r_kernel + "';")
print(query)
cursor.execute(query)
i=0
table=list()
for c in cursor:
    table.append(c)
    print(i,table[i])
    i+=1

l = input("Please input the NO. category to compare(eg, 1):")
if l:
    category = table[int(l)][0]

query = ("select distinct `case` from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"'" + " and "+ "`r_release` = '"+r_release+"'" + " and "+ "`r_build` = '"+ r_build + "' and " + "`r_kernel` = '" + r_kernel + "'" + " and " + "`category` = '" + category + "'"+";")
print(query)
cursor.execute(query)
i=0
table=list()
for c in cursor:
    table.append(c)
    print(i,table[i])
    i+=1

l = input("Please input the NO. case to compare(eg, 1):")
if l:
    case = table[int(l)][0]

query = ("select distinct `suite` from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"'" + " and "+ "`r_release` = '"+r_release+"'" + " and "+ "`r_build` = '"+ r_build + "' and " + "`r_kernel` = '" + r_kernel + "'" + " and " + "`category` = '" + category + "'"+ " and "+" `case` = '"+ case +"';")
print(query)
cursor.execute(query)
i=0
table=list()
for s in cursor:
    table.append(s)
    print(i,table[i])
    i+=1

suites = table

query = ("select distinct `q_host` from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"'" + " and "+ "`r_release` = '"+r_release+"'" + " and "+ "`r_build` = '"+ r_build + "' and " + "`r_kernel` = '" + r_kernel + "'" + " and " + "`category` = '" + category + "'"+ " and "+" `case` = '"+ case + "' and `q_host` = `r_host`"+"order by `q_host`"+";")
print(query)
cursor.execute(query)
i=0
table=list()
for s in cursor:
    table.append(s)
    print(i,table[i])
    i+=1

hosts = table

print(hosts)
print("==========================================================")

w = {}
for h in hosts:
    query = ("select distinct `suite`,`status` from report_view where `q_release` = '"+q_release+"' and `q_build` = '"+q_build+"' and `q_kernel` = '"+q_kernel+"'" + " and "+ "`r_release` = '"+r_release+"'" + " and "+ "`r_build` = '"+ r_build + "' and " + "`r_kernel` = '" +r_kernel + "'" + " and " + "`category` = '" + category + "'"+ " and "+" `case` = '"+ case + "' and `q_host` = `r_host`"+ " and `q_host` = '"+"".join(h)+"'" + " order by `suite`;")
    print("king={}".format(query))
    cursor.execute(query)
    status_list=list()
    suite_list=list()
    for suite,status in cursor:
        status_list.append(status)
        suite_list.append(suite)
    w[h] = pd.Series(status_list, index=suite_list)



d = {
        'apac2-ph022' : pd.Series(['PASS', 'FAIL', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
        'apac2-ph023' : pd.Series(['PASS', 'PASS', 'PASS', 'PASS'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
        'apac2-ph027' : pd.Series(['PASS', 'FAIL', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
        'apac2-ph031' : pd.Series(['PASS', 'PASS', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
        }

df = pd.DataFrame(d)
df = pd.DataFrame(w)
pd.set_option('display.width', 2000)

print(df)

cnx.close()
