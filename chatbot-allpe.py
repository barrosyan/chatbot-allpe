from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('AllBot', read_only = True, 
              preprocessors=['chatterbot.preprocessors.convert_to_ascii', 
                             'chatterbot.preprocessors.unescape_html',
                             'chatterbot.preprocessors.clean_whitespace'],
             logic_adapters = [
                 {
                     'import_path': 'chatterbot.logic.BestMatch',
                     'default_response': 'Sorry, I am unable to process your request. Please try again, or contact us for help.',
                     'maximum_similarity_threshold': 0.75
                 }
             ],)

trainer = ListTrainer(bot)

with open ('dataset.txt', 'r') as f:
    chatbot_responses = f.readlines()

for i in range(0, len(chatbot_responses), 2):
    question = chatbot_responses[i].replace('"','').replace(',\n','').replace(', \n','')
    answer = chatbot_responses[i+1].replace('"','').replace(',\n','').replace(', \n','')
    trainer.train([
        question,
        answer,
    ])

app = Flask(__name__)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    query = data['query']
    response = str(bot.get_response(query))
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)