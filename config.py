from configparser import ConfigParser


# define the port and host just incase I change it in the future, for now localhost 5000
HOST = '127.0.0.1'
PORT = 5000
SECRET_KEY = 'fdasf'

config_file = 'AppConfig.ini'

configur = ConfigParser()
configur.read(config_file)
SECRET_KEY = configur.get('Secrets', 'secret_key')