#!/usr/bin/python

import sys

from database import database

from TestCase import TestCase

from node import statistics_node
from node import build_statistic_data

import pandas as pd

from collections import defaultdict
from collections import OrderedDict
from DefaultOrderedDict import DefaultOrderedDict


compare_product_list = list()
compare_product_where_string=""
compare_testsuite_string = ""
compare_testcase_string = ""
compare_host_string = ""
compare_arch_string = ""
final_select_string = ""
TestCase_global_list_array = list()
statistics_list = list()


def create_candidate_list():
    """
    The candidate list include kernel_version, product, release. this group could
    on behalf of one object that be used in performance testing as a abstract product.
    """
    query  = ("SELECT distinct `kernel_version`, `product`, `release` from performance_view")
    cnx = database.open_query()
    cursor = cnx.cursor()
    cursor.execute(query)

    i=0
    table=list()
    for (kernel_version, product, release) in cursor:
        table.append([kernel_version, product, release])
        print(i, table[i])
        i+=1

    cnx.close()

    l = input("Please input the NO. products(eg. 11,1):").split(",")
    for index in l:
        try:
            compare_product_list.append(table[int(index)])
        except IndexError:
            sys.stderr.write("choose error, total amount: " + str(len(table)) + "\n" +"out of list\n")
            sys.exit(1)
    return

def make_where_string_for_compare_product_list():
    where_string=""
    kernel_version_string=""
    product_string=""
    release_string=""
    start_kernel=True
    start_product=True
    start_release=True

    start=True
    if compare_product_list:
        print("compare_product_list={}".format(compare_product_list))
        for k,p,r in compare_product_list:
            '''
            [0]: kernel_version
            [1]: product
            [2]: release
            '''
            if k and p and r:
                if start == False:
                    where_string = "".join([where_string, " or "])
                where_string = "".join([where_string, "(`kernel_version` = '" + k + "' and `product` = '" + p + "' and `release` = '" + r + "' )"])
                start = False
            else:
                return "";
    return "".join(["(" + where_string + ")"])


def create_testsuite_list():
    if compare_product_list:
        where_string = make_where_string_for_compare_product_list()
        global compare_product_where_string
        compare_product_where_string = where_string
    if where_string:
        cnx = database.open_query()
        select_string="".join(["SELECT distinct testsuite from  performance_view ", " where ", where_string, ";"])
        print(select_string)
        cursor = cnx.cursor()
        cursor.execute(select_string);

        i=0
        table=list()
        for (testsuite) in cursor:
            table.append(testsuite)
            print(i, table[i])
            i+=1
        cnx.close()

        l = input("Please input the NO. testsuite(eg. 3):")
        global compare_testsuite_string
        if not l and i > 0:
            compare_testsuite_string = "".join(table[0])
        else:
            compare_testsuite_string = "".join(table[int(l)])
        return

def create_testcase_list():
    global compare_product_where_string
    global compare_testsuite_string
    if compare_product_where_string and compare_testsuite_string:
        query = "".join(["SELECT distinct testcase from performance_view where" + compare_product_where_string + " and " + " `testsuite` = '" + compare_testsuite_string + "';"])
        cnx = database.open_query()
        cursor = cnx.cursor()
        cursor.execute(query)

        i = 0
        table=list()
        for (testcase) in cursor:
            table.append(testcase)
            print(i, table[i])
            i+=1
        cnx.close()
        l = input("Please input the NO. testcase(eg, 0):")
        global compare_testcase_string
        if not l and i > 0:
            compare_testcase_string = "".join(table[0])
        else:
            compare_testcase_string = "".join(table[int(l)])
        return

def create_host_list():
    if compare_testcase_string and compare_testsuite_string and compare_product_where_string:
        query = "".join(["SELECT distinct host from performance_view where" + compare_product_where_string + " and " + " `testsuite` = '" + compare_testsuite_string + "'" + " and " + " `testcase` = '" + compare_testcase_string + "';"])
        cnx = database.open_query()
        cursor = cnx.cursor()
        cursor.execute(query)

        i = 0
        table=list()
        for (host) in cursor:
            table.append(host)
            print(i, table[i])
            i+=1
        cnx.close()
        l = input("Please input the NO. host(eg, 0):")
        global compare_host_string
        if not l and i > 0:
            compare_host_string = "".join(table[0])
        else:
            compare_host_string = "".join(table[int(l)])
        return

def create_arch_list():
    if compare_testcase_string and compare_testsuite_string and compare_product_where_string and compare_host_string:
        query = "".join(["SELECT distinct arch from performance_view where" + compare_product_where_string + " and " + " `testsuite` = '" + compare_testsuite_string + "'" + " and " + " `testcase` = '" + compare_testcase_string + "'" + " and " + " `host` = '" + compare_host_string + "';"])
        cnx = database.open_query()
        cursor = cnx.cursor()
        cursor.execute(query)

        i = 0
        table=list()
        for (arch) in cursor:
            table.append(arch)
            print(i, table[i])
            i+=1
        cnx.close()
        l = input("Please input the NO. arch(eg, 0):")
        global compare_arch_string
        if not l and i > 0:
            compare_arch_string = "".join(table[0])
        else:
            compare_arch_string = "".join(table[int(l)])
        return

def user_input_interface():
    create_candidate_list()

    create_testsuite_list()

    create_testcase_list()

    create_host_list()

    create_arch_list()


def make_final_select_query():
    global final_select_string
    final_select_string = "".join(["SELECT * from performance_view where" + compare_product_where_string + " and " + " `testsuite` = '" + compare_testsuite_string + "'" + " and " + " `testcase` = '" + compare_testcase_string + "'" + " and " + " `host` = '" + compare_host_string + "' and `arch` = '" + compare_arch_string + "';"])

def build_global_testcase_list():
    """
    Query Database get TestCase objects set.
    This set include all candidate records to compare.
    """
    make_final_select_query()
    cnx = database.open_query()
    cursor = cnx.cursor()
    print(final_select_string)
    cursor.execute(final_select_string)
    testcase_list = list()
    for (submission_id, arch, product, release, host, log_url, testsuite, test_time, failed, testcase, kernel_version) in cursor:
        testcase_list.append(TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase,kernel_version))

    #groups = defaultdict(list)

    #for obj in testcase_list:
    #    groups[obj.kernel_version+obj.product+obj.release].append(obj)
    #new_list = groups.values()
    #a = OrderedDict(new_list)

    #groups = OrderedDict()
    #for obj in testcase_list:
    #    groups[obj.kernel_version+obj.product+obj.release].append(obj)
    #new_list = groups.values()
    """
    TestCase_global_list_array looks like:

    """
    groups = DefaultOrderedDict(list)
    for obj in testcase_list:
        groups[obj.kernel_version+obj.product+obj.release].append(obj)
    new_list = groups.values()

    global TestCase_global_list_array
    TestCase_global_list_array = new_list



def build_statistic_list():
    if TestCase_global_list_array:
        for l in TestCase_global_list_array:
            statistics_list.append(statistics_node(l))


def format_dataframe(football):
    a=len(football.columns)
    c=int(a/2)
    d=len(football.index)

    for c1 in range(a-c, a):
        for d1 in range(0, d, 1):
            if 'mean' in football.index[d1] and 'Time' in football.index[d1]:
                try:
                    i = football.iloc[d1,c1] = 100 * (football.iloc[d1, c1-c-1] / football.iloc[d1,c] - 1)
                    if i < -10:
                        football.iloc[d1,c1] ="{:0.4f}*".format(football.iloc[d1,c1])

                except IndexError:
                    print("football.iloc[d1,c1] = 100 * (football.iloc[c1-c-1,d1] / football.iloc[c,d1] - 1)")
                    sys.exit(2)

user_input_interface()

build_global_testcase_list()

build_statistic_list()

if statistics_list:
    data = build_statistic_data(statistics_list)

if data:
    pd.set_option('display.width', 4000)
    dataframe = pd.DataFrame(data, index=statistics_list[0].indexs)
    #dataframe.style.format({'ratio1': "{:0.4f}", 'ratio2': "{:0.4f}"})
    a=len(dataframe.columns)
    b=a
    for l in range(1, a, 1):
        dataframe.insert(b, 'ratio'+str(l),100 * (dataframe[statistics_list[-l+1].name] / dataframe[statistics_list[-l].name] - 1))
        b+=1

print(dataframe.sort_index())
#format_dataframe(dataframe)
#print(dataframe)
