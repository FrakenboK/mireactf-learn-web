from flask import Flask, request, render_template, jsonify
import json
import requests

app = Flask(__name__)

def create_resp(message: str) -> dict[str:str]:
    return jsonify({"message": message})

@app.route("/", methods=["GET"])
def flag():
    return render_template("index.html")

@app.route("/api/send", methods=['POST'])
def pinger():
    data = json.loads(request.data)
    if "url" not in data:
        return create_resp("The IP address was not specified")
    
    headers = {}
    if "headers" in data:
        headers = data["headers"]
    try:
        data = requests.get(data["url"], headers=headers).text
    except:
        return create_resp("bebebe")
    
    return create_resp(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=14337, debug=False)
