
if __name__ == '__main__':
	import DBWrapper
	from user import User
else:
	# ran into some testing shennanigans
	# have to import it like this since it is called from the main file
	import data.DBWrapper as DBWrapper
	from data.user import User

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
		self.taskid = 0
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



		# find if user exists in the database
		temp = Task.GetTaskById(dbConn, task.taskid)

		if task.userid == 0:
			raise Exception('Task must be attached to user')

		if temp == None:
			# means we have to insert
			sql = 'INSERT INTO tasks (userid, title, details, due_date, repeats, priority, progress) VALUES (%s, %s, %s, %s, %s, %s, %s);'


			res = DBWrapper.perform_action(dbConn, sql, [
				task.userid,
				task.title,
				task.details,  
				task.due_date,
				task.repeats,
				task.priority,
				task.progress
				
			])
        

        	# get the task id of the thing
			sql = "SELECT LAST_INSERT_ID();"
			row = DBWrapper.retrieve_one_row(dbConn, sql)
			taskid = row[0]

			task.taskid = taskid

			return task
		else:
			# means we have to update

			sql = 'UPDATE tasks SET title = %s, details = %s, due_date = %s, repeats = %s, priority = %s, progress = %s WHERE taskid = %s;'
			res = DBWrapper.perform_action(dbConn, sql, [
				task.title,
				task.details,  
				task.due_date,
				task.repeats,
				task.priority,
				task.progress,
				task.taskid
			])

			edited_task = Task.GetTaskById(dbConn, task.taskid)
			return edited_task

			

	@staticmethod
	def GetTaskById(dbConn, taskid : int) -> "Task":
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


		#  being = 0 means it doesn't exist
		if 0 == taskid:
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


	@staticmethod
	def GetOneUsersTask(dbConn, userid : int) -> list['Task']:
		"""
		Deletes specified user

		Parameters
		----------
		dbConn	: database connection
		user 	: user whose tasks we're retrieving


		Returns
		----------
		list of task objects that belong to the user
		"""

		try:
			sql = 'SELECT * FROM tasks WHERE userid= %s'
			rows = DBWrapper.retrieve_all_rows(dbConn, sql, [userid])

			res = []

			for row in rows:

				taskid, userid, title, details, due_date, repeats, priority, progress = row


				tmp = Task(title, userid)
				tmp.taskid = taskid
				tmp.details = details
				tmp.due_date = str(due_date)
				tmp.repeats = repeats
				tmp.priority = priority
				tmp.progress = progress

				res.append(tmp)

			return res

		except Exception as ex:
			print(str(ex))
			return []