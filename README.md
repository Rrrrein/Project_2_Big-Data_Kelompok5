# PROJECT 2 BIG DATA APACHE KAFKA 

**KELOMPOK 5**
| Nama     | NRP     | Tugas                                   |
| -------- | ------- | --------------------------------------- |
| Ayya     | 051xxxx | Flask API, Spark Script, Evaluasi Model |
| Member 2 | 051xxxx | Kafka Producer & Consumer               |
| Member 3 | 051xxxx | Dataset Processing & Dokumentasi        |

---
## 📚 Deskripsi Proyek
![image](https://github.com/user-attachments/assets/f25c3288-064e-4743-9ac3-41e9e8a43a4f)
Proyek ini mensimulasikan sistem Big Data yang memproses review aplikasi Netflix secara streaming menggunakan Kafka. Data dikirim secara sekuensial oleh Kafka Producer, diterima oleh Kafka Consumer, lalu disimpan dalam batch JSON. Data yang telah terkumpul dilatih menggunakan Apache Spark MLlib untuk membentuk tiga model machine learning berbeda berdasarkan bagian data yang berbeda. Model-model ini kemudian digunakan oleh REST API untuk memberikan prediksi klasifikasi cluster terhadap input pengguna.

# Netflix App Review Streaming & Clustering using Kafka and Apache Spark
## Fitur Utama
* [x] Kafka Producer membaca dan mengirim data secara streaming
* [x] Kafka Consumer menyimpan data dalam batch (500 data per batch)
* [x] Batch digabung per 1000 menjadi grup data untuk melatih model
* [x] Spark ML digunakan untuk membuat 3 model machine learning berbeda
* [x] API dibangun menggunakan Flask dan menyajikan model via endpoint berbeda
* [x] Dapat digunakan via Postman maupun Thunder Client (VSCode)

## 🖼Arsitektur Sistem

```
[Dataset]
   ↓
[Kafka Producer]
   ↓
[Kafka Server]
   ↓
[Kafka Consumer]
   ↓
[Batch JSON per 500 Data]
   ↓
[Folder batch_grouped/ (500.000 data/model)]
   ↓
[Spark ML Training (3 model berbeda)]
   ↓
[Folder models/]
   ↓
[REST API (model_1, model_2, model_3)]
```

## 🗃Struktur Folder

```
.
├── api/
│   ├── app.py
│   ├── engine.py
│   └── server.py
├── kafka/
│   ├── producer.py
│   └── consumer.py
├── spark/
│   └── spark_script.py
├── batches/                    # 500-data batch
├── batches_grouped/           # batch untuk masing-masing model
├── models/                    # hasil model Spark
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Cara Menjalankan Proyek

```bash
# 1. Clone repo dan masuk ke folder
$ git clone https://github.com/username/project-kafka-spark.git
$ cd project-kafka-spark

# 2. Buat virtual environment dan install dependensi
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# 3. Jalankan Docker Kafka + Zookeeper
$ docker-compose up -d

# 4. Jalankan Producer
$ python kafka/producer.py

# 5. Jalankan Consumer (kumpulkan 500.000 data / 1000 batch untuk tiap model)
$ python kafka/consumer.py

# 6. Jalankan script Spark untuk training model
$ spark-submit spark/spark_script.py

# 7. Jalankan Flask API
$ python api/server.py
```

## Contoh Request API

```http
POST http://localhost:9999/predict/model_1
Content-Type: application/json
{
  "rating": 4,
  "likes": 15,
  "length": 300
}

Response:
{
  "prediction": 2
}
```

## Dependensi

* kafka-python
* pyspark
* flask
* cherrypy
* tqdm
* matplotlib (opsional untuk visualisasi)
* scikit-learn (untuk evaluasi manual)

## Referensi

* Dataset: [https://www.kaggle.com/datasets/bwandowando/1-5-million-netflix-google-store-reviews](https://www.kaggle.com/datasets/bwandowando/1-5-million-netflix-google-store-reviews)
* Apache Spark MLlib Docs
* Kafka Python Docs
* Kaggle Notebook Referensi: [https://www.kaggle.com/code/dima806/netflix-app-rating-autoviz-catboost-shap](https://www.kaggle.com/code/dima806/netflix-app-rating-autoviz-catboost-shap)

## Catatan Tambahan

* Gunakan group\_id berbeda pada Kafka Consumer jika ingin reset offset.
* Spark akan mencoba bind ke port 4040, pastikan belum digunakan atau sediakan alternatif.
* API dapat dites via Postman maupun Thunder Client di VSCode.

