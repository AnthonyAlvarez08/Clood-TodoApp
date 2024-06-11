from flask import Flask, render_template, url_for, request
import config
import boto3
import DBWrapper

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
dbConn = None


"""

==============things that route to front end==============

"""
@app.get('/')
@app.get('/home')
def home() -> str:

    # get in the habit of explicitly returning the return status on these I guess
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin() -> str:
    return render_template('signin.html')



@app.route('/taskview')
def taskview() -> str:
    return render_template('task_view.html')



"""

==============Backend stuff==============

"""

@app.get('/heartbeat')
def heartbeat() -> dict:
    return {'alive': True}, 200

"""
User management
"""


# create user


# delete user


# sign in


# sign out


"""
item list management
"""

# create new task
@app.post('/newtask')
def newtask():


    # will not work because I haven't set up the database yet lol

    try:
        title = request.values['task_title']
        description = request.values['description']
        due_date = request.values['due_date']
        repeats = request.values['repeats']
        

        sql = 'instert into tasks (userid, task_title, description, due_date, repeats) values (%s, %s, %s, %s, %s)';


        res = DBWrapper.perform_action(dbConn, sql, 
            [userid, title, description, due_date, repeats])



        # get the task id of the thing
        sql = "SELECT LAST_INSERT_ID();"
        row = DBWrapper.retrieve_one_row(dbConn, sql)
        taskid = row[0]


        return {'status': success, 'taskid': taskid}, 200
    except Exception as ex:
        return {'error': str(ex.with_traceback)}, 400



# delete taks(s)


# complete task(s)



# edit task
# basically just delete and reinsert lol


if __name__ == '__main__':
    # dbConn = DBWrapper.get_dbConn(config.EndPoint, config.PortNum, config.Username, config.dbPass, config.dbName)
    app.run(host=config.HOST, port=config.PORT, debug=True)