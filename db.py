import pandas as pd 
import sqlite3
import config

def table_view_of_db(table_name) :
        '''this function  findshow all of the memeber of db  '''
        con = sqlite3.connect(config.DATABASE_PATH)
        sql_query = pd.read_sql(f"SELECT * FROM {table_name}", con)
        df = pd.DataFrame(sql_query)
        con.commit()
        con.close()
        return (df)

def update_db(path ,table_name ,re_ap )  :
    """update database from xlsx file  """
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    #upload new data to db 
    df = pd.read_excel(path)
    df.to_sql(name=table_name,con=con,if_exists=re_ap ,index=False)
    con.commit()
    cur.execute(f"SELECT Count(*) FROM {table_name}" )
    numberOfRows = cur.fetchone()[0]
    con.commit()
    con.close()
    return (numberOfRows)

def Find_prize_slice(table_name , count_winner ) :
    '''this function  find winner by count of prize in table '''
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT Count() FROM %s" % table_name )
    numberOfRows = cur.fetchone()[0]
    con.commit()
    con.close()
    prize_slice = numberOfRows /  count_winner
    prize_slice = int(prize_slice)
    return (numberOfRows, prize_slice)

def find_winner_from_db(table_name , id) :
    '''this function  find winner by count of prize in table '''
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    rowsQuery = f"SELECT * FROM {table_name} where ROW='{id}'"
    cur.execute(rowsQuery)
    rows = cur.fetchall()
    con.commit()
    con.close()
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
    con = sqlite3.connect(config.DATABASE_PATH)
    cur = con.cursor()
    Query = "SELECT name FROM sqlite_master WHERE type='table';"
    cur.execute(Query)
    tables_names  = cur.fetchall()
    con.commit()
    con.close()
    table_list  = []
    for table in tables_names :
        table_list.append(table[0])
    return(table_list)

def delete_table(table_name):
    try :
        '''this function  delete table from db   '''
        con = sqlite3.connect(config.DATABASE_PATH)
        cur = con.cursor()
        sql_query = f"DROP TABLE {table_name} ;"
        cur.execute(sql_query)
        con.commit()
        con.close()
        Message = "data deleted  successfully"
    except :
        Message = "error"
    return Message