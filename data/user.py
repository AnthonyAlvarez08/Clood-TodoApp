
if __name__ == '__main__':
	import DBWrapper
else:
	# ran into some testing shennanigans
	# have to import it like this since it is called from the main file
	import data.DBWrapper as DBWrapper

class User:
	userid : int
	email : str
	lastname : str
	firstname : str
	pwdhash : str


	def __init__(self, email : str, pwdhash : str, lastname : str, firstname: str):
		self.email = email,
		self.pwdhash = pwdhash
		self.lastname = lastname
		self.firstname = firstname
		self.userid = 0


	@classmethod
	def Upsert(dbConn, user):
		"""
		Either updates given user in the database if it exists
		or it inserts a new user in the database

		Parameters
		----------
		user : user object to put in the databse
		
  		"""


		# find if user exists in the database
		temp = User.GetUserByEmail(user.email)

		if temp == None:
			# means we have to insert
			pass
		else:
			# means we have to update
			pass

	@classmethod
	def GetUserByEmail(self, email: str):
		"""
		tries to find a user in the database by their email

		Parameters
		----------
		email : returns the email of the user
		
		Returns
		-------
		User object with the matching user if it exits
		returns None otherwise 
  		"""


		sql = 'SELECT * FROM users WHERE email= %s'
		row = DBWrapper.retrieve_one_row(dbConn, sql, [user.email])

