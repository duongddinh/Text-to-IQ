import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error
from kerastuner.tuners import RandomSearch
from tensorflow.keras.callbacks import EarlyStopping
import joblib  # for saving TfidfVectorizer
import tensorflow as tf  # for saving the model

# Load data
data = pd.read_csv('merged_iq_data.csv')
texts = data['text'].values
iq_scores = data['iq'].values

# Split data
X_train, X_temp, y_train, y_temp = train_test_split(texts, iq_scores, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Vectorize text
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vect = vectorizer.fit_transform(X_train).toarray()
X_val_vect = vectorizer.transform(X_val).toarray()
X_test_vect = vectorizer.transform(X_test).toarray()

# Model building function
def build_model(hp):
    model = Sequential()
    model.add(Dense(units=hp.Int('units_input', min_value=32, max_value=512, step=32), 
                    activation='relu', input_dim=X_train_vect.shape[1]))
    for i in range(hp.Int('n_layers', 1, 3)):
        model.add(Dense(units=hp.Int(f'units_layer{i}', min_value=32, max_value=256, step=32), activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=Adam(hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='LOG')),
                  loss='mean_squared_error')
    return model

# Hyperparameter tuning
tuner = RandomSearch(
    build_model,
    objective='val_loss',
    max_trials=5,  
    executions_per_trial=1,
    directory='my_dir',
    project_name='iq_prediction'
)

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

tuner.search(X_train_vect, y_train, epochs=50, validation_data=(X_val_vect, y_val), callbacks=[early_stopping])

best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

model = tuner.hypermodel.build(best_hps)

model.fit(X_train_vect, y_train, epochs=50, validation_data=(X_val_vect, y_val), callbacks=[early_stopping])

mse = model.evaluate(X_test_vect, y_test)
rmse = np.sqrt(mse)
print(f"RMSE on Test Set: {rmse}")

# Save the model and vectorizer
model.save('iq_model.h5')  # Save the trained model
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')  # Save the vectorizer
