from vllm import LLM, ChatResponse

class Llm:
    def __init__(self):
        self.model = LLM(model="google/gemma-2-9b-it")  
    def response(self, prompt):
        message = [
            {"role": "system", "content": "you are helpful assistance provide good answer based on prompt language"},
            {"role": "user", "content": prompt}
        ]

        response: ChatResponse = self.model.chat(messages=message)

        output = response.message.content
        return output
