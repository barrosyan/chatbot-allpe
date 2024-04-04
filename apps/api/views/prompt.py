from django.http import JsonResponse
import requests
from deep_translator import GoogleTranslator
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
import decouple
import json


API_TOKEN='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'
API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"

headers = {"Authorization": f"Bearer {API_TOKEN}"}



class ChatAPIViewSet(ViewSet):
    # @method_decorator(cache_page(60*60*2))
    # @method_decorator(vary_on_headers("Authorization",))
    
    def get_model_response(self, input_text, context):
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": input_text.replace(context,""), "context": context}
        )
        return response.json()
    
    @action(
        detail=False,
        methods=["post"],
        url_path="chat",
    )
    def query(
        self, 
        request, 
        context="From now on, you are a specialized chat for customer success, in the podiatry area, so respond to the following message (Remember to respect human rights, without profanity and without self-diagnosis, only suggestions, but always suggesting an appointment with a specialized professional at All Pé, asking if they would like to schedule an appointment with anyone):", 
        user_input=None):
        
        try:
            with open("chat_messages.txt", 'r') as f:
                chat = f.readlines()
                f.close()
            i = 2
        except:
            chat = []
            i = 1

        user_input = request.data.get('prompt')
        if not user_input:
            return JsonResponse(
                {"error": "Prompt is required"},
                status=HTTP_400_BAD_REQUEST
            )

        if user_input:
            if i == 1:
                chat.append(context + user_input)

                translated_input = GoogleTranslator(source='auto', target='en').translate('\n'.join(chat))
                outputs = self.get_model_response(translated_input,context)
                try:
                    output = outputs[0]['generated_text'].split('\n\n')[1]
                except:
                    output = outputs[0]['generated_text']
                translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ', '')
                i = 2
            else:
                chat.append(user_input)
                translated_input = GoogleTranslator(source='auto', target='en').translate('Responda apenas a última sentença desta conversa baseando-se no contexto completo' + ('\n'.join(chat)))
                outputs = self.get_model_response(translated_input,context)
                output = outputs[0]['generated_text'].split('\n')[len(chat)]
                translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ', '')

            chat.append(translated_output)

            with open("chat_messages.txt", 'w') as f:
                f.write(chat.join('\n'))
                f.close()
            return JsonResponse({'message': translated_output})
        else:
            return JsonResponse(
                {'erro': 'Entrada de usuário não fornecida'},
                status=400
            )
