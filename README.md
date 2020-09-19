# (WMMP) WHO MAIL ME PROJECT

The project uses a simple group of Python scripts, creates a text scrape from an MBOX file
from a Gmail account to analyze data, to produce visualizations and reports if you need them
to add to your data science projects.

## How does it work?
The Scripts follows a structure to produce the correct results
 * `mbox.txt` Chose a mbox file and convert it to a plain text mbox.txt ( Read pre-procesing data )
 * `WMM_gather.py` Gather the information from mbox.txt creates a SQL database and clean the data
 * `WMM_visual.py` Reads the database and produce graphs to analyse them
 
This is the beta phase and there are many things to improve that could be added to the script,
feel free to contribute if you wish 

## User guide 

### **1. Pre-procesing data ('mbox file'):**
  The gathering file only works with .txt files with a defined structure as detailed below, you can see and example of it in the "Input" folder:
 
#### **1.1. mbox file :** 
   Download the .mbox file through your gmail account following the instructions in the link: 
      
   + Download mbox file : https://takeout.google.com
      
   Google will download the data of your mail from the beginning of time in a file type "filename.mbox".
   The file can weigh several GB so it is necessary to convert it to plain text and thus avoid the unnecessary use of memory when processing the data, leaving a file of just MB    easily manipulated

#### **1.2. From a .mbox to.txt file :**
   to convert the file, use the ´´mbox-viewer´´ program, a powerful tool that is extremely fast and easy to use.
   you can download it from its repository and thank the author.
      
  + Githhub : https://github.com/eneam/mboxviewer  
  + Direct download: https://sourceforge.net/projects/mbox-viewer/

   Once `mbox-viewer` was installed, read the user guide and do what you have to do with all your emails, the important thing to use `WMMP` is that the emails that you are going    to export to txt have a date and where they are from. to avoid errors with text scraping once you have selected the mails to export convert to txt according to the user          guide    and that's it, the program will give you a .txt file with the correct structure to use `WMMP`
 
 
### **2. Gathering cript ´WMM_gather.py´**
Once you have the mbox.txt file ready you can start with the processing scripts, the first one to use will be `WMM_gather.py`
   
##### **2.1 Requirements:**
     
   + MySQL software:
     This script works by creating a MySQL database (soon more SQL databases like sqlite) so it is necessary to install this software.
             
     + Community version download  do https://dev.mysql.com/downloads/mysql/
         
   + MySQL library for python : 
     This library can be installed directly with MySQL package, otherwise use pip method
     
        ```
        shell> pip install mysql-connector-python
        ```    
     Or you can see full installation guide for other distributions here:    
     + Python library : https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
    
#### **2.2 Running the script:** 
  + Open the scrpit and put your MySQL credentials
  
  ```
     # SQL CONNECTION
     conn = sql.connect(
         host ="put your host here",
         user =" user name here",
         password =" MySQL pass here"
     )
  ```
        
  + If you are starting a new project or deleting an old one, turn on the "drop" lines, but if you just want to update your database, turn off these lines:

```
     # Use just when you start a new project
 --->#cur.execute('DROP DATABASE IF EXISTS mail_mbox')
     # change the database's name "mail_box" if you want
     cur.execute("CREATE DATABASE IF NOT EXISTS mail_mbox")
     cur.execute("USE mail_mbox")

     # Use just when you start a new project
 --->#cur.execute('DROP TABLE IF EXISTS Counts')
     cur.execute('''
     CREATE TABLE IF NOT EXISTS counts(
     counts_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
     Org TEXT, count INTEGER);
     ''')

     # Use just when you start a new project
 --->#cur.execute('DROP TABLE IF EXISTS mails')
     cur.execute('''
     CREATE TABLE IF NOT EXISTS mails(
     mails_id  INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
     day INT, month INT, year INT, counts_id  INTEGER);
     ''')
```

  + Automatic file upload -> in "fname" put the default path to the mbox.txt file or just skip it and put it manually when you run the script
  
```
    # load data from m-box.txt o .csv file
    fname = input('Write a file name or Enter to use default: ')
    if (len(fname) < 1):
        fname = 'D:/...put your file access route here/'
```

  + Finally run the script and wait until it finishes, check your new database and the information it contains.


___

License
---------------
MIT 

Enjoy
---------------
If this tool has been useful for you, feel free to thank me in your program code.
