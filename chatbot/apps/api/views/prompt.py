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


API_TOKEN = decouple.config("API_TOKEN", default=None)
MODEL_URL = decouple.config("MODEL_URL", default=None)
headers = {"Authorization": f"Bearer {API_TOKEN}"}


class ChatAPIViewSet(ViewSet):
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    @action(
        detail=False,
        methods=["post"],
        url_path="chat",
    )
    def get_model_response(self, input_text):
        response = requests.post(MODEL_URL, headers=headers, json={"inputs": input_text})
        return response.json()
    
    def query(self, request):
        chat = []
        i = 1
        while True:
            user_input = request.data.get('prompt')

            if user_input:
                if i == 1:
                    context = 'A partir de agora você é um chat especializado para customer success, portanto, responda a pergunta a seguir: '
                    chat.append(context + user_input)

                    translated_input = GoogleTranslator(source='auto', target='en').translate('\n'.join(chat))
                    outputs = self.get_model_response(translated_input)
                    output = outputs[0]['generated_text'].split('\n\n')[1]
                    translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ', '')
                    i = 2
                else:
                    chat.append(user_input)
                    translated_input = GoogleTranslator(source='auto', target='en').translate('Responda apenas a última sentença desta conversa baseando-se no contexto completo' + ('\n'.join(chat)))
                    outputs = self.get_model_response(translated_input)
                    output = outputs[0]['generated_text'].split('\n')[len(chat)]
                    translated_output = GoogleTranslator(source='auto', target='pt').translate(output).replace('Answer: ', '')

                chat.append(translated_output)

                if translated_output == 'Encerrar conversa':
                    break

                return JsonResponse({'resposta': translated_output})
            else:
                return JsonResponse({'erro': 'Entrada de usuário não fornecida'}, status=400)
