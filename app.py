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
    # Drop the PEOPLE  table if already exists.
    curl.execute("DROP TABLE IF EXISTS PEOPLE")
    # Creating table
    table = """ CREATE TABLE PEOPLE (
            ROW INT,
			NAME CHAR(25) NOT NULL,
			PHONE INT   
		); """

    curl.execute(table)
    #upload new data to db 
    df = pd.read_excel(path)
    df.to_sql(name='PEOPLE',con=conn,if_exists='replace',index=True)
    conn.commit()
    conn.close()
    print("Db  updated suxcesfully")



if __name__ ==  "__main__":
    update_db("data.xlsx")
    app.run(host="0.0.0.0", port="12345",debug=True)



