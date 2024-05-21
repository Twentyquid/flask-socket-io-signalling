from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")



@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("ack",{"rid": request.sid}, broadcast=True, include_self=False)


@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit({'id':request.sid},broadcast=True)

@socketio.on('call')
def handle_call(data):
    print("caller data is: ", data)
    emit("call",{'sid': data['sid'], "sdp": data['sdp']}, broadcast=True, include_self=False)
    
@socketio.on('answer')
def handle_answer(data):
    print("answer")
    emit("answer", data, broadcast=True, include_self=False)

@socketio.on('ready')
def handle_answer(data):
    print("ready")
    emit("ready", {"data":"data"},broadcast=True, include_self=False)

@socketio.on('offer')
def handle_offer(data):
    print("offer")
    emit("offer", data,broadcast=True, include_self=False)

@socketio.on('candidate')
def handle_offer(data):
    print("candidate", data)
    emit("candidate", data, broadcast=True, include_self=False)


@socketio.on("msg")
def handle_msg(data):
    print("msg is:", str(data))

# @socketio.on("answer")
# def handle_answer(data):
#     print("answer received")
#     emit("answer", {'sid': data['sid'], 'sdp': data['sdp']}, broadcast=True, include_self=False)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)