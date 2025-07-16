import json
import requests
import re
import time
class Llm:
    def __init__(self):
        # self.vllm_url = "http://185.103.84.24:80/v1/chat/completions"
        self.vllm_url = "http://'0.0.0.0', 8000/v1/chat/completions"

    
        
        
    def vllm_inference(self, user_message,system_message):
        # Assuming config.OPEN_MODELS is a dictionary that maps model IDs to model names
        start_time = time.time()
        prompt = [{"role": "user", "content": user_message},
                            {"role": "system", "content": system_message}]

        model = "google/gemma-2-9b-it"
        # print("hi im in vllm inference")
        payload = {
            "model": model,
            "messages": prompt,  
            "max_tokens": 1000,
            "temperature": 0.5,      
            "top_p": 1,   
        }

        try:
            # Send a POST request to VLLM server
            response = requests.post(
                self.vllm_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            # print("response")
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                # print("status code is 200")
                end_time = time.time()  
        
                print(f"Time taken for inference: {end_time - start_time} seconds")
                return response_data
            else:
                print(f"Error in response data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error : {e}")
            return None
                 
    def clean_text(self, content):
        cleaned_content = content.strip()                          # Remove leading/trailing spaces
        cleaned_content = re.sub(r'\n+', '\n', cleaned_content)    # Collapse multiple newlines
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)     # Optional: collapse all excessive spaces to single space
        cleaned_content = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_content)  # Optional: remove Markdown bold **text**
        return cleaned_content


def main():
    # system_message= "تو یک مترجم آیات قرآنی هستی"
    # user_input = "کلماتی را در قرآن می‌گویم و می‌خواهم در یک پاراگراف کوتاه تعریف کامل کنی: ارءیتم "

    
    system_message = '''
ابتدا موجودیت های نامدار را به همراه مقادیرشان شناسایی کن. موجودیت های نامدار شامل: افراد،اسامی و فامیل‌‌های خاص، مکان ها، سازمان ها، تاریخ ها و مقادیر عددی است. 
در مرحله دوم اگرمقدار موجودیت موجود بود بلی بگذار اگر موجود نبود خیر بگذار.
 اگر موجودیتی شامل اسامی اختصاری مانند آقای ع.ا. یا آقای ا.ف. فرزند ج. است، را "خیر" بگذار.
اگر نام یا نام خانوادگی کامل بعد از موجودیت آمده بود "بله" بگذار.
اگر به جای مقدار موجودیت فقط کاراکتر * بود و بعد از آن هم مقدار موجودیت خاصی ذکر نشده بود "خیر" بگذار .
اگر موجودیت‌هایی هستند که باید عددی باشند ولی بعد از آن عددی نیامده "خیر" بگذار.
خروجی را در فرمت csv مانند نمونه خروجی که در 3 ``` آمده است، بده. 
نمونه ورودی :
پرونده کلاسه *حوزه دو شهری شعبه *تصمیم نهایی شماره *\n\n خواهان: اقای ع. ا. ر. ن. فرزند ا. به نشانی *\n\n خوانده: اقای ا. ن. فرزند م. ب. به نشانی *\n\n خواسته: اعسار از پرداخت محکوم به\n\n ( ( \n\n رای شورا ) ) \n\n در خصوص دعوی اقای ع. ا. ر. ن. فرزند ا. بطرفیت اقای ا. ن. بخواسته اعسار وتقسیط محکوم به دادنامه شماره *مورخ 94/2/27 درپرونده کلاسه *حوزه 2 شعبه *باعنایت به محتویات پرونده وبا توجه به درخواست خواهان و باعنایت به اظهارات طرفین شهود تعرفه شده واستشهادیه منضم دادخواست خواهان که قرینه ای برعدم توانایی پرداخت دین بوده ومستندا" به مواد7و8 و11قانون نحوه اجرای محکومیتهای مالی ومواد 277 و652 قانون مدنی خواسته خواهان را وارد تشخیص وحکم بر اعسار به تقسیط محکوم به ماهیانه 2/000/000 ریال تا استهلاک کامل صادر واعلام می نماید. رای صادره حضوری وظرف 20 روز از تاریخ ابلاغ قابل تجدیدنظرخواهی در محاکم محترم عمومی حقوقی *میباشد./\n\n قاضی حوزه 2 شعبه *\n\n ح. ا. ک
مد قایدی.
نمونه خروجی:
```نوع موجودیت,مقدار در متن,وضعیت
نام کامل خواهان,آقای ع. ا. ر. ن. فرزند ا.,خیر
نام کامل خوانده,آقای ا. ن. فرزند م. ب.,خیر
نشانی خواهان,به نشانی *,خیر
نشانی خوانده,به نشانی *,خیر
تاریخ دقیق,94/2/27,بلی
شماره پرونده (کلاسه),کلاسه * حوزه 2 شعبه *,خیر
شماره دادنامه,دادنامه شماره *,خیر
شعبه دادگاه/شورا,حوزه 2 شعبه *,بلی
قاضی / دادرس / صادرکننده رأی,ح. ا. ک.,خیر
نام سازمان / نهاد رسمی,محاکم محترم عمومی حقوقی,بلی (به عنوان نهاد قضایی عمومی)
شهود (با نام کامل),شهود تعرفه شده (بدون نام),خیر
نشانی خوانده,به نشانی *,خیر
تاریخ دقیق,94/2/27,بلی
مدیردفتر,موسوی,بله```


'''
    
    user_input = '''
پرونده کلاسه *تصمیم نهایی شماره *

 خواهان ها: 

 1. 

 اقای ا. ک. فرزند ن. 2. خانم ا. ک. فرزند ا. 3. خانم ش. ک. فرزند خ. با وکالت اقای م. خ. فرزند ه. به نشانی *

 خوانده: اقای م. ر. ح. به نشانی *

 خواسته: اعسار از پرداخت محکوم به

 به تاریخ  پرونده کلا سه فوق دروقت فوق العاده تحت نظراست شورا با توجه به محتویات پرونده ختم رسیدگی رااعلام و به شرح ذیل مبادرت به صدور رای می نماید.

 رای شورا

 در خصوص دادخواست خواهان ها ا. ا. ش. ک. با وکالت م. خ. به طرفیت خوانده م. ح. به خواسته اعسار به تقسیط مبلغ 190/000/000 ریال قاضی شورا با توجه به محتویات پرونده از جمله دادخواست تقدیمی نظر به اینکه خواهان دلیل موجه و مدللی جهت اثبات ادعای خود  ارائه ننموده و استشهادیه ابرازی نیز فاقد شرایط مندرج در ماده 7و8و9 قانون نحوه محکومیتهای مالی مصوب سال 93 می باشد. لذا دعوی خواهان غیر وارد تشخیص و مستندا به مواد مذکور قانون فوق حکم به رد دعوی وی را صادر و اعلام می دارد. رای صادره حضوری و ظرف بیست روز پس از ان قابل تجدید نظرخواهی در محاکم عمومی دادگستری شهرستان *می باشد. 

 قاضی شعبه *

 ک.'''
    llm = Llm()
    response = llm.vllm_inference(user_message=user_input, system_message=system_message)
    content = response['choices'][0]['message']['content']
    clean_text = llm.clean_text(content)
    # print(content)
    print(clean_text)

if __name__ == "__main__":
    main()

