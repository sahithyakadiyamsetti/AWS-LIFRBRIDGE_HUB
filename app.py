from flask import Flask, render_template, jsonify
from flask import request
from flask import redirect
from flask import url_for  
from flask import flash
import mysql.connector
from datetime import datetime
from psutil import users
from flask import session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key" #Needed for flash msgs


# db_config = {
#     'host': 'database-bloodbank.crqmssgockvo.ap-south-1.rds.amazonaws.com',
#     'user': 'admin',
#     'password': 'Suryavarma123',
#     'database': 'bloodbank'
# }

#database config
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Sohel@1213',
    'database': 'blood'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      **db_config)


# Function to establish a database conn
def get_db_connection():
    # conn = mysql.connector.connect(**db_config)
    try:
        return cnxpool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error:{err}")
        return None
    
@app.route("/test-db-connection")
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")  # Test query to check connection
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"Connected to the database: {db_name[0]}"
    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['get', 'post'])
def register():
    if request.method == 'POST':
        # session.init_app(app)  # Initialize the session
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        blood_type = request.form['blood_type']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute("SELECT * FROM register WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("email already exists! Please log in Life Saver")
            return redirect(url_for('login', email= email)) # redirect to login page
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO register (fullname, email, password, blood_type) VALUES (%s,%s, %s, %s)",
                       (fullname, email, password, blood_type))
        conn.commit()
        cursor.close()
        conn.close()

        user_data = {
            'fullname': fullname,
            'email': email,
            'blood_type': blood_type
        }
        session['user'] = user_data
        flash("Registration successful! Please log in.")
        return redirect(url_for('confirm',user=user_data))

    return render_template("register.html")

@app.route('/confirm')
def confirm():
        user = session.get('user')
        return render_template('confirmation.html', user=user)


@app.route("/login", methods=['get', 'post'])
def login(email=None):
    if email is None:
        email = request.args.get('email')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify login credentials
        cursor.execute("SELECT * FROM register WHERE email = %s AND password = %s", 
                       (email, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            user_data = {
                'fullname' : user[4],
                'email': user[1],
            }
            session['user'] = user_data
            return redirect(url_for('dashboard', email=email))
        else:
            flash("Invalid login credentials!")
            return redirect(url_for('login'))

    return render_template("login.html")
    
import logging

@app.route("/dashboard") #, methods=['POST']
def dashboard():
    # if email is None:
    email = session.get('user')['email']
    #if request.method == 'POST' :
    # user = session.get('user')
    # email = user['email']
 
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user's blood group
    cursor.execute("SELECT fullname,email, blood_type FROM register WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    if user_data is None: # type: ignore
        logging.error("User data not found")
        return redirect(url_for('register'))
    
    user_data={
        'fullname' : user_data[0],
        'email' : user_data[1],
        'blood_type' : user_data[2]
    }

    # return redirect(url_for('req', email=email))    

    # Get blood requests for the user's blood group
    cursor.execute("SELECT * FROM request WHERE blood_type = %s and status = 'pending' ", (user_data['blood_type'],))
    requests = cursor.fetchall()

    request_data = []
    for request in requests:
        request_data.append({
            'date': request[2],  # assuming date is the first column
            'location': request[4],  # assuming location is the second column
            'urgency': request[5],  # assuming urgency is the third column
            'requester_id': request[1],  # assuming requester_id is the fourth column
            'request_id' : request[0]
        })


    cursor.close()
    conn.close()

    return render_template("dashboard.html",user=user_data, requests=request_data)
    
@app.route("/request", methods=['get', 'post'])
def req():
    user = session.get('user')
    if request.method == 'POST':
        location = request.form['location']
        blood_type = request.form['blood_type']
        urgency = request.form['urgency']
        # email = session.get('user')['email']
        # user=session.get('user')
        print(location,blood_type,urgency)
        # if user is None:
        #     flash("Error: User session parameter is missing!")
        #     return redirect(url_for('dashboard'))
        
        email=user['email']
        conn = get_db_connection()
        cursor = conn.cursor()
        print(conn)
        cursor.execute("Select id from register where email = %s", (email,))
        requester_id = cursor.fetchone()[0]
        # Insert the blood request into the database

        try:
            cursor.execute("INSERT INTO request (requester_id, location,blood_type, urgency) VALUES (%s, %s, %s, %s)",
                (requester_id, location,blood_type,urgency))
            conn.commit()
            flash("Blood request submitted!!")
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
            flash("An error occurred while submitting your request.")
        finally:
            cursor.close()
            conn.close()
        # requester_id = cursor.lastrowid # get the last inserted id
        # conn.commit()
        # cursor.close()
        # conn.close()

        # print(f"Request inserted with ID: {requester_id}")
        # flash("Blood request submitted!")
        return redirect(url_for('dashboard'))
    # user = session.get('user')

    

    return render_template("request.html",user=user, message = "Blood request submitted!")

def get_requester_data(requester_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM register WHERE id = %s", (requester_id,))
    requester_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return requester_data

def get_request_data(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM request WHERE id = %s", (request_id,))
    request_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return request_data

@app.route("/respond/<int:requester_id>/<int:request_id>")
def respond(requester_id, request_id):
    user = session.get('user')

    requester_data = get_requester_data(requester_id)
    request_data = get_request_data(request_id)

    # conn = get_db_connection()
    # cursor = conn.cursor()

    # cursor.execute("select *from request where id = %s", (requester_id,))
    # request_data = cursor.fetchone()

    if request_data is None or requester_data is None:
        return redirect (url_for('dashboard'))
    
    # cursor.execute("select * from register where id = %s", (request_data[1],))
    # requester_data = cursor.fetchone()

    # user = session.get('user')

    # cursor.close()
    # conn.close()

    request_data_dict = {
    'date': request_data[2],
    'location': request_data[4],
    'urgency': request_data[5]
    }

    requester_data_dict = {
    'full_name': requester_data[4],
    'email': requester_data[1],
    'blood_type': requester_data[3]
    }

    return render_template("respond.html",request_data=request_data_dict, requester_data=requester_data_dict, user=user, requester_id=requester_data[0], request_id = request_data[0])

@app.route("/donate-blood/<int:request_id>/<int:requester_id>", methods=["POST"])
def donate_blood( request_id, requester_id):
    # data = request.get_json()
    user = session.get('user')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE request SET status = 'donated' WHERE id = %s", ( request_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

# @app.route("/test-db-connection")
# def test_db_connection():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT DATABASE();")  # Test query to check connection
#         db_name = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         return f"Connected to the database: {db_name[0]}"
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
   

if __name__ == "__main__":
    app.run(debug=True)
