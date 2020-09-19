#  ##### Coding: utf-8 ####

# See README.md for information and usage about the project
# Copyright (c) 2020 HARDROCO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT A short and simple permissive license with conditions
# only requiring preservation of copyright and license notices.
# Licensed works, modifications, and larger works may be distributed
# under different terms and without source code.
# See the MIT license in license.txt file or in
#             https://choosealicense.com/licenses/mit/
#
# You can update your database running over again the program, but be careful with
# the "DROP" lines, just active them to start a new project .
# =======================================================================

# libraries
import mysql.connector as sql
import re
import sys
print('Running program...')

print('loading lybraries --> OK')

# SQL CONNECTION
conn = sql.connect(
    host="put your host here",
    user=" put your user name here",
    password="put your MySQL pass here"
)

cur = conn.cursor()  # buffered = True, emergency case to bypass error in cursor, but it s better to limit 1 fetchone command

print('Connecting to SQL --> OK')

# HEADER PROGRAM
print('''\n>>> ¡WARNING! This program run under the MIT License, please read about it
in the license file attached to the project.. <<<''')

print('''\n========================================================\n
          WHO MAIL ME - Gathering Data Program
                 Created by HARDROCO\n
========================================================''')

print('''This program will gather and save data from a mail's .txt or .csv file,
previously download and convert from .mbox to plain text type, from your mail account.
(Check the pre-processing data instructions)

Finally the data will be save in a MySQL Database, you can change some code lines
to run the program in a different SQL software

>>> You can update your database running over again the program, but be careful with 
the "DROP" lines, just active them to start a new project .\n''')

# CONTINUE OR QUIT THE PROGRAM
print('Do you want to start the program?\n')
user_op = (input('Select Enter to continue or N to quit :')).upper()
option_n = 'N'

if user_op == option_n:
    print('Program finished, Good bye!')
    sys.exit()
else:
    print('Running program...\n')

# DATABASE CREATION
print('Cheking Database ...')

# Use just when you start a new project
#cur.execute('DROP DATABASE IF EXISTS mail_mbox')
# change the database's name "mail_box" if you want
cur.execute("CREATE DATABASE IF NOT EXISTS mail_mbox")
cur.execute("USE mail_mbox")

# Use just when you start a new project
#cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''
CREATE TABLE IF NOT EXISTS counts(
counts_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
Org TEXT, count INTEGER);
''')

# Use just when you start a new project
#cur.execute('DROP TABLE IF EXISTS mails')
cur.execute('''
CREATE TABLE IF NOT EXISTS mails(
mails_id  INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
day INT, month INT, year INT, counts_id  INTEGER);
''')

print('Database --> OK\n')

# RE-FUNCTIONS TO FIND SOMETHINHGS


def lookup(look, file):
    fh = open(file, encoding='utf-8')
    data_li = list()

    for line in fh:
        data = re.findall(look, line)
        if len(data) < 1:
            continue
        data_li.append(data)
    return data_li


# print('functions load --> OK')

# load data from m-box.txt o .csv file
fname = input('Write a file name or Enter to use default: ')
if (len(fname) < 1):
    fname = 'D:/...put your file access route here/'

print('loading file --> OK\n')

print('Scraping text...\n')
# REGULAR EXPRESION TO FIND DATA
re_mails = '^FROM: .*@(\S+)'
re_dates = '^DATE: (\S+)'

mail_list = lookup(re_mails, fname)
date_list = lookup(re_dates, fname)

# the length of the lists must always be the same, if not check your RE
print('list len')
print(len(mail_list), len(date_list))
print('Text Scraped --> OK')


# saving data in SQL database
print('\nSaving data in Database...')

ini_count = 1

# cleaning some emails and dates
for org, date in zip(mail_list, date_list):
    date_s = date[0].split('/')
    day, month, year = date_s[0], date_s[1], date_s[2]
    org_list = re.findall('(.+)>', org[0])

    if len(org_list) < 1:
        org_clean = org[0]
    else:
        org_clean = org_list[0]

# saving data en tables
    cur.execute('SELECT count FROM Counts WHERE org = %s LIMIT 1', (org_clean,))
    row = cur.fetchone()

    if row is None:
        cur.execute('''INSERT INTO counts (org, count)
                    VALUES (%s, %s)''', (org_clean, ini_count)
                    )
    else:
        cur.execute(
            'UPDATE Counts SET count = count + 1 WHERE org = %s', (org_clean,)
        )

    cur.execute('SELECT counts_id FROM Counts WHERE org = %s', (org_clean, ))
    counts_id = cur.fetchone()[0]

    cur.execute('''INSERT INTO mails
                (day, month, year, counts_id)
                VALUES ( %s, %s, %s, %s)''',
                (day, month, year, counts_id)
                )

conn.commit()
cur.close()

print('Data saved --> OK\n')

print('>>> Now you can use the visualization program to see th results\n')

print('Program finished.')

print(f'''\n=======================================================\n
           WHO MAIL ME - Gathering Data Program
                  Created by HARDROCO\n
=======================================================''')
