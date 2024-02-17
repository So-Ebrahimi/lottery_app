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
    # conn = sqlite3.connect(host='', port=0, timeout=None, source_address=None)
    # curl = conn.crusor()
    # curl.execute(sql)
    df = pd.read_excel(path)
    # df headers = index , name , phone 
    for  name , phone in df.iterrows() : 
        print( name , phone)


if __name__ ==  "__main__":
    update_db("data.xlsx")
    app.run(host="0.0.0.0", port="12345",debug=True)



