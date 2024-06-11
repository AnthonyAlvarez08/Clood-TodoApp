# I don't feel like writing alll the sql stuff myself so I will get it from my old university starter code


#
# datatier.py
#
# Executes SQL queries against a MySQL database.
#
# Original author:
#   Prof. Joe Hummel
#   Northwestern University
#

import pymysql


###################################################################
#
# get_dbConn:
#
# Opens and returns a connection object for interacting with a
# MySQL database.
#
def get_dbConn(endpoint, portnum, username, pwd, dbname):
  """
  Opens and returns a connection object for interacting 
  with a MySQL database

  Parameters
  ----------
  endpoint : machine name or IP address of server (string),
  portnum : server port # (integer),
  username : user name for login (string),
  pwd : user password for login (string),
  dbname : database name (string)

  Returns
  -------
  a connection object
  """
  try:
    dbConn = pymysql.connect(host=endpoint,
                             port=portnum,
                             user=username,
                             passwd=pwd,
                             database=dbname)

    return dbConn

  except Exception as err:
    print("datatier.get_dbConn() failed:")
    print(str(err))
    raise


##################################################################
#
# retrieve_one_row:
#
# Given a database connection and an SQL Select query,
# executes this query against the database and returns
# the first row (tuple) retrieved by the query (the tuple
# can be empty if the SELECT retrieved no data). The query
# can be parameterized using %s, in which case pass the
# values as a list [value1, value2, ...]
#
def retrieve_one_row(dbConn, sql, parameters=[]):
  """
  Executes an sql SELECT query against the database connection
  and returns the first row as a tuple

  Parameters
  __________
  dbConn : the database connection, 
  sql : the SQL SELECT query (can be parameterized with %s),
  parameters: optional list of values if parameterized

  Returns
  _______
  First row as a tuple, or () if SELECT retrieves no data
  """

  dbCursor = dbConn.cursor()

  try:
    dbCursor.execute(sql, parameters)
    row = dbCursor.fetchone()
    if row is None:  # executed successfully, but no data was retrieved
      return ()
    else:
      return row

  except Exception as err:
    print("datatier.retrieve_one_row() failed:")
    print(str(err))
    raise

  finally:
    dbCursor.close()


##################################################################
#
# retrieve_all_rows:
#
# Given a database connection and an SQL Select query,
# executes this query against the database and returns
# a list of rows (tuples) retrieved by the query. If the
# query retrieves no data, the empty list [] is returned.
# The query can be parameterized using %s, in which case
# pass the values as a list [value1, value2, ...]
#
def retrieve_all_rows(dbConn, sql, parameters=[]):
  """
  Executes an sql SELECT query against the database connection
  and returns all rows as a list of tuples

  Parameters
  __________
  dbConn : the database connection, 
  sql : the SQL SELECT query (can be parameterized with %s),
  parameters: optional list of values if parameterized

  Returns
  _______
  All rows as a list of tuples, or [] if SELECT retrieves no
  data
  """

  dbCursor = dbConn.cursor()

  try:
    dbCursor.execute(sql, parameters)
    rows = dbCursor.fetchall()
    if rows is None:  # executed successfully, but no data was retrieved
      return []
    else:
      return rows

  except Exception as err:
    print("datatier.retrieve_all_rows() failed:")
    print(str(err))
    raise

  finally:
    dbCursor.close()


###############################################################
#
# perform_action:
#
# Given a database connection and an SQL action query,
# executes an ACTION query and returns the number of rows
# modified; a return value of 0 means no rows were
# modified. Action queries are typically "insert",
# "update", "delete". The query can be parameterized
# using %s, in which case pass the values as a list
# [value1, value2, ...]
#
def perform_action(dbConn, sql, parameters=[]):
  """
  Executes an sql ACTION query against the database connection
  and returns number of rows modified

  Parameters
  __________
  dbConn : the database connection, 
  sql : the SQL SELECT query (can be parameterized with %s),
  parameters: optional list of values if parameterized

  Returns
  _______
  number of rows modified (0 is not an error but implies
  the query made no modifications)
  """

  dbCursor = dbConn.cursor()

  try:
    # try to execute, and if successful commit the changes
    # and return the # of rows modified by the query:
    dbCursor.execute(sql, parameters)
    dbConn.commit()
    return dbCursor.rowcount

  except Exception as err:
    # failed, rollback any possible changes and log error:
    dbConn.rollback()
    print("datatier.perform_action() failed:")
    print(str(err))
    raise

  finally:
    dbCursor.close()
