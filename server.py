from flask import Flask,request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

with open('loan_prediction.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def eligibility():
    file = request.files['file']
    df = pd.read_csv(file)
    prediction = loaded_model.predict2(df)
    print(prediction)
    return f"Loan Approval Predictions: {prediction}"


if __name__ == '__main__':
    app.run()
