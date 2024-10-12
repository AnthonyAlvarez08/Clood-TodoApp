from flask import Flask, render_template, url_for, request, make_response, redirect
import boto3


# utility imports
import config
import auth

# data imports
import data.DBWrapper as DBWrapper
from data.task import Task
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName) # None
# dbConn = None



"""

there's gotta be a better way to organize this right?

TODO: actual authentication, temporarily just use cookies for now

https://www.pythonlore.com/sending-responses-in-flask-with-response-objects/ 
https://vivekmolkar.com/posts/working-with-flasks-request-and-response-objects/
https://tedboy.github.io/flask/generated/generated/flask.Response.html


here is some stuff on testing webservers locally
https://flask.palletsprojects.com/en/2.3.x/testing/
https://testdriven.io/blog/flask-pytest/



"""


"""

==============things that route to front end==============

TODO: basically whole front end lol

"""
@app.get('/')
@app.get('/home')
def home() -> str:
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin() -> str:

    if request.method == 'POST':
        res = make_response()

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup() -> str:
    return render_template('signup.html')



@app.route('/taskview')
def taskview() -> str:
    return render_template('task_view.html')



"""

==============Backend stuff==============

TODO: delete user, basically all task stuff


"""

@app.get('/heartbeat')
def heartbeat() -> dict:
    return {'alive': True}, 200

"""
User management
"""

@app.get('/api/allusers')
def getusers() -> dict:

    """
    Function that exists purely to test database access
    
    """
    try:
        
        sql = 'select email, firstname from users;'
        rows = DBWrapper.retrieve_all_rows(dbConn, sql, [])

        return {'status': "success", 'users': rows}, 200
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400

# create user
@app.post('/api/createuser')
def createuser() -> dict:
     # will not work because I haven't set up the database yet lol

    try:

        # I do want it to crash if it doesn't containe these fields so it is fine to do dict index
        email = request.values['email']
        lastname = request.values['lastname']
        firstname = request.values['firstname']
        pwd = request.values['password']
        pwd = auth.hash_password(pwd)


        temp_usr = User(email, pwd, lastname, firstname)

        created = User.Upsert(dbConn, temp_usr)


        return {'status': "success", 'userid': created.userid}, 200
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400

# delete user
@app.post('/api/deleteuser/<userid>')
def deleteuser(userid : int) -> dict:
    try:

        userid = int(userid)

        User.DeleteUserByID(userid)

        return {'status': 'success'}, 200

    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400


# sign in
@app.post('/api/signin/')
def sign_in():
    try:
        email = request.values['email']
        pwd = request.values['password']
        raise NotImplementedError
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400



# sign out


"""
item list management
"""

# create new task
@app.post('/api/newtask/<userid>')
def newtask(userid):

    try:

        title = request.values['title']
        details = request.values.get('details')
        due_date = request.values.get('due_date')
        repeats = request.values.get('repeats')
        priority = request.values.get('priority')
        # userid = request.values['userid']
        userid = int(userid)
        

        temp = Task(title, userid)
        temp.details = details
        temp.due_date = due_date
        temp.repeats = repeats
        temp.priority = priority

        res = Task.Upsert(dbConn, temp)
        


        return {'status': "success", 'taskid': res.taskid}, 200
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400



# get all of a user's tasks
@app.get('/api/gettasks/<userid>')
def gettasks(userid):
    try:

        # raise NotImplementedError
        userid = int(userid)
        rows = Task.GetOneUsersTask(dbConn, userid)
        # print(rows)

        return {'status': "success", 'tasks': [str(i) for i in rows]}, 200
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400


# delete task(s)
@app.post('/api/deletetask/<taskid>')
def deletetask(taskid : int) -> dict:

    try:

        taskid = int(taskid)
        # userid = request.values['userid']
        

        Task.DeleteTaskByID(dbConn, taskid)

        return {'status': "success"}, 200
    except Exception as ex:
        return {'error': str(ex), 'with traceback': str(ex.with_traceback)}, 400


# complete task(s)



# edit task
# basically just delete and reinsert lol


if __name__ == '__main__':
    # dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
    app.run(host=config.HOST, port=config.PORT, debug=True)