import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings

class MLService:
    _instance = None
    _model = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MLService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        if self._model is None:
            self.load_model()
    def load_model(self):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'crop_prediction_model.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}. Please run training script first.")
        
        with open(model_path, 'rb') as f:
            self._model = pickle.load(f)
    @property
    def model(self):
        if self._model is None:
            self.load_model()
        return self._model
    def predict(self, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
        """
        Runs the RandomForest model and generates crop recommendation.
        Returns:
            dict containing predicted_crop, confidence_score, risk_level, recommendation, and alternative_crops
        """
        # Prepare inputs
        features = pd.DataFrame([{
            'Nitrogen': float(nitrogen),
            'Phosphorus': float(phosphorus),
            'Potassium': float(potassium),
            'Temperature': float(temperature),
            'Humidity': float(humidity),
            'pH': float(ph),
            'Rainfall': float(rainfall)
        }])
        # Predict probabilities
        probabilities = self.model.predict_proba(features)[0]
        classes = self.model.classes_
        # Sort classes by probability descending
        sorted_indices = np.argsort(probabilities)[::-1]
        
        # Top prediction
        predicted_crop = classes[sorted_indices[0]]
        confidence_score = float(probabilities[sorted_indices[0]] * 100)
        
        # Alternatives
        alternative_crops = []
        for idx in sorted_indices[1:3]: # Top 2 alternatives
            alternative_crops.append({
                'crop': str(classes[idx]),
                'confidence': round(float(probabilities[idx] * 100), 2)
            })
        # Risk level determination
        if confidence_score >= 85.0:
            risk_level = "Low"
        elif confidence_score >= 60.0:
            risk_level = "Medium"
        else:
            risk_level = "High"
        # Recommendation builder
        recommendation = self._generate_recommendation(
            predicted_crop, confidence_score, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
        )
        return {
            'predicted_crop': predicted_crop,
            'confidence_score': round(confidence_score, 2),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'alternative_crops': alternative_crops
        }
    def _generate_recommendation(self, crop, confidence, n, p, k, temp, humidity, ph, rainfall):
        recommendations = []
        
        # 1. Base climate suitability
        if confidence >= 85.0:
            recommendations.append(f"Highly suitable conditions detected for {crop}.")
        else:
            recommendations.append(f"Sub-optimal conditions for {crop}. Alternative crops might be safer.")
            
        # 2. pH specific rules
        if ph < 5.5:
            recommendations.append("Soil is highly acidic. Consider applying agricultural lime (calcium carbonate) to raise pH.")
        elif ph > 7.5:
            recommendations.append("Soil is alkaline. Apply sulfur or organic mulch to reduce pH to ideal levels.")
            
        # 3. Rainfall specific rules
        if rainfall < 80.0:
            if crop in ['Rice', 'Sugarcane']:
                recommendations.append("Extremely low rainfall for water-intensive crops. Supplemental drip or flood irrigation is mandatory.")
            else:
                recommendations.append("Low rainfall detected. Drip irrigation is recommended to sustain crop growth.")
        elif rainfall > 220.0 and crop not in ['Rice', 'Sugarcane']:
            recommendations.append("Heavy rainfall warning. Ensure adequate field drainage to prevent waterlogging and root rot.")
        # 4. NPK nutrient specific rules
        if n < 40.0:
            recommendations.append("Nitrogen depletion. Apply nitrogen-rich fertilizers (e.g. Urea) or plant leguminous cover crops.")
        if p < 30.0:
            recommendations.append("Phosphorus deficiency. Apply Superphosphate or bone meal to boost root development.")
        if k < 40.0:
            recommendations.append("Potassium deficiency. Apply Muriate of Potash to enhance disease resistance.")
        # Add a default general note if no warning recommendations
        if len(recommendations) == 1:
            recommendations.append("Nutrient levels and climatic variables fall within ideal physiological ranges. Continue standard crop care.")
        return " ".join(recommendations)