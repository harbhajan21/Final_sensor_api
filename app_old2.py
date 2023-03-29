# -*- coding: utf-8 -*-s
import logging
import json
from flask import Flask, jsonify,request
import os
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Set initial status to locked
status = 'LOCKED'

socketio = SocketIO(app)
# # define a function to handle incoming messages
# @sio.on('message')
# def handle_message(sid, data):
#     print('received message:', data)
#     sio.emit('message', data)


@app.route('/send', methods=['GET'])
def send_message():
    socketio.emit('response', {'data': 'This is a response from the server.'})
    response = {'message': 'This is an example response.'}
    return jsonify(response)

@socketio.on('message')
def handle_message(data):
    # Handle incoming messages from clients
    print('received message:', data)

@app.route('/status_value', methods=['GET']) 
def function1():
    return jsonify({'lock_status': status})
        
@app.route('/receive_resp', methods=['POST']) 
def function2():
    global status
    new_status = request.json.get('status')
    print("received", new_status)
    if new_status not in ['LOCKED', 'UNLOCKED']:
        return jsonify({'error': 'Invalid status'}), 400
    status = new_status
    return jsonify({'lock_status': status})

if __name__ == '__main__':
    print("Working dir = ", os.path.abspath(os.getcwd()))
    app.run(host="127.0.0.1", port="5003", threaded=True) 
    socketio.run(app, debug=True)    
            
