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
# =======================================================================

# import libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import mysql.connector as sql
import sys

print('Starting program...')
print('loading lybraries --> OK')

# SQL CONNECTION
conn = sql.connect(
    host="your host",
    user="your user",
    password="your pass",
    database="mail_mbox"
)
cur = conn.cursor()  # buffered = True  # emergency case to bypass error in cursor, but it s better to limit 1 fetchone command

print('Connecting to SQL --> OK\n')

print('''>>> ¡WARNING! This program run under the MIT License, please read about it
in the license file attached to the project.. <<<''')

# HEADER PROGRAM
print('''\n==================================================\n
         WHO MAIL ME - Vizualization program
                 Created by HARDROCO\n
==================================================''')

print('''This program will plot graphics from the mail's Database
created with the gathering program. The graphics will be 
created in the next order:\n
1. Top Mail received from each Organization in your mail box
2. Mail received each the year by a specific Organization
3. Mail received each the month by a specific Organization
4. Mail received each the day by a specific Organization\n''')

# CONTINUE OR QUIT THE PROGRAM
print('Do you want to start the program?\n')
user_op = (input('Select Enter to continue or N to quit :')).upper()
option_n = 'N'

if user_op == option_n:
    print('Program finished, Good bye!')
    sys.exit()
else:
    print('Running program...\n')

# -------------------------------------------------------------------
print('''---GRAPHIC 1---\n
1. Top Mail received from each Organization in your mail box\n''')

# DATAFRAME 1
comand = "SELECT counts_id, Org, count FROM Counts ORDER BY count DESC"
df = pd.read_sql(comand, conn)

#print('df1 created --> ok\n')

# TOP ORG
print('>>> Choose how many organizations you want to chart:\n')

# data frame lenght and control vizulization
first_value = 1
last_value = len(df['counts_id'])
top_value = int(
    input(f'Enter a number ({first_value} - {last_value}): '))

df_top_show = df.head(top_value)

#print('control variables --> OK')

# FUNCTIONS

# BARPLOT GRAPH


def graph_barplot_mbox(g_x, g_y, g_title, x_lb, y_lb, dis, pltt):
    print('loading graph...')

    sns.set(style="darkgrid")
    plt.figure(figsize=(15, 12))

    ax = sns.barplot(g_x, g_y, palette=pltt)

    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='11'
    )

    plt.title(g_title,
              fontweight='bold',
              fontsize='x-large',
              color='orange'
              )

    plt.subplots_adjust(top=0.7)

    plt.xlabel(x_lb, fontweight='bold', color='orange',
               fontsize='17', horizontalalignment='center')
    plt.ylabel(y_lb, fontweight='bold', color='orange',
               fontsize='17', horizontalalignment='center')

    # data on bars
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + dis,
                '{:1.0f}'.format(height),
                ha="center")

    return plt.show()

# COUNTPLOT GRAPH


def graph_countplot_mbox(g_x, g_title, x_lb, y_lb, dis, pltt):
    print('loading graph...')

    sns.set(style="darkgrid")
    plt.figure(figsize=(15, 12))

    ax = sns.countplot(g_x, palette=pltt)

    plt.xticks(
        horizontalalignment='right',
        fontweight='light',
        fontsize='11'
    )

    plt.title(g_title,
              fontweight='bold',
              fontsize='x-large',
              color='orange'
              )

    plt.subplots_adjust(top=0.7)

    plt.xlabel(x_lb, fontweight='bold', color='orange',
               fontsize='17', horizontalalignment='center')
    plt.ylabel(y_lb, fontweight='bold', color='orange',
               fontsize='17', horizontalalignment='center')

    # data on bars
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + dis,
                height,
                ha="center")

    return plt.show()


#print('functions load --> OK ')

# GRAPH 1 - FULL HISTORY
print(f'\nTop {top_value} Organizations:\n\n', df_top_show, '\n')

# graph axis
grap_x, grap_y = df_top_show['Org'], df_top_show['count']

grap_title = f'''Top {top_value} Organizations' emails received
Org vs Count'''

# graphic parameter
x_label = 'Organization'
y_label = 'Count'
dis_lbl = 7
palette = "deep"

graph_barplot_mbox(grap_x, grap_y, grap_title,
                   x_label, y_label, dis_lbl, palette)

# HEADER GRAPH 2
print(f'''\n---GRAPHIC 2---\n
2. Mail received each year by a specific Organization\n''')

print(f'''>>> Choose an Org's ID from the "top {top_value} Org" showed
before or choose a number from the range below to show the
mails received from it. 
Range ( {first_value} - {last_value} )\n  ''')

# VIZUALIZATION DATA
mail_org = int(input(f'Org ID: '))
org_obj = df[df['counts_id'] == mail_org]['Org']
org_clean = org_obj.iloc[0]

print(f'Org Selected --> {org_clean}\n')

# DATAFRAME 2
comand_2 = '''SELECT Counts.Org,mails.day, mails.month, mails.year 
FROM counts JOIN mails ON Counts.counts_id = mails.counts_id 
WHERE mails.counts_id = %s ORDER BY year DESC;'''

df_2 = pd.read_sql(comand_2, conn, params=(str(mail_org),))

#print('Dataframe 2 created --> OK')

# DATES - GRAPH 2
column_y_m = ['year', 'month']
group_y_m = df_2.groupby(column_y_m)

column_y = 'year'
group_y = df_2.groupby(column_y)

#print('DataFrame grouped --> OK\n')

# GRAPH 2 -  YEAR
print(f'''\n{org_clean} YEAR GRAPH\n''')

# graph axis
grap_x_y = df_2['year']

# graphic parameter
grap_title_y = f'''Mail received by year from {org_clean}
Year vs Count'''
x_label_y = 'Year'
y_label_y = 'Count'
dis_lbl_y = 7
palette_y = 'BrBG'

total_count_y = df_2['Org'].count()

graph_countplot_mbox(grap_x_y, grap_title_y, x_label_y,
                     y_label_y, dis_lbl_y, palette_y)

print(
    f'\nTotal mail received by Year from {org_clean} = ', total_count_y, '\n')

# HEADER GRAPH 3
print(f'''---GRAPHIC 3---\n
3. Mail received each month from {org_clean}\n''')

print(f'''>>> Choose a especific date to see the mails 
received from {org_clean}\n
Years available:''')

# DATES - GRAPH 3

# show years
yea_cl = list()

for name_group, group in group_y:
    yea_cl.append(name_group)
print(yea_cl)

año = int(input('Year to consult: '))
year_g = group_y.get_group(año)

print(f'''\nMonths available in {año}:''')

# show months
mon_cl = list()

for mon in year_g['month']:
    if mon in mon_cl:
        continue
    else:
        mon_cl.append(mon)
print(mon_cl)

month = int(input('Month to consult: '))
month_g = group_y_m.get_group((año, month))

# GRAPH 3 - MONTH
print(f'''\n{org_clean} YEAR {año} - MONTH GRAPH\n''')

# graphic axis
grap_x_m = year_g['month']

# graphic parameter
grap_title_m = f'''Mail received by month from {org_clean} - {año}
month vs Count'''
x_label_m = 'month'
y_label_m = 'Count'
dis_lbl_m = 0.5
palette_m = 'BuPu'

total_count_m = year_g['month'].count()

graph_countplot_mbox(grap_x_m, grap_title_m, x_label_m,
                     y_label_m, dis_lbl_m, palette_m)

print(
    f'\nTotal Mail received by month for {org_clean} = ', total_count_m, '\n')

# HEADER GRAPH 4
print(f'''---GRAPHIC 4---\n
4. Mail received each day from {org_clean}\n''')


# GRAPH 4 - day
print(f'''{org_clean} YEAR {año} - MONTH {month} - DAY GRAPH\n''')

# graphic axis
grap_x_d = month_g['day']

# graphic parameter
grap_title_d = f'''Mail received by Day from {org_clean} - {año}/{month}
Day vs Count'''
x_label_d = 'Day'
y_label_d = 'Count'
dis_lbl_d = 0.02
palette_d = 'CMRmap'

total_count_d = month_g['day'].count()

graph_countplot_mbox(grap_x_d, grap_title_d, x_label_d,
                     y_label_d, dis_lbl_d, palette_d)

print(f'\nTotal Mail received by day from {org_clean} = ', total_count_d, '\n')

cur.close()

# END PROGRAM
print('Program finished.')

print(f'''\n==================================================\n
            WHO MAIL ME - Vizualization program
                 Created by HARDROCO\n
==================================================''')
