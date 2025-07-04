import pickle
from flask import Flask, request, render_template
import numpy as np

application = Flask(__name__)
app = application

# Load ridge regression model and standard scaler
ridge_model = pickle.load(open('models/ri.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scalar.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('home.html')  # Use home.html as your main template

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_method():
    if request.method == 'POST':
        try:
            # Collect input values from the form
            data = [
                float(request.form['Temperature']),
                float(request.form['RH']),
                float(request.form['Ws']),
                float(request.form['Rain']),
                float(request.form['FFMC']),
                float(request.form['DMC']),
                float(request.form['ISI']),
                float(request.form['Classes']),
                float(request.form['Region']),
            ]

            # Scale the data
            scaled_data = standard_scaler.transform([data])
            prediction = ridge_model.predict(scaled_data)[0]

            return render_template('home.html', prediction=round(prediction, 2), form_data=request.form)

        except Exception as e:
            return render_template('home.html', prediction=f"Error: {str(e)}", form_data=request.form)

    # When accessed via GET (like typing URL), just return the form
    return render_template('home.html')


        
if __name__ == '__main__':
    app.run(debug=True)

