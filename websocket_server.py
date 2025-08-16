from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@sock.route('/ws')
def echo(ws):
    while True:
        data = ws.receive()  # Receive message from client
        if data is None:
            break
        ws.send(f"Echo: {data}")  # Send back message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
