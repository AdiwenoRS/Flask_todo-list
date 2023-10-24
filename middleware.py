from werkzeug.wrappers import Request, Response
import mysql.connector 

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'trualia ',
    database = 'to-do_list'
)

cursor = database.cursor()

cursor.execute("select * from users")
data = cursor.fetchall()

class Middleware():
    def __init__(self, app):
        self.app = app
        self.email = data
        self.password = data

    def __call__(self, environ, start_response):
        request = Request(environ)
        email = request.authorization['username']
        password = request.authorization['password']
        
        for i in range(len(data)):
            if email == self.email[i][1] and password == self.password[i][3]:
                environ['user'] = [
                    {"name": self.email[i][2]}
                ]

                return self.app(environ, start_response)
        
        res = Response('Authentication failed', mimetype='text/plain', status=401)
        return res(environ, start_response)