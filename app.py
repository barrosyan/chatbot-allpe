from flask import Flask, request, jsonify
import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

with open('dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

user_sentences = []
tag_words_lists = []

for item in data:
    tag_words = ' '.join(item['tag_question'])
    tag_words_lists.append(tag_words)
    for answer in item['answers']:
        user_sentences.append(answer)

nltk.download('punkt')
tfidf_vectorizer = TfidfVectorizer()
tag_words_vectors = tfidf_vectorizer.fit_transform(tag_words_lists)

def get_most_similar_tag(sentence):
    sentence_vector = tfidf_vectorizer.transform([sentence])
    similarities = cosine_similarity(sentence_vector, tag_words_vectors)
    most_similar_tag_index = np.argmax(similarities)
    return most_similar_tag_index

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    most_similar_tag_index = get_most_similar_tag(user_input)
    answers_for_tag = data[most_similar_tag_index]['answers']
    chosen_answer = np.random.choice(answers_for_tag)
    return jsonify({'response': chosen_answer})

if __name__ == '__main__':
    app.run(debug=True)
