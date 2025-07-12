from transformers import pipeline

# Load the model
pipe = pipeline("text-generation", model="google/gemma-2-9b-it", trust_remote_code=True)

# Persian prompt
persian_prompt = "لطفاً یک داستان کوتاه درباره دوستی بنویس."

# Generate text
output = pipe(persian_prompt, max_new_tokens=100, do_sample=True)

# Print the generated output
print(output[0]["generated_text"])
print("hi")