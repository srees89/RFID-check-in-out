import sqlite3 as db
import os
from prettytable import from_db_cursor

conn = db.connect('cards.db')
cursor = conn.cursor()
menu = {}
menu['1']="Add Tag." 
menu['2']="Display All."
menu['3']="Find Tag"
menu['4']="Print to file"
menu['5']="main"
menu['9']="Exit"
while True:
  os.system('cls')
  print(34 * "=")
  print ("| Back End For RFID check-in/out |")
  print(34 * "=")
  print '\n'
  print(16 * "=")
  print ("| MAIN MENU |")
  print(16 * "=")
  options=menu.keys()
  options.sort()
  for entry in options:
   print entry, menu[entry]
  
  selection=raw_input("Please Select:") 
  if selection =='1': 
    tag = raw_input("Enter Tag: ")
    name = raw_input("Enter Name: ")
    cursor.execute("INSERT INTO CARDS (TAG, NAME, FLAG) values (?, ?, 0)", (tag, name))
    conn.commit()
    raw_input("Press any key to continue")
  elif selection == '2': 
   print "Opened database successfully \n"
   cursor = conn.execute("SELECT * FROM CARDS ORDER By TAG")
   pt = from_db_cursor(cursor)
   print pt
   raw_input()  
	 
  elif selection == '3':
     print "Opened database successfully"; 
     cursor = conn.execute("SELECT TAG, NAME FROM CARDS")
     Tag = raw_input("Please Scan your Tag: ")
     query = "SELECT * FROM CARDS WHERE TAG=?"
     cursor.execute(query, (Tag,))
     for row in cursor:
       print "Tag in database"
       print row[0] + " Is assigned too " + row [1], "\n"
     raw_input("Press any key to continue")
  
  elif selection == '4':
     print "Opened database successfully"; 
     cursor = conn.execute("SELECT TAG, NAME, FLAG FROM CARDS")
     cursor.execute("UPDATE CARDS SET FLAG=0 WHERE FLAG=1")
     print "reset complete"
     raw_input("Press any key to continue")
  elif selection =='7':
     cursor.execute('SELECT TAG, NAME, FLAG FROM CARDS ORDER BY TAG')
     pt = from_db_cursor(cursor)
     print pt
     tabstring = pt.get_string()
     output=open("export.txt","w")
     output.write("RFID DATABASE"+"\n")
     output.write(tabstring)
     output.close()
     print "Database has been exported as export.txt" 
     raw_input()
  elif selection == '5':#check-in|out
     print "Opened database successfully"; 
     cursor = conn.execute("SELECT TAG, NAME, FLAG FROM CARDS")
     while True:
       print(21 * "=")
       print ("| RFID check-in/out |")
       print(21 * "=")
       Tag = raw_input("Please Scan your Tag: ")
       q = "SELECT * FROM CARDS WHERE TAG=?"
       up = "UPDATE CARDS SET FLAG = (CASE WHEN FLAG=0 THEN 1 ELSE 0 END) WHERE TAG=?"
       id = "SELECT * FROM CARDS WHERE TAG=?"
       if Tag==9:
	    break
       cursor.execute(q, (Tag,))
       cursor.execute(up, (Tag,))
       conn.commit()
       for row in cursor.execute(id, (Tag,)):
        print row [1] + " has been checked " + ('in' if row[2] else 'out')
       raw_input("press enter")
       os.system('cls')
  elif selection == '9': #exit
    conn.close()
    print "database closed now exiting"
    break
  else: 
    print "Unknown Option Selected!" 
    raw_input("Press any key to continue")
    os.system('cls')
