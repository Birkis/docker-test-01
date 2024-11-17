from flask import Flask, jsonify, request
from crewai.main import run as crew_run
import threading
import uuid
from queue import Queue

app = Flask(__name__)

# Mock data - we'll store it in memory for this example
mock_data = [
    {"id": 1, "name": "Item 1", "value": 100},
    {"id": 2, "name": "Item 2", "value": 200},
    {"id": 3, "name": "Item 3", "value": 300}
]

# Store for background jobs
job_results = {}

def process_crew_job(job_id, age, interests):
    try:
        result = crew_run(inputs={
            "age": age,
            "interests": interests
        })
        job_results[job_id] = {"status": "completed", "result": result}
    except Exception as e:
        job_results[job_id] = {"status": "failed", "error": str(e)}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(mock_data)

@app.route('/api/data', methods=['POST'])
def add_data():
    new_item = request.get_json()
    
    # Simple validation
    if not new_item or 'name' not in new_item or 'value' not in new_item:
        return jsonify({"error": "Invalid data"}), 400
    
    # Create new item with incremented ID
    new_id = max(item['id'] for item in mock_data) + 1
    new_item['id'] = new_id
    
    mock_data.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/crew/kickoff', methods=['POST'])
def kickoff_crew():
    try:
        data = request.get_json()
        if not data or 'age' not in data or 'interests' not in data:
            return jsonify({
                "error": "Missing required fields. Please provide 'age' and 'interests'"
            }), 400

        # Generate a unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        job_results[job_id] = {"status": "processing"}
        
        # Start background thread
        thread = threading.Thread(
            target=process_crew_job,
            args=(job_id, data['age'], data['interests'])
        )
        thread.start()
        
        return jsonify({
            "success": True,
            "job_id": job_id,
            "message": "Job started successfully"
        })
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/crew/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if job_id not in job_results:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify(job_results[job_id])

if __name__ == '__main__':
    app.run(debug=True)