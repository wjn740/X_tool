#!/usr/bin/python3



import mysql.connector


qadb2 = {
        'user' : 'qadb',
        'password' : '',
        'host' : '147.2.207.30',
        'database' : 'qadb',
        'raise_on_warnings': True,
        }

reportdb = {
        'user' : 'jnwang',
        'password' : '33jwang5',
        'host' : '147.2.207.100',
        'database' : 'reportdb',
        'raise_on_warnings': True,
        }

def open_reportdb():
    """
    Open a Query of SQL database.
    """
    try:
        cnx = mysql.connector.connect(**reportdb)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

def open_query():
    """
    Open a Query of SQL database.
    """
    try:
        cnx = mysql.connector.connect(**qadb2)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

def query_init_list(query_string, datalist):
    cursor = open_query(query_string)
    if cursor:
        for (data) in cursor:
            datalist.add(data)
    return

