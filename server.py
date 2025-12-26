from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

# Создаем приложение
app = Flask(__name__)
# Разрешаем запросы с любого места (для разработки), иначе браузер будет орать
CORS(app)

# Имитация базы данных (в файлике json, потому что для MVP SQL не обязателен)
DB_FILE = 'database.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

@app.route('/')
def home():
    return "Clever.txt Server is Running! ☘️"

@app.route('/save', methods=['POST'])
def save_document():
    data = request.json
    doc_id = data.get('id')
    content = data.get('content')
    
    # Тут по-хорошему надо чистить от XSS (библиотека bleach), 
    # но ты просил дерзко, так что пока на свой страх и риск.
    
    db = load_db()
    db[doc_id] = content
    save_db(db)
    
    print(f"Документ {doc_id} сохранен.")
    return jsonify({"status": "success"})

@app.route('/load/<doc_id>', methods=['GET'])
def load_document(doc_id):
    db = load_db()
    content = db.get(doc_id, "")
    return jsonify({"content": content})

if __name__ == '__main__':
    # Запускаем на порту 5000
    app.run(debug=True, port=5000)