#!/usr/bin/python

from database import database

from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import argparse

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


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val == 'Fail' else 'black'
    return 'color: %s' % color


#Main program

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--q_release", help="choose a q_release", required=True)
parser.add_argument("-b", "--q_build", help="choose a q_build", required=True)
parser.add_argument("-c", "--q_kernel", help="choose a q_kernel", required=True)
parser.add_argument("-d", "--r_release", help="choose a r_release", required=True)
parser.add_argument("-e", "--r_build", help="choose a r_build", required=True)
parser.add_argument("-f", "--r_kernel", help="choose a r_kernel", required=True)
parser.add_argument("-g", "--category", help="choose a category", required=True)
parser.add_argument("-i", "--case", help="choose a case", required=True)
args = vars(parser.parse_args())



q_release = args['q_release']
q_build  = args['q_build']
q_kernel = args['q_kernel']

r_release = args['r_release']
r_build  = args['r_build']
r_kernel = args['r_kernel']

category = args['category']

case = args['case']

ignore_user = 0
if q_release and q_build and q_kernel and r_release and r_build and r_kernel and category and case:
    ignore_user = 1

cnx = database.open_reportdb()

cursor = cnx.cursor()

if ignore_user == 0:
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

#suite query
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
    cursor.execute(query)
    status_list=list()
    suite_list=list()
    for suite,status in cursor:
        status_list.append(status)
        suite_list.append(suite)
    w[h] = pd.Series(status_list, index=suite_list)

cnx.close()

#example
#d = {
#        'apac2-ph022' : pd.Series(['PASS', 'FAIL', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
#        'apac2-ph023' : pd.Series(['PASS', 'PASS', 'PASS', 'PASS'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
#        'apac2-ph027' : pd.Series(['PASS', 'FAIL', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
#        'apac2-ph031' : pd.Series(['PASS', 'PASS', 'PASS', 'FAIL'], index=['btrfs', 'xfs', 'ext3', 'ext4']),
#        }
#df = pd.DataFrame(d)

#pd.CategoricalIndex.fillna(0)
pd.set_option('display.width', 2000)
pd.set_option('html.border', 1)
df = pd.DataFrame(w)
table_title="{}-{} vs {}-{}".format(q_release,q_build,r_release,r_build)
html=df.style.applymap(color_negative_red).set_table_attributes("border=1").render()
df.name=case
f = open(case+".html", 'w')
print(df)
#print(html)

soup = BeautifulSoup(html, 'html5lib')

tr = soup.find('th', class_='blank level0')
tr.string.replaceWith(table_title)
html=soup.prettify(formatter=None)


f.write(html)
f.close()

