from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from users import User

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = User()
        user.register_user(first_name, last_name, email, username, password)

        return redirect(url_for('home'))
    else:
        return render_template('register.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User()
        #Define boolean login
        login = user.login_user(username, password)

        if  login is True:
            #If username and password match, redirect user to his/her dashboard
            return render_template('/dashboard')
        else:
            #If username or password is incorrect, redirect to login page and display "Username/password incorrect"
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)