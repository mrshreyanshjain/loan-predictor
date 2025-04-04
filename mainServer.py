from flask import Flask, render_template, request, redirect, flash, send_from_directory
import pandas as pd
import os
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('loan_prediction.pkl', 'rb') as model_file:
    predictor = pickle.load(model_file)


# Path to save uploaded files
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.csv'):
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the CSV file
        data = pd.read_csv(file_path)

        # Assuming the CSV file has some necessary columns
        if not all(column in data.columns for column in ['Gender', 'LoanAmount', 'Property_Area']):
            flash('Invalid CSV format')
            return redirect(request.url)

        predictions = predictor.predict2(data)
        data['loan_approved'] = predictions

        # Save the result with predictions
        result_csv_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'predictions.csv')
        data.to_csv(result_csv_path, index=False)

        return render_template('download.html', file_url='/downloads/predictions.csv')

    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect(request.url)


# Route to download the file
@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(debug=True)
