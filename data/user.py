
if __name__ == '__main__':
	import DBWrapper
else:
	# ran into some testing shennanigans
	# have to import it like this since it is called from the main file
	import data.DBWrapper as DBWrapper

class User:
	"""
	Represents a user in the database

	"""
	userid : int
	email : str
	lastname : str
	firstname : str
	pwdhash : str



	def __init__(self, email : str, pwdhash : str, lastname : str, firstname: str):
		self.email = email
		self.pwdhash = pwdhash
		self.lastname = lastname
		self.firstname = firstname
		self.userid = 0


	def __repr__(self) -> str:
		return f'{self.email}: {self.lastname}, {self.firstname}'


	@staticmethod
	def Upsert(dbConn, user : "User") -> "User":
		"""
		Either updates given user in the database if it exists
		or it inserts a new user in the database

		update will not change neither email nor userid

		Parameters
		----------
		user : user object to put in the databse

		Returns
		----------
		updated user object
		
  		"""


		# find if user exists in the database
		temp = User.GetUserByEmail(dbConn, user.email)

		if temp == None or temp.userid == 0:
			# means we have to insert
			sql = 'INSERT INTO users (email, lastname, firstname, pwdhash) VALUES (%s, %s, %s, %s);'


			res = DBWrapper.perform_action(dbConn, sql, [user.email, user.lastname, user.firstname, user.pwdhash])
        

        	# get the task id of the thing
			sql = "SELECT LAST_INSERT_ID();"
			row = DBWrapper.retrieve_one_row(dbConn, sql)
			userid = row[0]

			user.userid = userid

			return user
		else:
			# means we have to update

			sql = 'UPDATE users SET lastname = %s, firstname = %s, pwdhash = %s WHERE userid = %s;'
			res = DBWrapper.perform_action(dbConn, sql, [user.lastname, user.firstname, user.pwdhash, user.userid])

			edited_user = User.GetUserByEmail(dbConn, user.email)
			return edited_user

			

	@staticmethod
	def GetUserByEmail(dbConn, email : str) -> "User":
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
		try:
			sql = 'SELECT * FROM users WHERE email= %s'
			row = DBWrapper.retrieve_one_row(dbConn, sql, [email])

			if len(row) == 0:
				return None

			userid, email, lastname, firstname, pwdhash = row


			res = User(email, pwdhash, lastname, firstname)
			res.userid = userid

			return res
		except Exception as ex:
			return None


	@staticmethod
	def DeleteUserByID(dbConn, userid : int):
		"""
		Deletes specified user

		Parameters
		----------
		dbConn	: database connection
		user 	: user object to put in the databse
		"""
		try:
			sql = 'DELETE FROM users WHERE userid = %s'

			res = DBWrapper.perform_action(dbConn, sql, [userid])
		except:
			return

	@staticmethod
	def DeleteUserByEmail(dbConn, email : int):
		"""
		Deletes specified user

		Parameters
		----------
		dbConn	: database connection
		user 	: user object to put in the databse
		"""
		try:
			sql = 'DELETE FROM users WHERE email = %s'

			res = DBWrapper.perform_action(dbConn, sql, [email])
		except:
			return


