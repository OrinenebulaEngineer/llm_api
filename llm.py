from vllm import LLM, ChatResponse
import requests

class Llm:
    def __init__(self):
        self.model = LLM(model="google/gemma-2-9b-it")  
    
    def __init__(self):
        self.vllm_url =  "http://127.0.0.1:5000"  

    def vllm_response(self, prompt):
        response = requests.post(f"{self.vllm_url}/generate", json={"prompt": prompt})
        if response.status_code == 200:
            return response.json().get("output")
        else:
            return "Error: Unable to get response from VLLM server."
       

    def ollama_response(self, prompt):
                
        message = [
                {"role" : "system" , "content" : "you are helpful assistance provide good answer based on  prompt language"},
                {"role" : "user",  "content" : prompt}
            ]

        response : ChatResponse = chat(
                model = 'qwen:32b',
                messages= message)
            
        output = response.message.content
        # print(output)

        return output