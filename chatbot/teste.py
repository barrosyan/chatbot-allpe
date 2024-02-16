#!pip install deep_translator

API_TOKEN='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'

import requests
from deep_translator import GoogleTranslator

API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
 response = requests.post(API_URL, headers=headers, json=payload)
 return response.json()

chat=[]
i=1
while True:
    user_input=input('')
    
    if i == 1:
      context='A partir de agora você é um chat especializado para customer success, portanto, responda a pergunta a seguir: '
      chat.append(context+user_input)
    
      translated_input = GoogleTranslator(source='auto', target='en').translate('\n'.join(chat))
      outputs = query({
        "inputs": translated_input,
      })
      output = outputs[0]['generated_text'].split('\n\n')[1]
      translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ','')
      i=2

    else:
      chat.append(user_input)
      translated_input = GoogleTranslator(source='auto', target='en').translate('Responda apenas a última sentença desta conversa baseando-se no contexto completo'+('\n'.join(chat)))
      outputs = query({
        "inputs": translated_input,
      })
      output = outputs[0]['generated_text'].split('\n')[len(chat)]
      translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ','')
    
    print('\n')
    print(translated_output)
    print('\n')
    chat.append(translated_output)