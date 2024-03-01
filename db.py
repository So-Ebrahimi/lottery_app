import pandas as pd 
import sqlite3




def table_view_of_db(table_name) :
        '''this function  findshow all of the memeber of db  '''
        con = sqlite3.connect("sql.db")
        sql_query = pd.read_sql(f"SELECT * FROM {table_name}", con)
        df = pd.DataFrame(sql_query)
        con.commit()
        con.close()
        return (df)

def update_db(path ,table_name)  :
    """update database from xlsx file  """
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    #upload new data to db 
    df = pd.read_excel(path)
    df.to_sql(name=table_name,con=conn,if_exists='replace',index=False)
    conn.commit()
    curl.execute(f"SELECT Count(*) FROM {table_name}" )
    numberOfRows = curl.fetchone()[0]
    conn.commit()
    conn.close()
    print("Db  updated suxcesfully")
    return (numberOfRows)

def Find_prize_slice(table_name , count_winner ) :
    '''this function  find winner by count of prize in table '''
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    curl.execute("SELECT Count() FROM %s" % table_name )
    numberOfRows = curl.fetchone()[0]
    conn.commit()
    conn.close()
    prize_slice = numberOfRows /  count_winner
    prize_slice = int(prize_slice)
    return (numberOfRows, prize_slice)

def find_winner_from_db(table_name , id) :
    '''this function  find winner by count of prize in table '''
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    rowsQuery = f"SELECT * FROM {table_name} where ROW='{id}'"
    curl.execute(rowsQuery)
    rows = curl.fetchall()
    conn.commit()
    conn.close()
    winner_name , winer_phone = rows[0][1] , rows[0][2]
    return (winner_name , winer_phone)

def Find_winner_id( table_name, numberOfRows , prize_slice ,winner_id ):
    """this function find winner id and  return it  """
    range_win = int(numberOfRows / prize_slice ) 
    winners_dict = {}
    start = 0 
    for winer  in range(range_win):
        id =  start + winner_id 
        winner_name , winer_phone = find_winner_from_db(table_name , id) 
        start += prize_slice
        winner_dict = {"winer index" : winer + 1  , "winner_name"  :  winner_name  , "winer_phone" : winer_phone }
        winners_dict[winer] = winner_dict
    return (winners_dict)
    

def find_tables_name():
    '''this function return db tables name '''
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    Query = "SELECT name FROM sqlite_master WHERE type='table';"
    curl.execute(Query)
    tables_names  = curl.fetchall()
    conn.commit()
    conn.close()
    table_list  = []
    for table in tables_names :
        table_list.append(table[0])
    return(table_list)

def delete_table(table_name):
    try :
        '''this function  delete table from db   '''
        con = sqlite3.connect("sql.db")
        curl = con.cursor()
        sql_query = f"DROP TABLE {table_name} ;"
        curl.execute(sql_query)
        con.commit()
        con.close()
        Message = "data deleted  successfully"
    except :
        Message = "error"
    return Message