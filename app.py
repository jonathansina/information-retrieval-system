from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.type_hint import ControllerType
from src.pipelines.config.default import PIPELINE_DEFAULT_CONFIG
from src.pipelines.pipeline.builder import PipelineBuilder

# Mock functions for IR and LLM
def get_ir_results(query):
    pipeline = (
        PipelineBuilder(controller_type=ControllerType.INFERENCE)
        .with_logger("information-retrieval", "IRS", "development")
        .with_config(PIPELINE_DEFAULT_CONFIG)
        .with_preprocessor()
        .with_vectorizer()
        .with_vocabulary()
        .with_similarity()
        .with_evaluator()
        .build()
    )
    result = pipeline.run(query)
    
    response = [
        {
            "question": result["retrieved_question"][i],
            "answer": result["retrieved_answer"][i],
            "category": result["retrieved_category"][i],
        }
        for i in range(len(result["retrieved_question"]))
    ]
    
    return response

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
    ### EXAMPLE OF USAGE ###
    # 1. FIRST TRAIN THE MODEL WITH LOGGER ENABLED
    pipeline = (
        PipelineBuilder(controller_type=ControllerType.TRAINING)
        .with_logger("information-retrieval", "IRS", "development")
        .with_config(PIPELINE_DEFAULT_CONFIG)
        .with_preprocessor(True)
        .with_vectorizer(True)
        .with_vocabulary()
        .with_similarity()
        .with_evaluator(True)
        .build(True)
    )
    pipeline.run()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)  # Adjust as needed