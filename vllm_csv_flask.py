from flask import Flask,request,jsonify
import requests
import pandas as pd

app = Flask(__name__)

#Replace with vllm server
VLLM_SERVER_URL = "http://localhost:8000/v1/chat/completions"


@app.route('/label', methods = ['POST'])
def label_csv():

    #Get the system message from the request
    message = request.form.get('json_message')

    #Get model name
    data = request.json
    model_name = data.get('model_name') 

        
    #Get the csv file from the request
    file = request.files['file']

    if message:
        print(f"Message is : {message}")
    
    # Check the file extension to determine the format
    file_name = file.filename
    if file_name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file_name.endswith(('.xls', 'xlsx')):
        df = pd.read_excel(file)
    else:
        return jsonify({"error": "Unsupported file format. Please upload a CSV or Excel file."}), 400
    
    result =[]
    for index,row in df.iterrows():
        
