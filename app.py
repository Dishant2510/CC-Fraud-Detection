from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
import os
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

# Load the trained model
model = joblib.load('fraud_detection_model_v2.pkl')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def interpret_confidence(score):
    """Return confidence level with more granular categories"""
    confidence = 1 - score  # Calculate confidence in prediction
    if confidence >= 0.9:
        return "high"
    elif confidence >= 0.75:
        return "medium_high"
    elif confidence >= 0.6:
        return "medium"
    elif confidence >= 0.4:
        return "low_medium"
    else:
        return "low"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the CSV file
            data = pd.read_csv(filepath)
            
            # Check if required columns exist
            required_columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
            if not all(col in data.columns for col in required_columns):
                return jsonify({'error': 'CSV file missing required columns'}), 400
            
            # Prepare features (drop 'Class' if it exists)
            if 'Class' in data.columns:
                data = data.drop('Class', axis=1)
            
            # Scale the Amount column
            scaler = StandardScaler()
            data['Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
            
            # Get predictions
            predictions = model.predict(data)
            probas = model.predict_proba(data)
            
            # Prepare response with improved confidence levels
            results = []
            for i in range(len(predictions)):
                result = {
                    'transaction_id': i,
                    'is_fraud': int(predictions[i]),
                    'confidence_score': float(probas[i][1]),
                    'confidence_level': interpret_confidence(probas[i][1]),
                    'amount': float(data.iloc[i]['Amount'])
                }
                results.append(result)
            
            return jsonify({'results': results})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)