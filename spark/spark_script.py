from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier
from pyspark.ml import Pipeline
from pyspark.sql.functions import length, when
import os

BATCH_FOLDER = "batches_grouped"
MODEL_FOLDER = "models"
os.makedirs(MODEL_FOLDER, exist_ok=True)

spark = SparkSession.builder \
    .appName("NetflixMultiModelTraining") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

group_dirs = sorted([d for d in os.listdir(BATCH_FOLDER) if d.startswith("group_")])

for idx, group_dir in enumerate(group_dirs, 1):
    print(f"📁 Processing group: {group_dir}")
    group_path = os.path.join(BATCH_FOLDER, group_dir)
    batch_files = sorted([f for f in os.listdir(group_path) if f.endswith(".json")])

    df_list = []
    for file in batch_files:
        path = os.path.join(group_path, file)
        df = spark.read.option("multiline", "true").json(path)
        df_list.append(df)

    df = df_list[0]
    for d in df_list[1:]:
        df = df.unionByName(d)

    df = df.withColumn("review_rating", df["review_rating"].cast("int")) \
           .withColumn("review_likes", df["review_likes"].cast("int")) \
           .withColumn("review_length", length(df["review_text"].cast("string")))

    df = df.select("review_rating", "review_likes", "review_length").dropna()

    # ➕ Tambah kolom label dummy
    df = df.withColumn("label", when(df["review_rating"] >= 4, 1).otherwise(0))

    features = ["review_rating", "review_likes", "review_length"]
    assembler = VectorAssembler(inputCols=features, outputCol="features")

    if idx == 1:
        print("🔵 Menggunakan KMeans")
        model_algo = KMeans(featuresCol="features", predictionCol="prediction", k=3, seed=42)
        stages = [assembler, model_algo]
    elif idx == 2:
        print("🟢 Menggunakan Logistic Regression")
        model_algo = LogisticRegression(featuresCol="features", labelCol="label", predictionCol="prediction", maxIter=10)
        stages = [assembler, model_algo]
    else:
        print("🟠 Menggunakan Decision Tree")
        model_algo = DecisionTreeClassifier(featuresCol="features", labelCol="label", predictionCol="prediction", maxDepth=5)
        stages = [assembler, model_algo]

    pipeline = Pipeline(stages=stages)
    model = pipeline.fit(df)

    model_path = os.path.join(MODEL_FOLDER, f"model_{idx}")
    model.write().overwrite().save(model_path)
    print(f"✅ Model {idx} disimpan di {model_path}")

spark.stop()
print("🎉 Semua model selesai dilatih.")
