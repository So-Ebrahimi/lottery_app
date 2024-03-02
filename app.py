import os
import pandas as pd 
import time
from datetime import  datetime
from werkzeug.utils import secure_filename
from flask import Flask , Response, redirect, url_for\
                            , request, session, abort , flash , render_template ,send_file
from flask_login import LoginManager, UserMixin, \
                            login_required, login_user, logout_user 
from  db  import *
import config

#init
app = Flask(__name__)

#local variable 
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

# config SECRET_KEY
app.config.update(
    SECRET_KEY = config.SECRET_KEY
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    """ A minimal and singleton user class used only for administrative tasks """
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)

# create some users with ids 1 to 20       
user = User(0)

def allowed_file(filename):
    """ checks the extension of the passed filename to be in the allowed extensions"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

#root
@app.route("/")
@login_required
def root():
    return redirect("/home")
    
# some protected url
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    '''home direct aff lottery web app '''
    tables_name = find_tables_name()
    df = pd.DataFrame()
    count_winner, numberOfRows, prize_slice  = "###" , "###" ,"###"
    if request.method == 'POST':
        try : 
            table = request.form.get('table_name')
            count_winner =  int(request.form.get('count_winner'))
            numberOfRows , prize_slice = Find_prize_slice(table , count_winner )
            winner_id = int(request.form.get('winner_id'))
            winners_dict = Find_winner_id( table , numberOfRows , prize_slice ,winner_id )
            df = pd.DataFrame(winners_dict) 
            df = df.T
            df.to_excel("backup_winners/" + table + "_" + 
                        str(datetime.now().strftime("%Y-%m-%d %H_%M_%S"))+".xlsx")
            df.to_excel("output.xlsx")
            time.sleep(3)
        except :
            pass            
    return render_template("home.html" , count_winner=count_winner ,  numberOfRows=numberOfRows  ,
                                        prize_slice=prize_slice    ,    tables_name = tables_name,
                                        column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    """ user login: only for admin user (system has no other user than admin)"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if username == config.CORRECT_USERNAME and password == config.CORRECT_PASSWORD :
            login_user(user)
            return redirect("/home")
        else:
            return abort(401)
    else:
        return render_template("login.html")

@app.route('/veiw_db', methods=['GET', 'POST'])
@login_required
def db()  :
    "view database tables"
    df = pd.DataFrame()
    tables_name = find_tables_name()
    if request.method == 'POST':
        try :
            table_name = request.form.get('table_name')
            df = table_view_of_db(table_name)
        except :
            return("error")
    return render_template("view_db.html",column_names=df.columns.values
                        ,tables_name = tables_name,  row_data=list(df.values.tolist()), zip=zip)

@app.route("/upload_db" ,  methods=['GET', 'POST'])
@login_required
def upload_file():
    '''update & upload new data to  database  '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            session['info'] = 'No file part'
            return redirect(request.url)
        file = request.files['file']
        table_name = request.form.get('table_name')
        re_ap = request.form.get('re_ap')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try :
                numberOfRows = update_db(file_path , table_name , re_ap)
                session['info'] = f'imported {numberOfRows} row  '
            except :
                session['info'] = 'Error with db '
            os.remove(file_path)
            return redirect("/upload_db")
    info = session.get("info" , "")
    session['info'] =  ''
    return render_template("update_db.html",info=info)

@app.route('/delete_db', methods=['GET', 'POST'])
@login_required
def delete_t()  :
    "delete database tables"
    Message =""
    tables_names = find_tables_name()
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        Message = delete_table(table_name)
    return render_template("delete_db.html", Message=Message ,tables_names = tables_names)

@app.route('/download', methods=['GET'])
def download_result():
    # File name
    file_name = "output.xlsx"

    # Send the file as a response
    try:
        return send_file(file_name, as_attachment=True)
    except Exception as e:
        return str(e)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# handle login failed
@app.errorhandler(401)
def error(e):
    return render_template("401.html")

# handle 404 error
@app.errorhandler(404)
def error(e):
    return render_template("404.html")

# handle 500 error
@app.errorhandler(500)
def error(e):
    return render_template("500.html")

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ ==  "__main__":
    app.run(host="0.0.0.0", port="12345",debug=True)