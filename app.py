from flask import Flask, render_template, request, redirect, make_response # pip install flask
from flaskext.mysql import MySQL # pip install flask-mysql
from gevent.pywsgi import WSGIServer # pip install gevent

# Create a Flask application instance
app = Flask(__name__)

# Configure the MySQL database settings
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = '<user>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<password>'
app.config['MYSQL_DATABASE_DB'] = '<database>' # Initialize the MySQL database connection
mysql = MySQL(app)

# Initialize the database connection
connect = mysql.connect()
cursor = connect.cursor()

# Define the default route, which redirects to the login page
@app.route('/')
def index():
    # retrieve cookie username
    _username = request.cookies.get('username')

    # Check if username is exist in the database
    if _username:
        sql = 'SELECT username FROM users WHERE username = %s' 
        data = _username
        cursor.execute(sql, data)
        result = cursor.fetchone()
        if result:
            return redirect('/tasks')
    return redirect('/login')

# Define the login route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get user input for email and password
    _email = request.values.get('email')
    _password = request.values.get('password')
    _wrong = False
    
    # SQL query to check if the user exist in the database
    sql = 'SELECT * FROM users WHERE email = %s AND password = %s' 
    data = _email, _password
    cursor.execute(sql, data)
    result = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            # Check if user credentials are correct and redirect to tasks page
            if _email == result[0][1] and _password == result[0][3]:
                response = make_response(redirect('/tasks'))
                response.set_cookie('email', _email)
                response.set_cookie('password', _password)
                response.set_cookie('username', result[0][2])
                return response
        except:
            # Handle incorrect credentials
            _wrong = True
            pass

    # Render the login template with optional error message
    return render_template('login.html', _wrong=_wrong, result=result, _email=_email)

# Define the registration route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input for email, username, and password
        _email = request.values.get('email')
        _username = request.values.get('username')
        _password = request.values.get('password')
        
        # SQL query to insert user data into the database and create table based on username
        user = 'INSERT INTO users (email, username, password) VALUES (%s, %s, %s)'
        table = 'CREATE TABLE {username}(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, todo VARCHAR(50) NOT NULL)'
        data = _email, _username, _password
        cursor.execute(user, data)
        cursor.execute(table.format(username = _username)) # using this method instead basic $s that just put string value literally with quotes
        connect.commit()
        
        # Redirect to the login page after successful registration
        return redirect('/login')
    
    # Render the registration template
    return render_template('register.html')

# Define the tasks route for displaying and managing tasks
@app.route('/tasks')
def get_all_tasks():
    # Get user cookies and logout reponse
    _username = request.cookies.get('username')
    _email = request.cookies.get('email')
    _password = request.cookies.get('password')
    _logout = request.values.get('logout')
    
    # retrieve data from users database
    user = 'SELECT * FROM users WHERE username = %s AND email = %s AND password = %s'
    parameter = _username, _email, _password
    cursor.execute(user, parameter)
    user_result = cursor.fetchone()

    # delete cookies when user logout
    if _logout:
        response = make_response(redirect('/login'))
        response.set_cookie('username', '', expires=0)
        response.set_cookie('email', '', expires=0)
        response.set_cookie('password', '', expires=0)
        return response
    
    if user_result:
        # Get user input for task addition and search
        _add = request.values.get('adding')
        _searchtask = request.values.get('search')

        # SQL query to retrieve all tasks
        sql = 'SELECT * FROM {user}'
        #parameter2 = _username
        cursor.execute(sql.format(user=_username))
        result = cursor.fetchall()

        # Render the tasks template with task list and search/add input
        return render_template('index.html', result=result, _searchtask=_searchtask, _add=_add)
    
    return redirect('/login')

# Define the add route for adding a new task
@app.route('/tasks/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        # Get user input for the task to add and user cookies
        _add = request.values.get('adding')
        _username = request.cookies.get('username')

        
        # SQL query to insert a new task into the database
        sql = 'INSERT INTO {user} (todo) VALUES (%s)'
        data = _add
        cursor.execute(sql.format(user=_username), data)
        connect.commit()
        
        # Redirect to the tasks page after adding the task
        return redirect('/tasks')
    return redirect('/tasks')

# Define the route to update a task by its ID
@app.route('/tasks/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if request.method == 'POST':
        # Get user input for the updated task and cookies
        _upmenu = request.values.get('upmenu')
        _username = request.cookies.get('username')

        # SQL query to update a task by its ID
        sql = 'UPDATE {user} SET todo = %s WHERE id = %s'
        data = _upmenu, task_id
        cursor.execute(sql.format(user=_username), data)
        connect.commit()
        
        # Redirect to the tasks page after updating the task
        return redirect('/tasks')

# Define the route to delete a task by its ID
@app.route('/tasks/delete/<int:task_id>')
def delete_task(task_id):
    # get user cookies
    _username = request.cookies.get('username')

    # SQL query to delete a task by its ID
    sql = 'DELETE FROM {user} WHERE id = %s'
    data = task_id
    cursor.execute(sql.format(user=_username), data)
    connect.commit()
    
    # Redirect to the tasks page after deleting the task
    return redirect('/tasks')

# Run the Flask application
if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 8989), app)
    server.serve_forever()
