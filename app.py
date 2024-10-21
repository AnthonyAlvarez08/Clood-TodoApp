from flask import Flask, render_template, url_for, request, make_response, redirect, Blueprint
import boto3
import json

# utility imports
import config
import auth
import utils.ParsersAndFinicky as pf

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
TODO: update database so that there is only unique emails ( also just reset every table, there is a lot of garbage in there)

https://www.pythonlore.com/sending-responses-in-flask-with-response-objects/ 
https://vivekmolkar.com/posts/working-with-flasks-request-and-response-objects/
https://tedboy.github.io/flask/generated/generated/flask.Response.html


stuff about authentication in flask
https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/ 
https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/

here is how we did it in cs310
file:///C:/Users/antho/school/northwestern/02_sophomore_year/spring/CS310/projects/proj4/project04.pdf 





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
        return {'error': str(ex)}, 400

# create user
@app.post('/api/createuser')
def createuser() -> dict:
     # will not work because I haven't set up the database yet lol

    try:


        data = pf.parse_request_data(request)


        # I do want it to crash if it doesn't containe these fields so it is fine to do dict index
        email = data['email']
        lastname = data['lastname']
        firstname = data['firstname']
        pwd = data['password']
        pwd = auth.hash_password(pwd)


        temp_usr = User(email, pwd, lastname, firstname)

        created = User.Upsert(dbConn, temp_usr)


        return {'status': "success", 'userid': created.userid}, 200
    except Exception as ex:
        return {'error': str(ex)}, 400

# delete user
@app.post('/api/deleteuser/<int:userid>')
@app.delete('/api/deleteuser/<int:userid>')
def deleteuser(userid : int) -> dict:
    try:

        userid = int(userid)

        User.DeleteUserByID(userid)

        return {'status': 'success'}, 200

    except Exception as ex:
        return {'error': str(ex)}, 400


# sign in
@app.post('/api/signin/')
def sign_in():
    try:

        data = pf.parse_request_data(request)

        email = data['email']
        pwd = data['password']

        

        user : User = User.GetUserByEmail(email)

        if auth.check_password(pwd, user.pwdhash):
            res = make_response({'status' : 'success'})
            
        else:
            return {'status' : 'Unauthorized, couldn\'t sign in'}, 401
    except Exception as ex:
        return {'error': str(ex)}, 400



# sign out


"""
item list management
"""

# create new task
@app.post('/api/newtask/<int:userid>')
def newtask(userid : int):

    try:

        data = pf.parse_request_data(request)

        title = data['title']
        details = data.get('details', '')
        due_date = data.get('due_date', '2100-01-01')
        repeats = data.get('repeats', '')
        priority = data.get('priority', 0)
        userid = int(userid)
        

        temp = Task(title, userid)
        temp.details = details
        temp.due_date = due_date
        temp.repeats = repeats
        temp.priority = priority

        res = Task.Upsert(dbConn, temp)
        
        return {'status': "success", 'taskid': res.taskid}, 200
    except Exception as ex:
        return {'error': str(ex)}, 400



# get all of a user's tasks
@app.get('/api/gettasks/<int:userid>')
def gettasks(userid : int):
    try:

        # raise NotImplementedError
        userid = int(userid)
        rows = Task.GetOneUsersTask(dbConn, userid)
        # print(rows)

        return {'status': 'success', 'tasks': [str(i) for i in rows]}, 200
    except Exception as ex:
        return {'error': str(ex)}, 400


# delete task(s)
@app.post('/api/deletetask/<int:taskid>')
@app.delete('/api/deletetask/<int:taskid>')
def deletetask(taskid : int) -> dict:

    try:

        taskid = int(taskid)
        # userid = request.values['userid']
        

        Task.DeleteTaskByID(dbConn, taskid)

        return {'status': "success"}, 200
    except Exception as ex:
        return {'error': str(ex)}, 400

# edit task
@app.post('/api/edittask/<int:userid>/<int:taskid>')
def edittask(userid : int, taskid : int):

    try:

        data = pf.parse_request_data(request)

        title = data['title']
        details = data.get('details', '')
        due_date = data.get('due_date', '2100-01-01')
        repeats = data.get('repeats', '')
        priority = data.get('priority', 0)
        userid = int(userid)
        

        temp = Task(title, userid)
        temp.details = details
        temp.due_date = due_date
        temp.repeats = repeats
        temp.priority = priority
        temp.taskid = int(taskid)

        res = Task.Upsert(dbConn, temp)
        
        return {'status': "success", 'taskid': res.taskid}, 200
    except Exception as ex:
        return {'error': str(ex)}, 400



if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=True)