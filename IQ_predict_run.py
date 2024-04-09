import sys
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logs (0 = all logs, 1 = filter out INFO, 2 = filter out WARNING, 3 = filter out ERROR)
import warnings
warnings.filterwarnings('ignore')  # Suppress other warnings

# Load the model and vectorizer
model = load_model('iq_model.h5')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

def predict_iq(input_text):
    input_text_vect = vectorizer.transform([input_text]).toarray()
    predicted_iq = model.predict(input_text_vect)
    return predicted_iq[0][0]

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 name.py \"text here\"")
        sys.exit(1)
    
    input_text = sys.argv[1]
    predicted_iq = predict_iq(input_text)
    print(f"Predicted IQ Score: {predicted_iq}")
