from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/save_message', methods=['POST'])
def save_message():
    try:
        # Получаем полноценный оъект {"message":"hello, Bob", "From":"Alice", "To":"Bob"}
        data = json.loads(request.data)
    except: 
        return jsonify({"message": "error"})

    if "To" not in data:
        return jsonify({"message": "error"})

    # Проверяем все оставшиеся поля

    # Как-то сохраняем данные

    to = data["To"]
    return jsonify({"message": f"Saved your message for {to}"})

@app.route('/get_message', methods=['GET'])
def get_message():
    if "To" not in request.args:
        return jsonify({"message": "error"})

    # Получаем данные о сообщениях 
    # data = ...
    data = {"message": "Hello, Bob", "From": "Alice"}

    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337, debug=False)
