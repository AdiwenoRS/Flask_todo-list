from flask import Flask, render_template, request, redirect, make_response # pip install flask
from flaskext.mysql import MySQL # pip install flask-mysql
from gevent.pywsgi import WSGIServer # pip install gevent

# Create a Flask application instance
app = Flask(__name__)

# Configure the MySQL database settings
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trualia '
app.config['MYSQL_DATABASE_DB'] = 'to-do_list' # Initialize the MySQL database connection
mysql = MySQL(app)

# Initialize the database connection
connect = mysql.connect()
cursor = connect.cursor()

# Define the default route, which redirects to the login page
@app.route('/')
def index():
    return redirect('/login')

# Define the login route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get user input for email and password
    _email = request.values.get('email')
    _password = request.values.get('password')
    _wrong = False
    
    # SQL query to check if the user exists in the database
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
                return response
        except:
            # Handle incorrect credentials
            _wrong = True
            pass

    # Render the login template with optional error message
    return render_template('login.html', _wrong=_wrong, result=result)

# Define the registration route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input for email, username, and password
        _email = request.values.get('email')
        _username = request.values.get('username')
        _password = request.values.get('password')
        
        # SQL query to insert user data into the database
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
    # Get user cookies
    _email = request.cookies.get('email')
    _password = request.cookies.get('password')
    user = 'SELECT * FROM users WHERE email = %s AND password = %s'
    parameter = _email, _password
    cursor.execute(user, parameter)
    user_result = cursor.fetchone()

    if user_result:
        # Get user input for task addition and search
        _add = request.values.get('adding')
        _searchtask = request.values.get('search')

        # SQL query to retrieve all tasks
        sql = 'SELECT * FROM adi'
        cursor.execute(sql)
        result = cursor.fetchall()

        # Render the tasks template with task list and search/add input
        return render_template('index.html', result=result, _searchtask=_searchtask, _add=_add)
    return redirect('/login')

# Define the add route for adding a new task
@app.route('/tasks/add', methods=['POST'])
def add():
    if request.method == 'POST':
        # Get user input for the task to add
        _add = request.values.get('adding')
        
        # SQL query to insert a new task into the database
        sql = 'INSERT INTO adi (todo) VALUES (%s)'
        data = _add
        cursor.execute(sql, data)
        connect.commit()
        
        # Redirect to the tasks page after adding the task
        return redirect('/tasks')

# Define the route to retrieve a single task by its ID
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    # SQL query to retrieve a single task by its ID
    sql = 'SELECT * FROM adi WHERE id = %s'
    data = task_id
    cursor.execute(sql, data)
    result = cursor.fetchall()
    
    # Render the tasks template with the single task
    return render_template('index.html', result=result)

# Define the route to update a task by its ID
@app.route('/tasks/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if request.method == 'POST':
        # Get user input for the updated task
        _upmenu = request.values.get('upmenu')
        
        # SQL query to update a task by its ID
        sql = 'UPDATE adi SET todo = %s WHERE id = %s'
        data = _upmenu, task_id
        cursor.execute(sql, data)
        connect.commit()
        
        # Redirect to the tasks page after updating the task
        return redirect('/tasks')

# Define the route to delete a task by its ID
@app.route('/tasks/delete/<int:task_id>')
def delete_task(task_id):
    # SQL query to delete a task by its ID
    sql = 'DELETE FROM adi WHERE id = %s'
    data = task_id
    cursor.execute(sql, data)
    connect.commit()
    
    # Redirect to the tasks page after deleting the task
    return redirect('/tasks')

# Run the Flask application
if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 8989), app)
    server.serve_forever()
