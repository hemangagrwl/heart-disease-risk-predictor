from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load model and features
model = joblib.load("heart_disease_model.pkl")
feature_names = joblib.load("feature_columns.pkl")

# Health ranges (normal values)
HEALTH_RANGES = {
    'age': {'min': 20, 'max': 80, 'unit': 'years'},
    'trestbps': {'min': 90, 'max': 120, 'unit': 'mm Hg', 'name': 'Blood Pressure'},
    'chol': {'min': 125, 'max': 200, 'unit': 'mg/dl', 'name': 'Cholesterol'},
    'thalach': {'min': 60, 'max': 100, 'unit': 'bpm', 'name': 'Resting Heart Rate'}
}

def get_risk_zone(probability):
    """Determine risk zone based on probability"""
    if probability < 25:
        return {'zone': 'VERY LOW RISK', 'color': '#27ae60', 'icon': '✅'}
    elif probability < 50:
        return {'zone': 'MODERATE RISK', 'color': '#f39c12', 'icon': '⚠️'}
    elif probability < 75:
        return {'zone': 'HIGH RISK', 'color': '#e67e22', 'icon': '⚠️'}
    else:
        return {'zone': 'CRITICAL RISK', 'color': '#e74c3c', 'icon': '🚨'}

def get_feature_importance(input_data):
    """Get top contributing factors"""
    contributions = []
    
    # Check key risk factors
    age = input_data['age'][0]
    chol = input_data['chol'][0]
    trestbps = input_data['trestbps'][0]
    cp = input_data['cp'][0]
    
    if age > 55:
        contributions.append({'factor': 'Age', 'impact': 'high', 'value': f'{age} years'})
    if chol > 240:
        contributions.append({'factor': 'Cholesterol', 'impact': 'high', 'value': f'{chol} mg/dl'})
    elif chol > 200:
        contributions.append({'factor': 'Cholesterol', 'impact': 'medium', 'value': f'{chol} mg/dl'})
    if trestbps > 140:
        contributions.append({'factor': 'Blood Pressure', 'impact': 'high', 'value': f'{trestbps} mm Hg'})
    elif trestbps > 120:
        contributions.append({'factor': 'Blood Pressure', 'impact': 'medium', 'value': f'{trestbps} mm Hg'})
    if cp == 3:
        contributions.append({'factor': 'Chest Pain (Asymptomatic)', 'impact': 'high', 'value': 'Present'})
    
    return contributions[:5]  # Top 5

def get_recommendations(probability, input_data):
    """Generate personalized health recommendations"""
    recommendations = []
    
    age = input_data['age'][0]
    chol = input_data['chol'][0]
    trestbps = input_data['trestbps'][0]
    thalach = input_data['thalach'][0]
    
    if probability > 50:
        recommendations.append('🏥 Consult a cardiologist immediately for comprehensive evaluation')
    
    if chol > 200:
        recommendations.append('🥗 Reduce saturated fats and increase fiber intake (fruits, vegetables, whole grains)')
        recommendations.append('💊 Discuss cholesterol-lowering medications with your doctor')
    
    if trestbps > 130:
        recommendations.append('🧂 Reduce sodium intake (aim for less than 2,300mg per day)')
        recommendations.append('🏃 Regular aerobic exercise (30 minutes, 5 days/week)')
    
    if age > 50:
        recommendations.append('📅 Schedule annual cardiac health screenings')
    
    if thalach < 100:
        recommendations.append('💪 Improve cardiovascular fitness through regular exercise')
    
    if probability < 25:
        recommendations.append('✅ Maintain your healthy lifestyle with balanced diet and regular exercise')
    
    recommendations.append('🚭 Avoid smoking and limit alcohol consumption')
    recommendations.append('😴 Ensure 7-8 hours of quality sleep each night')
    
    return recommendations[:6]  # Top 6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = {
            "age": [float(request.form.get('age'))],
            "sex": [int(request.form.get('sex'))],
            "cp": [int(request.form.get('cp'))],
            "trestbps": [float(request.form.get('trestbps'))],
            "chol": [float(request.form.get('chol'))],
            "fbs": [int(request.form.get('fbs'))],
            "restecg": [int(request.form.get('restecg'))],
            "thalach": [float(request.form.get('thalach'))],
            "exang": [int(request.form.get('exang'))],
            "oldpeak": [float(request.form.get('oldpeak'))],
            "slope": [int(request.form.get('slope'))],
            "ca": [int(request.form.get('ca'))],
            "thal": [int(request.form.get('thal'))],
        }

        # Convert to DataFrame
        df_input = pd.DataFrame(data)
        df_input = pd.get_dummies(df_input)
        
        # Align with training features
        for col in feature_names:
            if col not in df_input.columns:
                df_input[col] = 0
        
        df_input = df_input[feature_names]
        
        # Predict
        prediction = model.predict(df_input)[0]
        probability = model.predict_proba(df_input)[0][1] * 100
        
        # Get enhanced features
        risk_zone = get_risk_zone(probability)
        risk_factors = get_feature_importance(data)
        recommendations = get_recommendations(probability, data)
        
        result = {
            'prediction': int(prediction),
            'probability': round(probability, 2),
            'risk_zone': risk_zone['zone'],
            'zone_color': risk_zone['color'],
            'zone_icon': risk_zone['icon'],
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'input_data': data
        }
        
        return render_template('index.html', result=result)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/about')
def about():
    """Model information page"""
    model_info = {
        'name': 'CatBoost Classifier',
        'accuracy': '85%',
        'dataset_size': '920 patients',
        'features': len(feature_names)
    }
    return render_template('about.html', model_info=model_info)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
