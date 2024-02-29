import os
from werkzeug.utils import secure_filename
from flask import Flask , Response, redirect, url_for, request, session, abort , flash , render_template
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
import pandas as pd 
import sqlite3



app = Flask(__name__)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# config
app.config.update(
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)

# create some users with ids 1 to 20       
user = User(0)



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# some protected url
@app.route('/', methods=['GET', 'POST'])
@login_required
def root():
    df = pd.DataFrame()
    numberOfRows, prize_slice  = " " , " " 
    
    if request.method == 'POST':
        try : 
            table_name = request.form.get('table_name')
            count_winner =  int(request.form.get('count_winner'))
            numberOfRows , prize_slice = Find_prize_slice(table_name , count_winner )
            winner_id = int(request.form.get('winner_id'))
            winners_dict = Find_winner_id( table_name , numberOfRows , prize_slice ,winner_id )
            df = pd.DataFrame(winners_dict) 
            df = df.T
        except :
            pass            
    return render_template("base_lottery.html" , numberOfRows=numberOfRows  , prize_slice=prize_slice ,
                                        column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
    

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if username == "sobhan" and password == "1234" :
            login_user(user)
            return redirect("/")
        else:
            return abort(401)
    else:
        return render_template("login.html")


@app.route('/database', methods=['GET', 'POST'])
@login_required
def db()  :
    df = table_view_of_db("PEOPLE")
    if request.method == 'POST':
        try :
            table_name = request.form.get('table_name')
            df = table_view_of_db(table_name)
        except :
            return("error")
    return render_template("tables_db.html",column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route("/updatedb" ,  methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            session['info'] = 'No file part'
            return redirect(request.url)
        file = request.files['file']
        table_name = request.form.get('table_name')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            numberOfRows = update_db(file_path, table_name)
            session['info'] = f'imported {numberOfRows} people ' 
            os.remove(file_path)
            return redirect("/updatedb")
    info = session.get("info" , "")
    session['info'] =  ''
    return render_template("update_db.html",info=info)

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)



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
        winner_dict = {"winer index" : winer , "winner_name"  :  winner_name  , "winer_phone" : winer_phone }
        winners_dict[winer] = winner_dict
    return (winners_dict)
    




if __name__ ==  "__main__":
    app.run(host="0.0.0.0", port="12345",debug=True)