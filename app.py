from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load the machine learning model
# Make sure 'model.pkl' is in the same directory as app.py
try:
    with open('price1.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None # Set model to None if loading fails

# You might need to load your preprocessor (e.g., OneHotEncoder, StandardScaler)
# if your model requires it. For simplicity, we're assuming the model handles
# all transformations internally, or you'll add them here.
# For example, if you used OneHotEncoder for 'company' and 'fuel_type':
# with open('encoder.pkl', 'rb') as encoder_file:
#     encoder = pickle.load(encoder_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = None
    if request.method == 'POST':
        if model is None:
            prediction_text = "Error: Machine learning model not loaded. Please check server logs."
            return render_template('index.html', prediction_text=prediction_text)

        try:
            # Get data from the form
            name = request.form['name']
            company = request.form['company']
            year = int(request.form['year'])
            kms_driven = int(request.form['kms_driven'])
            fuel_type = request.form['fuel_type']

            # Prepare data for prediction
            # IMPORTANT: Ensure the order and format matches what your model expects
            # If your model expects one-hot encoded categorical features, you'll need
            # to apply that here.
            # Example for categorical features:
            # You might need to map string inputs to numerical values or use an encoder.
            # For demonstration, let's assume a simple mapping or direct input if your
            # model was trained on these as numerical/encoded already.
            # If your model expects actual strings and handles encoding internally (e.g., LightGBM, CatBoost),
            # then you can pass them directly.
            
            # For demonstration, let's create a DataFrame row matching the model's training input
            # This is crucial for models expecting specific column names/order.
            
            # Dummy example if your model expects specific string inputs (e.g., for direct embedding or internal encoding)
            # data_for_prediction = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
            #                                      columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])

            # More robust approach: If your model expects numerical features after encoding
            # This part is highly dependent on how your model was trained.
            # Let's assume your model expects numerical features. If `company` and `fuel_type`
            # are strings, you need to convert them to numerical representations (e.g., using a pre-trained encoder).

            # For now, let's assume the model expects these values directly and can handle them.
            # If `company` and `fuel_type` are categorical strings, and your model uses
            # a OneHotEncoder or similar, you *must* apply it here using the *same encoder*
            # that was used during training.
            
            # Example if you need to manually prepare features (adjust based on your model's exact input format):
            # This is a placeholder, you will need to replace this with the actual feature engineering
            # Your model expects numerical features after all transformations.
            # The simplest assumption is that you pass a list/array of numerical values.
            # If your model's input expects categorical strings, then this might be simpler.
            
            # Example for a model expecting a 2D array of numerical features:
            # You would need to map 'company' and 'fuel_type' to numerical values.
            # For now, let's use a dummy numerical representation if your model expects it.
            # Replace these with your actual mappings or encoder application.
            # If your model's input is directly ['name', 'company', 'year', 'kms_driven', 'fuel_type']
            # as strings, then you can just pass those.

            # Example: Assume your model was trained on a DataFrame with specific column names.
            # The column order and names *must* match the training data.
            input_df = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                                    columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
            
            # If you used an encoder (e.g., OneHotEncoder) for categorical features, apply it here:
            # encoded_features = encoder.transform(input_df[['company', 'fuel_type']])
            # # Then combine with numerical features:
            # final_input = np.hstack([input_df[['year', 'kms_driven']].values, encoded_features])
            # Or if your model expects a pandas DataFrame after all preprocessing:
            # final_input_df = preprocess_function(input_df) # A function you define to match training preprocessing

            # For simplicity, let's assume your model takes a 2D array and handles
            # any internal encoding for strings (e.g., if you used a model like CatBoost)
            # or if 'company' and 'fuel_type' are already numerical mappings.
            
            # If your model expects a simple 2D numpy array of values:
            # Convert categorical inputs to numerical if required by your model:
            # (THIS IS A PLACEHOLDER - YOU NEED TO IMPLEMENT ACTUAL MAPPING/ENCODING)
            # Example:
            # company_numerical = some_mapping_function(company)
            # fuel_type_numerical = another_mapping_function(fuel_type)
            # features = np.array([[company_numerical, year, kms_driven, fuel_type_numerical]])

            # For a more general approach where the model expects a DataFrame with specific columns:
            prediction = model.predict(input_df)[0]
            prediction_text = f"Predicted Car Price: ₹ {prediction:,.2f}"

        except ValueError:
            prediction_text = "Please enter valid numerical values for Year and KMs Driven."
        except KeyError as e:
            prediction_text = f"Error: Missing form field. {e}"
        except Exception as e:
            prediction_text = f"An error occurred during prediction: {e}"

    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True) # debug=True allows for automatic reloading on code changes