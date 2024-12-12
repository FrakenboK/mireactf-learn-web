from flask import Flask, request, render_template, jsonify
from subprocess import run
import json

app = Flask(__name__)

def create_resp(message: str) -> dict[str:str]:
    return jsonify({"message": message})

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/api/calculate", methods=['POST'])
def pinger():
    data = json.loads(request.data)
    if "sign" not in data:
        return create_resp("Nothing to calculate")
    
    try:
        answer = eval(data["sign"])
    except:
        return create_resp("bebebe")
    return create_resp(answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=61337, debug=False)
