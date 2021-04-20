from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, select

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Creates database class
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(32), nullable=False)


def __repr__(self):
    return '<User %r>' % self.id

#Homepage
@app.route('/')
def index():
    link1 = 'btn btn-outline-primary style=margin-right: 10px;'
    link2 = 'btn btn-outline-primary'
    value1 = 'Log in'
    value2 = 'Sign Up'
    return render_template('index.html', link1=link1, link2 = link2, value1=value1, value2=value2)
#Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Get data from the form
        getUserName = request.form.get('name')
        getUserEmail = request.form.get('email')
        getUserPassword = request.form.get('password')
        #Check if data already exists in database
        authenticate = Users.query.filter(or_(Users.full_name==getUserName, Users.email==getUserEmail)).first()
        #If there's no data, set variables to None and return an error message
        if(getUserName=='' and getUserEmail=='' and getUserPassword==''):
            getUserName = None
            getUserEmail = None
            getUserEmail = None
            message= "Fields cannot be empty!"
            return render_template('register.html', message=message)
        elif(authenticate):
            #Check if account already exists and return message
            exists = "Account already exists!"
            return render_template('register.html', exists=exists)
        else:
            #If the data does not already exist in the database, add data to database 
            newUser = Users(full_name=getUserName, email=getUserEmail, password=getUserPassword)
            db.session.add(newUser)
            db.session.commit()
            message1 = "Account Created! Proceed to Log In"
            return render_template('register.html', message1=message1)         
    else:
        link1 = 'btn btn-outline-primary style=margin-right: 10px;'
        value1 = 'Log in'
        return render_template('register.html', link1=link1, value1=value1)

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #Get data from form
    if request.method == 'POST':
        getUserEmail = request.form.get('email')
        getUserPassword = request.form.get('password')
        #Check if the email matches the password in the database
        authenticate = Users.query.filter(and_(Users.email == getUserEmail, Users.password == getUserPassword)).first()
        if (authenticate):
            #If email and password match, return success page
            return redirect('/success')
        #If and empty form is returned set variables to None and return error message
        elif(getUserEmail=='' or getUserPassword==''):
            getUserEmail = None
            getUserPassword = None
            fields = "Fields cannot be empty!"
            return render_template('login.html', fields=fields) 
        else:
            #If password and email do not match return error message
            verify = "Incorrect email or password!"
            return render_template('login.html', verify=verify)
    else:
        link2 = 'btn btn-outline-primary'
        value2 = 'Sign Up'
        return render_template('login.html', link2=link2, value2=value2)

#Success page
@ app.route('/success')
def sucesss():
    link2 = 'btn btn-outline-primary'
    value2 = 'Log out'
    return render_template('success.html', link2=link2, value2=value2)


if __name__ == '__main__':
    app.run(debug=True)
