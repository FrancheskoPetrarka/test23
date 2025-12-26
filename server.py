from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import json

app = Flask(__name__)
# Включаем CORS на полную катушку
CORS(app, resources={r"/*": {"origins": "*"}})

DB_FILE = 'database.json'

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    return "☘️ Clever.txt API is Alive!"

@app.route('/save', methods=['POST', 'OPTIONS'])
def save_document():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    data = request.json
    doc_id = data.get('id')
    content = data.get('content')
    
    db = load_db()
    db[doc_id] = content
    save_db(db)
    
    print(f"✅ [SAVE] Документ сохранен: ID = {doc_id}")
    return _corsify_actual_response(jsonify({"status": "success", "id": doc_id}))

@app.route('/load/<doc_id>', methods=['GET'])
def load_document(doc_id):
    db = load_db()
    content = db.get(doc_id, "")
    
    if content:
        print(f"📖 [LOAD] Чтение документа: ID = {doc_id} (найдено)")
    else:
        print(f"❓ [LOAD] Запрос нового документа: ID = {doc_id} (пусто)")
    
    return _corsify_actual_response(jsonify({"content": content}))

# Вспомогательные функции, чтобы CORS тебя не донимал
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    # Запрещаем браузеру кэшировать ответы, чтобы друг видел всё сразу
    response.headers.add("Cache-Control", "no-cache, no-store, must-revalidate")
    return response

if __name__ == '__main__':
    print("🚀 Clever.txt запущен на порту 5000")
    print("Убедись, что Ngrok проброшен: ngrok http 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
