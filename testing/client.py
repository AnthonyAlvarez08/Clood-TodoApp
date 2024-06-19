# TODO: install stuff in venv

import requests
from getpass import getpass

API_ENDPOINT = 'http://localhost:5000/api/'


def new_user():

	firstname = input('First Name> ')
	lastname = input('Last Name> ')
	email = input('Email> ')
	password = getpass('password> ')

	body = {'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password}

	res = requests.post(API_ENDPOINT + 'createuser', json=body)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      body = res.json()
      print("Error message:", body)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # success, extract jobid:
    #
    body = res.json()

    print('Returned', str(body))