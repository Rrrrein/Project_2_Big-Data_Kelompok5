from flask import Flask, request, jsonify
from engine import predict_cluster

app = Flask(__name__)

@app.route("/predict/<model_id>", methods=["POST"])
def predict(model_id):
    try:
        # Ambil data dari request
        data = request.get_json()

        # Pastikan semua field tersedia
        rating = data.get("review_rating")
        likes = data.get("review_likes")
        length = data.get("review_length")

        if rating is None or likes is None or length is None:
            return jsonify({"error": "Input tidak lengkap"}), 400

        # Jalankan prediksi
        result = predict_cluster(model_id, rating, likes, length)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
