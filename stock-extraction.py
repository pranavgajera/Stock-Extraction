# CS288 Homework 8
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import sys
import os
import subprocess
import re
import sys
import xml
from functools import reduce
import mysql.connector
from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from io import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   lst = dom.getElementsByTagName(tag)
   # 
   # ............

   return lst

# get all text recursively to the bottom
def get_text(e):
   lst=[]
   if(e.nodeType in (3,4)):
      lst.append(e.nodeValue)
   else:
      for y in e.childNodes:
         lst=lst+get_text(y)

   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-z0-9-.]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   p1=subprocess.call(['java','-jar','tagsoup-1.2.1.jar','--files',fn])
   xhtml_file=fn.replace('.html','.xhtml')
   return xhtml_file

def extract_values(dm):
   lst = []
   global lst_text
   lst_text=[]
   
   # getting tr elements
   l = get_elms_for_atr_val('tr','class','most_actives')
   
   # getting text list for the tr elements
   for x in l:
      lst_text.append(get_text(x))
   
   lst_text[0][2]=lst_text[0][2].replace('Price (Intraday)','Price')
   lst_text[0][3]=lst_text[0][3].replace('Change','chng')
   lst_text[0][4]=lst_text[0][4].replace('% Change','pchng')
   lst_text[0][6]=lst_text[0][6].replace('Avg Vol (3 month)','Avg_Vol')
   lst_text[0][7]=lst_text[0][7].replace('Market Cap','Market_Cap')
   lst_text[0][8]=lst_text[0][8].replace('PE Ratio (TTM)','PE_Ratio')
   global keys
   keys=lst_text[0]
   for j in range(1,len(lst_text)):
      for k in range(0,len(lst_text[j])):
         if( k in (2,3,4,5,6,7)):
            lst_text[j][k]=replace_non_alpha_numeric(lst_text[j][k])
            lst_text[j][k]= lst_text[j][k].replace(' ','')
  
   # getting dictionary elements for lst
   for i in range(1,len(lst_text)):
      lst.append(tr_to_dict(lst_text[0],lst_text[i]))
   #   testing 
   print(len(lst)) 
  
  
   return lst

def tr_to_dict(x,n):
   dict={}
   xn=len(x)
   for j in range(0,xn-2):
      dict[x[j]]=n[j]
   return dict
# mysql> describe most_active;

def insert_to_db(l,tbl):
   lst=[]
   for i in l:
      str="INSERT INTO " +tbl+" (Symbol,Name,Price,chng,pchng,Volume,Avg_Vol,Market_Cap)"+" VALUES ("+"\""+i[keys[0]]+"\","+"\""+i[keys[1]]+"\","+i[keys[2]]+","+i[keys[3]]+","+i[keys[4]]+","+i[keys[5]]+","+i[keys[6]]+","+i[keys[7]]+")"
      lst.append(str)
   return lst;

def main():
   html_fn = sys.argv[1]
   table = html_fn.replace('.html','')
   xhtml_fn = html_to_xml(html_fn)
   
   global dom
   dom = parse(xhtml_fn)
   lst = extract_values(dom)
   conn=mysql.connector.connect (host="localhost",db="stock_market",user="root",passwd="", auth_plugin="mysql_native_password")
   cursor=conn.cursor()
   s='DROP TABLE IF EXISTS '+table+';'
   cursor.execute(s)
   s='CREATE TABLE '+table+' (Symbol varchar(10),Name varchar(80),Price float,chng float,pchng float,Volume float,Avg_Vol float,Market_cap float)'
   
   cursor.execute(s)
   
   # make sure your mysql server is up and running
   l = insert_to_db(lst,table)
   i=0 # fn = table name for mysql
   for x in l:
      cursor.execute(x)
 
   cursor.close()
   conn.commit()
   conn.close()

   return xml
# end of main()

if __name__ == "__main__":
    main()

# end of hw7.py