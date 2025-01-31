from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time

# Mock functions for IR and LLM
def get_ir_results(query):
    return [f"Match1{query}", "Match2", "Match3", "Match4", "Match5"]

def get_llm_response(query):
    time.sleep(2)  # Simulate delay
    return f"LLM Response for {query}"

app = Flask(
    __name__,
    static_folder="ui"
)
CORS(app)  # Enable CORS
socketio = SocketIO(app)

@app.route('/submit', methods=['POST'])
def submit_query():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Start processing in background thread
    threading.Thread(target=process_query, args=(query,)).start()
    
    return jsonify({"status": "Processing started"}), 202

@app.route('/', methods=['GET'])
def hi():
    return send_from_directory(
        directory="ui", 
        path="index.html"
    )

def process_query(query):
    ir_results = get_ir_results(query)
    socketio.emit('ir_results', {'ir_results': ir_results})
    
    llm_response = get_llm_response(query)
    socketio.emit('llm_response', {'llm_response': llm_response})

@socketio.on('connect')
def on_connect():
    print("Client connected")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)  # Adjust as needed