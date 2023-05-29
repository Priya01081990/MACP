
import pandas as pd
from login_functionality import chcek_login, get_user_data_by_username
from flask import Flask, render_template, request, redirect, session, url_for



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load user data from CSV file using Pandas
        USERS_DATABASE = pd.read_csv('users.csv')

        if not chcek_login(db=USERS_DATABASE, username=username, password=password):    # Check if user exists in the
            # loaded user data
            user_data = get_user_data_by_username(db=USERS_DATABASE, username=username)
            session['user_data'] = user_data
            return render_template('home.html', name=user_data.get("name"), user_data=user_data)
        else:
            msg = 'Invalid credentials. Please try again.'
            return render_template('error.html', msg=msg)

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # Load user data from CSV file using Pandas
        USERS_DATABASE = pd.read_csv('users.csv')

        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']

        # Check if the username already exists
        if username in USERS_DATABASE['username'].tolist():
            error = 'Username already exists. Please choose a different username.'
            return render_template('error.html', error=error)
        else:
            # Add new user to the loaded data
            new_user = pd.DataFrame(
                [{
                    'username': username,
                    'password': password,
                    'name': name,
                    'contact': contact,
                    'address': address
                 }]
            )
            users_data = pd.concat([USERS_DATABASE, new_user], ignore_index=True)
            users_data.to_csv('users.csv', index=False)
        return redirect('/')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user_data', None)
    return redirect('/')


if __name__ == '__main__':
    app.run()
