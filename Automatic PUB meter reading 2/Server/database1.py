import sqlite3
import sys
 
connect = None
try:
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()    
    cursor.execute('SELECT SQLITE_VERSION()')
	
    data = cursor.fetchone()
    print "SQLite version: %s" % data                
except sqlite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if connection:
        connection.close()