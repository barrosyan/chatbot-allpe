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


API_TOKEN = decouple.config("API_TOKEN", default=None)
MODEL_URL = decouple.config("MODEL_URL", default=None)
headers = {"Authorization": f"Bearer {API_TOKEN}"}


class ChatAPIViewSet(ViewSet):
    # @method_decorator(cache_page(60*60*2))
    # @method_decorator(vary_on_headers("Authorization",))
    
    def get_model_response(self, input_text):
        response = requests.post(
            MODEL_URL,
            headers=headers,
            json={"inputs": input_text}
        )
        return response.json()
    
    @action(
        detail=False,
        methods=["post"],
        url_path="chat",
    )
    def query(self, request):
        
        with open("chat_messages.json", 'r') as f:
            chat = json.loads(f.read())
            f.close()
        i = 2

        if not chat:
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

            with open("chat_messages.json", 'w') as f:
                f.write(json.dumps(chat, indent=4, ensure_ascii=False))
                f.close()
            return JsonResponse({'message': translated_output})
        else:
            return JsonResponse(
                {'erro': 'Entrada de usuário não fornecida'},
                status=400
            )
