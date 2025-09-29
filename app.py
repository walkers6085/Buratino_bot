from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    try:
        # Проверяем наличие файла
        if not os.path.exists("stocks.json"):
            return jsonify({"error": "Файл stocks.json не найден"}), 404
        
        with open("stocks.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Ошибка в формате JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"Ошибка загрузки: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)