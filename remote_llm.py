import torch
from transformers import pipeline

# بارگذاری مدل روی GPU
device = 0 if torch.cuda.is_available() else -1

pipe = pipeline("text-generation", model="OrionStarAI/Orion-14B-Base", trust_remote_code=True, device=device)

# نمایش وضعیت حافظه GPU
if device >= 0:
    print(f"GPU name: {torch.cuda.get_device_name(device)}")
    print(f"Allocated VRAM: {torch.cuda.memory_allocated(device) / 1024 ** 2:.2f} MB")
    print(f"Cached VRAM: {torch.cuda.memory_reserved(device) / 1024 ** 2:.2f} MB")

# پرامپت فارسی
persian_prompt = "لطفاً یک داستان کوتاه درباره دوستی بنویس."

# تولید متن
output = pipe(persian_prompt, max_new_tokens=100, do_sample=True)

print(output[0]["generated_text"])
print("hi")

# نمایش مصرف حافظه بعد از تولید
if device >= 0:
    print(f"Allocated VRAM after generation: {torch.cuda.memory_allocated(device) / 1024 ** 2:.2f} MB")
    print(f"Cached VRAM after generation: {torch.cuda.memory_reserved(device) / 1024 ** 2:.2f} MB")
