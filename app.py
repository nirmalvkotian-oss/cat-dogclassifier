from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from utils.utilsfile import decodeImage  # Updated import
from prediction.predict import DogCat

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = DogCat(self.filename)

# Initialize the app globally so the prediction route can always access it
clApp = ClientApp()

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    # Accepts the image directly from your HTML web form
    if 'file' not in request.files:
        return render_template('index.html', prediction="Error: No image uploaded")
        
    file = request.files['file']
    file.save(clApp.filename)
    
    # Run the model on the saved image
    result = clApp.classifier.predictiondogcat()
    
    # Extract the word 'cat' or 'dog' and send it back to the web page
    final_prediction = result[0]['image']
    return render_template('index.html', prediction=final_prediction)

if __name__ == "__main__":
    app.run(debug=True)