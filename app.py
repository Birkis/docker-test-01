from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data - we'll store it in memory for this example
mock_data = [
    {"id": 1, "name": "Item 1", "value": 100},
    {"id": 2, "name": "Item 2", "value": 200},
    {"id": 3, "name": "Item 3", "value": 300}
]

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

if __name__ == '__main__':
    app.run(debug=True)