from flask import Flask, render_template, url_for, request
import config
import boto3
import data.DBWrapper as DBWrapper
import auth
from data.task import Task
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
dbConn = None



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
        
        sql = 'select * from users;'
        rows = DBWrapper.retrieve_all_rows(dbConn, sql, [])

        return {'status': "success", 'users': rows}, 200
    except Exception as ex:
        return {'error': str(ex.with_traceback)}, 400

# create user
@app.post('/api/createuser')
def createuser() -> dict:
     # will not work because I haven't set up the database yet lol

    try:
        email = request.values['email']
        lastname = request.values['lastname']
        firstname = request.values['firstname']
        pwd = request.values['password']
        pwd = auth.hash_password(pwd)


        temp_usr = User(email, pwd, lastname, firstname)

        created = User.Upsert(dbConn, temp_usr)


        return {'status': "success", 'userid': created.userid}, 200
    except Exception as ex:
        return {'error': str(ex.with_traceback)}, 400

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
def authenticate_user():
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
@app.post('/api/newtask')
def newtask():

    try:

        title = request.values['title']
        details = request.values['details']
        due_date = request.values['due_date']
        repeats = request.values['repeats']
        priority = request.values['priority']
        userid = request.values['userid']
        

        temp = Task(title, userid)
        temp.details = details
        temp.due_date = due_date
        temp.repeats = repeats
        temp.priority = priority

        res = Task.Upsert(dbConn, temp)
        


        return {'status': "success", 'taskid': res.taskid}, 200
    except Exception as ex:
        return {'error': str(ex.with_traceback)}, 400



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
        return {'error': str(ex.with_traceback)}, 400


# delete task(s)
@app.post('/api/deletetask/<taskid>')
def deletetask(taskid : int) -> dict:

    try:

        taskid = int(taskid)
        # userid = request.values['userid']
        

        Task.DeleteTaskByID(dbConn, taskid)

        return {'status': "success"}, 200
    except Exception as ex:
        return {'error': str(ex.with_traceback)}, 400


# complete task(s)



# edit task
# basically just delete and reinsert lol


if __name__ == '__main__':
    dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
    app.run(host=config.HOST, port=config.PORT, debug=True)