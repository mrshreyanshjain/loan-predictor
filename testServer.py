from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('test.html')


# Route to handle the POST request
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Get JSON data from the request
    name = data.get('name', 'Stranger')
    return jsonify({"message": f"Hello, {name}!"})


if __name__ == '__main__':
    app.run(debug=True)
