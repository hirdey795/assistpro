# @app.route('/save-class-info')

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/save-class-info', methods=['POST'])
def save_class_info():
    try:
        
        data = request.json
        
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        file_path = '../client/src/dataset/class_info.json' # Could subject to change if using a db
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        
        return jsonify({'message': 'Data saved successfully, '}), 200
    
    except Exception as e:
        
        return jsonify({'error': str(e)}), 500

@app.route('/college-classes-response', methods=['GET'])
def college_classes_response():
    
    """ 
    NOTE: Create function that returns all of the classes from colleges given the user's inputs
    """
    
    pass

if __name__ == '__main__':
    app.run(port=5000, debug=True)