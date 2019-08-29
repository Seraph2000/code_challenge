import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm

app = Flask(__name__)

conn = sqlite3.connect('boxoffice.sqlite')
cursor = conn.cursor()

def db_fetch_all_names():
    cursor.execute(
        "fullname",
        )
    return cursor.fetchall()

def db_interact(a, b, c):
    cursor.execute(
        "insert into boxoffice (fullname, purchased_ticket, ticket_id) values (%s, %b, %d)",
        (a, b, c)
        )
    cursor.commit()

print("Opened database successfully")


## create table
# cursor.execute(
#     '''CREATE TABLE tickets(
#         fullname TEXT NOT NULL,
#         purchased_ticket BOOL,
#         ticket_id INT);
#     '''
# )
# cursor.close()

print("table created")

#  /register
@app.route('/register', methods=['POST', 'GET'])
def register():
    conn = sqlite3.connect('boxoffice.sqlite')
    cursor = conn.cursor()
    message="Please enter your full name to register"
    fullname = ''
    
    if request.method == 'POST':
        fullname=request.form['name']
        if fullname != '':
            print(type(fullname))
            print("fullname: {}".format(fullname))
            cursor.execute("SELECT fullname FROM tickets")  # execute a simple SQL select query
            names = cursor.fetchall()
            names = [e[0] for i, e in enumerate(names)]
            print("we're testing if user already registered: {}".format(names))
            if fullname in names:
                message="Sorry, that user is already taken!"
                return render_template('register.html', message=message)
            else:
                cursor.execute(
                    "insert into tickets (fullname, purchased_ticket, ticket_id) values (?,?,?)",
                    (fullname, False, 0)
                )
                conn.commit()
                return redirect(url_for('reserve', fullname=fullname, message=message, names=names))
        return render_template('register.html', fullname=fullname)
        
    else:
        return render_template('register.html')

# /reserve
@app.route('/reserve', methods=['POST', 'GET'])
def reserve():
    ticket_id = 0
    conn = sqlite3.connect('boxoffice.sqlite')
    cursor = conn.cursor()
    fullname = request.args.get('fullname')
    message = request.args.get('message')
    cursor.execute("SELECT ticket_id FROM tickets")
    ids = cursor.fetchall()
    total = len(ids)
    if request.method == 'POST':
        if total <= 5:
            ticket_id = int(total + 1)
            cursor.execute(
                "UPDATE tickets SET purchased_ticket=?, ticket_id=? WHERE fullname=?",
                (True, ticket_id, fullname)
            )
            conn.commit()
            message="Your purchase was successful!"
            return redirect(url_for('purchased', message=message))
        else:
            message="Sorry tickets sold out!"
            return redirect(url_for('purchased', message=message))
    elif request.method == 'GET':
        return render_template('reserve.html', fullname=fullname, total=total)

# /purchased
@app.route('/purchased', methods=['GET'])
def purchased():
    message = request.args.get('message', None)
    return render_template('purchased.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
    cursor.close()
