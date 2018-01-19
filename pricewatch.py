
# It does not support python version2.
# This program only works on Python3
# NEED to Install BeautifulSoup4 and SQlite3
# to run type
# python3 pricewatch.py update
# python3 pricewatch.py search gamename
# python3 pricewatch.py history gameid


import sys
print("Updating prices from site: Gamesman")
import sqlite3
conn = sqlite3.connect('anuj10410653.db') # creating a database
c = conn.cursor()
from bs4 import BeautifulSoup
import urllib.request
with urllib.request.urlopen('https://www.gamesmen.com.au/ps4/games/view-all') as s1_r:
	s1_html=s1_r.read()
with urllib.request.urlopen('https://www.jbhifi.com.au/games-consoles/platforms/ps4/?p=1&s=releaseDate&sd=2') as s2_r:
	s2_html=s2_r.read()
par1=sys.argv[1]

if par1=="update":

############################# scrapping data from gamesman###############################
	print("Updating prices from site: Gamesman")
	soup = BeautifulSoup(s1_html,'html.parser')
	s1_name=list()
	s1_price=list()
	s1_len=list()
	s1_data=soup.findAll("p",{"class": "product-name"})
	for s1_item in s1_data:
		s1_r=s1_item.findChildren()[0].get_text()
		s1_name.append(s1_r)
	s1_data=soup.findAll("div",{"class": "price-box"})
	for s1_item in s1_data:
		s1_a=s1_item.findChildren()[0].findChildren()[2].get_text()
		s1_e=s1_a.strip()
		s1_price.append(s1_e)
	s1_x=len(s1_name)
	for i in range(s1_x):
		s1_y='Gamesman'
		s1_len.append(s1_y) 
	s1_nameprice=tuple(zip(s1_name,s1_price,s1_len))
	s1_sortedlist=list(set(s1_nameprice))
        
 ######################## end of scrapping data from gamesman ################# 

 ########################## scrapping data from jb-hifi #########################
	print("Updating prices from site: Jb-hifi")
	s2_name=list()
	s2_price=list()
	s2_len=list()
	soup = BeautifulSoup(s2_html,'html.parser')
	s2_data=soup.findAll("h4")
	for s2_item in s2_data:
		s2_r=s2_item.get_text()
		s2_name.append(s2_r)
	s2_data=soup.findAll("span",{"class": "amount regular"})
	for s2_item in s2_data:
		s2_a=s2_item.get_text() 
		for s2_s in s2_a.split(): 
			if s2_s.isdigit():
				si='$'+str(s2_s)
				s2_price.append(si)      
	s2_x=len(s2_name)
	for i in range(s2_x):
		s2_y='Jb hi-fi'
		s2_len.append(s2_y)
	s2_nameprice=tuple(zip(s2_name,s2_price,s2_len))
	s2_sortedlist=list(set(s2_nameprice)) 
       
######################## ending scrapping from jb-hifi#######################

	combinelist=s1_sortedlist+s2_sortedlist

###################### Creating a table ####################	 
	c.execute('''CREATE TABLE IF NOT EXISTS user
		             (id INTEGER PRIMARY KEY,name TEXT,store TEXT,UNIQUE(name,store))''')
	c.execute('''CREATE TABLE IF NOT EXISTS userprice
		             (price INTEGER ,dt DATETIME, db DATETIME, tid INTEGER, FOREIGN KEY(tid) REFERENCES user(id))''')

############################## Inserting values in table#####################
	for items in combinelist:
		c.execute("INSERT OR IGNORE INTO user(name,store) VALUES(?,?);",[items[0],items[2]])
		c.execute("SELECT id FROM user WHERE (name = ? AND store = ?)", [items[0],items[2]])
		d = c.fetchone()[0]
		c.execute("INSERT OR IGNORE INTO userprice(price,dt,db,tid) VALUES(?,strftime('%H:%M', datetime('now', 'localtime')),strftime('%d/%m/%Y', datetime('now', 'localtime')),?);",[items[1],d])
		  
	 
elif par1=="search":
	par2=sys.argv[2]
	print("('ID', 'NAME', 'STORE')")
	c.execute("SELECT DISTINCT id, name,store,userprice.price FROM user join userprice on user.id=userprice.tid where name like '%"+str(par2)+"%'")
	rows = c.fetchall()
	for row in rows:
		print (row)

elif par1=="history":
	par2=sys.argv[2]
	print("('DATE','TIME','PRICE')")
	c.execute("SELECT userprice.db,userprice.dt,userprice.price FROM user join userprice on user.id=userprice.tid where user.id="+str(par2)+"")
	rows = c.fetchall()
	for row in rows:
		print (row)

else:
	print("Wrong Input.")


conn.commit()
conn.close()
