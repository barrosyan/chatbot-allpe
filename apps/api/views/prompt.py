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
            MODEL_URL,
            headers=headers,
            json={"inputs": input_text, "context": context}
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
        context='A partir de agora você é um chat especializado para customer success, na área de podologia, portanto, responda a mensagem a seguir (Lembre de respeitar os direitos humanos, sem palavras de baixo calão e sem autodiagnóstico, apenas sugestões, mas sempre sugerindo um atendimento de um profissional especializado na All Pé, perguntando se gostaria de agendar atendimento com algum): ', 
        user_input=None):
        
        try:
            with open("chat_messages.json", 'r') as f:
                chat = json.loads(f.read())
                f.close()
            i = 2
        except:
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
