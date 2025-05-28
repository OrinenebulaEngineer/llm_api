# from flask import Flask, request, jsonify
# import paramiko
# from llm import  Llm
# app = Flask(__name__)

# def connect_to_server(server_ip , username, password, command):
#     try:
#         #create an SSH client
#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         if server_ip and username and password:
#             #connect to the server 
#             client.connect(server_ip, username=username, password=password)

#         #Execute a command
#         stdin, stdout, stderr = client.exec_command(command=command)
#         output = stdout.read().decode()
#         error = stderr.read().decode()

#         client.close()

#     except Exception as e:
#         return None, str(e)

# @app.route('/run_command', methods=['POST'])
# def run_command():

#     data = request.json
#     prompt = data.get("prompt")

#     llm =  Llm()
#     llm_response = llm.vllm_response(prompt)
    
#     return jsonify({"output" : llm_response})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port =5000)
    

from flask import Flask, request, jsonify
import paramiko
import requests
import json

app = Flask(__name__)

def connect_to_server(server_ip, username, password, command):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if server_ip and username and password:
            # Connect to the server 
            client.connect(server_ip, username=username, password=password)

        # Execute a command
        stdin, stdout, stderr = client.exec_command(command=command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        client.close()

        return output, error

    except Exception as e:
        return None, str(e)

class Llm:
    def __init__(self):
        self.vllm_url = "http://localhost:8000/v1/chat/completions"  

    def vllm_inference(self, prompt):
        # Assuming config.OPEN_MODELS is a dictionary that maps model IDs to model names
        model = "google/gemma-2-9b-it"
        # print("hi im in vllm inference")
        payload = {
            "model": model,
            "messages": prompt,  
            "max_tokens": 2000,
        }

        try:
            # Send a POST request to VLLM server
            response = requests.post(
                self.vllm_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            print("response")
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                print("status code is 200")
                return response_data
            else:
                print(f"Error in response data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error : {e}")
            return None

@app.route('/run_command', methods=['POST'])
def run_command():
    data = request.json
    prompt = data.get("prompt")
    # return jsonify({"response": f"You said: {prompt}"})
    

    llm = Llm()
    llm_response = llm.vllm_inference(prompt)

    if llm_response:
        # Assuming the response contains a "choices" field with the output
        output = llm_response.get("choices", [{}])[0].get("message", {}).get("content", "No content")
    else:
        output = "Error: Unable to get response from VLLM server."

    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
