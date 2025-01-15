from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import crawl

client = OpenAI(api_key='api key')

app = Flask(__name__)

print("Çekilen veriler gpt'ye yükleniyor. Lütfen bekleyin.")
def load_data(dosyaAdi):
    try:
        with open(dosyaAdi, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "The data file was not found."

def soruF(question, context):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18", 
            messages=[
                {"role": "system", "content": "Sen bir haber yorumcususun. Sana verilen icerikte ### ile baslayan satirlar haber basligi, altindaki metin ise icerikler."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

context = load_data('data.txt')

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html') 

@app.route('/sor', methods=['POST'])
def sor():
    if context == "The data file was not found.":
        return jsonify({'error': 'The data file was not found.'})

    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided.'})

    answer = soruF(question, context)
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
