from flask import Flask, request

from resources import EntryManager, Entry

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# FOLDER = '/tmp/' для тестов на платформе Егора
FOLDER = 'C:\\Users\\baxter\\Desktop\\web'

@app.route("/api/entries/")  # http://127.0.0.1:8000/api/entries/
def get_entries():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()  # загрузит все записи из исходной папки FOLDER в память компьютера (в атрибут объекта entry_manager.entries)
    list_dict = []
    for entry in entry_manager.entries:
        list_dict.append(entry.json())
    return list_dict  # list, содержащий записи в формате dict

@app.route('/api/save_entries/', methods=['POST'])  # http://127.0.0.1:8000/api/save_entries/
def save_entries():
    entry_manager = EntryManager(FOLDER)
    data = request.get_json() # Заполучите JSON из запроса при помощи get_json
    for entry_data in data:
        item = Entry.from_json(entry_data)
        entry_manager.entries.append(item)
    entry_manager.save()
    return {'status': 'success'}
# получаю ошибку
# 127.0.0.1 - - [09/Sep/2024 09:19:22] "GET /api/save_entries/ HTTP/1.1" 405 -


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)