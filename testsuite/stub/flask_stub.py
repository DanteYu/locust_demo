from flask import Flask

server_port = 5000
app = Flask(__name__)

@app.route('/')
def hello_world():

    response = {"a": {"b": 2, "c": 3}}

    return response

if __name__ == "__main__":
    app.run('0.0.0.0', port=server_port)