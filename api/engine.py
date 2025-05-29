import os
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel

def predict_cluster(model_id, rating, likes, length):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "..", "models", model_id)
    model_path = os.path.normpath(model_path)

    
    if not os.path.exists(model_path):
        return {"error": f"Model {model_id} tidak ditemukan"}

    # Inisialisasi SparkSession
    spark = SparkSession.builder \
        .appName("PredictionAPI") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    try:
        # Load model dari folder
        model = PipelineModel.load(model_path)

        # Siapkan data input
        data = [(rating, likes, length)]
        columns = ["review_rating", "review_likes", "review_length"]
        df = spark.createDataFrame(data, columns)

        # Prediksi
        prediction = model.transform(df).collect()[0]["prediction"]
        return {"prediction": int(prediction)}

    except Exception as e:
        print("Prediction Error:", e)
        return {"error": str(e)}

    finally:
        spark.stop()
