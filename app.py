from flask import Flask 
import pandas as pd
import sqlite3


app = Flask(__name__)


@app.route("/test")
def main_page() : 
    """ this is test page """
    return "test"


def update_db(path)  :
    """update database from xlsx file  """
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    #upload new data to db 
    df = pd.read_excel(path)
    df.to_sql(name='PEOPLE',con=conn,if_exists='replace',index=False)
    conn.commit()
    conn.close()
    print("Db  updated suxcesfully")

def Find_prize_slice(table_name , count_winner ) :
    '''this function  find winner by count of prize in table '''
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    curl.execute("SELECT Count() FROM %s" % table_name )
    numberOfRows = curl.fetchone()[0]
    prize_slice = numberOfRows /  count_winner
    prize_slice = int(prize_slice)
    return (numberOfRows, prize_slice)


def find_winner_from_db(table_name , id) :
    '''this function  find winner by count of prize in table '''
    conn = sqlite3.connect("sql.db")
    curl = conn.cursor()
    rowsQuery = f"SELECT * FROM {table_name} where ROW='{id}'"
    print(rowsQuery)
    curl.execute(rowsQuery)
    rows = curl.fetchall()
    winner_name , winer_phone = rows[0][1] , rows[0][2]
    return (winner_name , winer_phone)



def Find_winner_id( table_name, numberOfRows , prize_slice ,winner_id ):
    """this function find winner id and  return it  """
    range_win = int(numberOfRows / prize_slice ) 
    winners_list = []
    start = 0 
    for winer  in range(range_win):
        id =  start + winner_id 
        winner_name , winer_phone = find_winner_from_db(table_name , id) 
        print("winner_name , winer_phone")



if __name__ ==  "__main__":
    update_db("data.xlsx")
    app.run(host="0.0.0.0", port="12345",debug=True)



