from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/app', methods=['POST'])
def bridge():
    data = request.json
    key = data.get("key")
    args = data.get("args", [])

    if not key:
        return jsonify({"error": "Key is missing!"}), 400

    if key == "abcdefg":
        try:
            command = ["app.exe"] + args

            subprocess.Popen(command, shell=True)
            return jsonify({"message": "app.exe executed successfully with arguments!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid key!"}), 403

if __name__ == '__main__':
    app.run(debug=True)
