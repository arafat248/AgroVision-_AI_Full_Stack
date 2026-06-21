import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # Features: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall
    # Let's generate random values in realistic ranges
    n = np.random.uniform(10, 140, num_samples)
    p = np.random.uniform(5, 100, num_samples)
    k = np.random.uniform(5, 200, num_samples)
    temp = np.random.uniform(15, 40, num_samples)
    humidity = np.random.uniform(20, 100, num_samples)
    ph = np.random.uniform(4.5, 8.5, num_samples)
    rainfall = np.random.uniform(30, 300, num_samples)
    
    df = pd.DataFrame({
        'Nitrogen': n,
        'Phosphorus': p,
        'Potassium': k,
        'Temperature': temp,
        'Humidity': humidity,
        'pH': ph,
        'Rainfall': rainfall
    })
    
    # Assign crops based on simple rule heuristics to make the classifier learn patterns
    crops = []
    for idx, row in df.iterrows():
        # Heuristics:
        # Rice: high rainfall (>150), high humidity (>70)
        # Maize: moderate rainfall (80-150), moderate temp (20-30)
        # Wheat: low rainfall (50-100), cooler temp (<23)
        # Cotton: moderate rainfall (60-120), high temp (>25), high potassium (>50)
        # Coffee: high rainfall (>130), high potassium (>100), moderate temp (20-28)
        # Sugarcane: high rainfall (>150), high temp (>26), high phosphorus (>60)
        # Potato: low temp (<20), moderate rainfall (50-100)
        
        if row['Rainfall'] > 180 and row['Humidity'] > 75:
            crops.append('Rice')
        elif row['Rainfall'] > 150 and row['Temperature'] > 25:
            crops.append('Sugarcane')
        elif row['Rainfall'] > 120 and row['Potassium'] > 80:
            crops.append('Coffee')
        elif row['Temperature'] < 20:
            crops.append('Potato')
        elif row['Rainfall'] < 80 and row['Temperature'] < 24:
            crops.append('Wheat')
        elif row['Potassium'] > 60 and row['Temperature'] > 25:
            crops.append('Cotton')
        else:
            crops.append('Maize')
            
    df['Crop'] = crops
    return df
def train_and_save():
    print("Generating synthetic data...")
    df = generate_synthetic_data(1500)
    
    X = df[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']]
    y = df['Crop']
    
    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Check accuracy
    score = model.score(X, y)
    print(f"Model trained with training accuracy: {score * 100:.2f}%")
    
    # Ensure directory exists
    os.makedirs('ml_models', exist_ok=True)
    
    model_path = os.path.join('ml_models', 'crop_prediction_model.pkl')
    print(f"Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print("Model training and saving complete!")
if __name__ == '__main__':
    train_and_save()