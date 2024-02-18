# import sqlite3

# # Connecting to sqlite
# # connection object
# connection_obj = sqlite3.connect('sql.db')

# # cursor object
# cursor_obj = connection_obj.cursor()

# # Drop the GEEK table if already exists.
# cursor_obj.execute("DROP TABLE IF EXISTS PEOPEL")

# # Creating table
# table = """ CREATE TABLE PEOPEL (
# 			NAME CHAR(25) NOT NULL,
# 			PHONE INT,
#             ROW INT 
# 		); """

# cursor_obj.execute(table)

# print("Table is Ready")

# # Close the connection
# connection_obj.close()

# import sqlite3
# import pandas as pd

# cxn = sqlite3.connect('sql.db')
# wb = pd.read_excel('data.xlsx')
# wb.to_sql(name='PEOPEL',con=cxn,if_exists='replace',index=True)
# cxn.commit()
# cxn.close()


import sqlite3 
  
# Connecting to sqlite 
# connection object 
connection_obj = sqlite3.connect('sql.db') 
  
# cursor object 
cursor_obj = connection_obj.cursor() 
  
# to select all column we will use 
statement = '''SELECT * FROM PEOPLE'''
  
cursor_obj.execute(statement) 
  
print("All the data") 
output = cursor_obj.fetchall() 
for row in output: 
  print(row) 
  
connection_obj.commit() 
  
# Close the connection 
connection_obj.close()


def update_db(path)  :
    """update database from xlsx file  """
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    # # Drop the PEOPLE  table if already exists.
    # curl.execute("DROP TABLE IF EXISTS PEOPLE")
    # # Creating table
    # table = """ CREATE TABLE PEOPLE (
    #         ROW INT,
	# 		NAME CHAR(25) NOT NULL,
	# 		PHONE INT   
	# 	); """

    # curl.execute(table)
    #upload new data to db 
    df = pd.read_excel(path)
    df.to_sql(name='PEOPLE',con=conn,if_exists='replace',index=True)
    conn.commit()
    conn.close()
    print("Db  updated suxcesfully")