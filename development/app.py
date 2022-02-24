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

        user = User(first_name, last_name, email, username, password)
        user.register_user()

        return redirect(url_for('home'))
        
    else:
        return render_template('register.html')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)