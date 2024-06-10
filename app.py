from flask import Flask, render_template, url_for
import config
import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY



@app.get('/')
@app.get('/home')
def home() -> str:

    # get in the habit of explicitly returning the return status on these I guess
    return "Hello World\nThere is nothing here", 200

@app.get('/heartbeat')
def heartbeat() -> dict:
    return {'alive': True}, 200



if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=True)