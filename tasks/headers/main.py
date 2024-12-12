from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def main():
    return "<h1>You want some flags?</h1>"

@app.route('/give_me_my_flag', methods=['FLAG'])
def give_me_my_flag():
    if request.headers.get('Flag-Header') != "I-am-real-flag-owner":
        return jsonify({"bebebe": "no flags for you"})
    
    try:
        data = json.loads(request.data)
    except:
        return jsonify({"bebebe": "no flags for you"})

    if "flags?" not in data:
        return jsonify({"bebebe": "no flags for you"})
    
    if type(data["flags?"]) != list:
        return jsonify({"bebebe": "no flags for you"})
    
    if len(data["flags?"]) != 2:
        return jsonify({"bebebe": "no flags for you"})
    
    for i in range(len(data["flags?"])):
        if data["flags?"][i] != f"trying to get flag {i+1} time":
            return jsonify({"bebebe": "no flags for you"})
        
    return jsonify({"here is your flag, little CTFer": os.getenv("FLAG")})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=11337, debug=False)
