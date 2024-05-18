from flask import Flask, request, jsonify, send_from_directory
import spacy
from spellchecker import SpellChecker
import os

app = Flask(__name__, static_folder='static')

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize the spell checker
spell = SpellChecker()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/correct', methods=['POST'])
def correct_text():
    data = request.get_json()
    text = data.get('text', '')

    # Use spaCy to process the text
    doc = nlp(text)

    # Correct spelling
    corrected_tokens = []
    for token in doc:
        if token.is_alpha:
            corrected_tokens.append(spell.correction(token.text))
        else:
            corrected_tokens.append(token.text)

    corrected_text = ' '.join(corrected_tokens)

    return jsonify({'corrected_text': corrected_text})

if __name__ == '__main__':
    app.run(debug=True)
