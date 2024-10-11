
if __name__ == '__main__':
	import DBWrapper
else:
	# ran into some testing shennanigans
	# have to import it like this since it is called from the main file
	import data.DBWrapper as DBWrapper

class Task:
	taskid : int
	userid : int
	title  : str
	details : str  
	due_date : str
	repeats  : str
	priority : int
	progress :str


	def __init__(self, title : str, userid : int):
		self.userid = userid
		self.title = title
		
		self.details = ''
		self.due_date = ''
		self.repeats = ''
		self.priority = -1
		self.progress = ''


	def __repr__(self) -> str:
		return f'{self.userid} ({self.taskid}): {self.title}'


	@staticmethod
	def Upsert(dbConn, task : "Task") -> "Task":
		"""
		Either updates given task in the database if it exists
		or it inserts a new task in the database

		update will not change either taskid nor userid

		Parameters
		----------
		task : task object to put in the databse

		Returns
		----------
		updated task object
		
  		"""

		return None


		# find if user exists in the database
		temp = Task.GetTaskById(dbConn, task.taskid)

		if temp == None or temp.userid == 0:
			# means we have to insert
			sql = 'INSERT INTO users (email, lastname, firstname, pwdhash) VALUES (%s, %s, %s, %s);'


			res = DBWrapper.perform_action(dbConn, sql, [user.email, user.lastname, user.firstname, user.pwdhash])
        

        	# get the task id of the thing
			sql = "SELECT LAST_INSERT_ID();"
			row = DBWrapper.retrieve_one_row(dbConn, sql)
			userid = row[0]

			task.userid = userid

			return task
		else:
			# means we have to update

			sql = 'UPDATE users SET lastname = %s, firstname = %s, pwdhash = %s WHERE userid = %s;'
			res = DBWrapper.perform_action(dbConn, sql, [user.lastname, user.firstname, user.pwdhash, user.userid])

			edited_user = Task.GetUserById(dbConn, task.taskid)
			return edited_user

			

	@staticmethod
	def GetTaskById(dbConn, taskid : int, userid : int) -> "Task":
		"""
		tries to find a user in the database by their email

		Parameters
		----------
		email : the email of the user you want to find
		
		Returns
		-------
		User object with the matching user if it exits
		returns None otherwise 

  		"""


		# either of these being = 0 means it doesn't exist
		if 0 in [taskid, userid]:
			return None

		try:
			sql = 'SELECT * FROM tasks WHERE taskid= %s'
			row = DBWrapper.retrieve_one_row(dbConn, sql, [taskid])

			if len(row) == 0:
				return None

			taskid, userid, title, details, due_date, repeats, priority, progress = row


			res = Task(title, userid)
			res.taskid = taskid
			res.details = details
			res.due_date = str(due_date)
			res.repeats = repeats
			res.priority = priority
			res.progress = progress

			return res
		except Exception as ex:
			print(str(ex))
			return None


	@staticmethod
	def DeleteTaskByID(dbConn, taskid : int):
		"""
		Deletes specified user

		Parameters
		----------
		dbConn	: database connection
		user 	: user object to put in the databse
		"""
		try:
			sql = 'DELETE FROM tasks WHERE taskid = %s'

			res = DBWrapper.perform_action(dbConn, sql, [taskid])
		except Exception as ex:
			print(str(ex))
			return
