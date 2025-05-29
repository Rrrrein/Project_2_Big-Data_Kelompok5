# PROJECT 2 BIG DATA APACHE KAFKA 

**KELOMPOK 5**
| Nama     |                 NRP     |
| -------- |------- | 
| Nayla Raissa Azzahra     | 5027231054 |
| Aisha Ayya Ratiandari    | 5027231056 |
| Aisyah Rahmasari         | 5027231072 |

---
## Deskripsi Proyek
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

## Arsitektur Sistem

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
1. Clone repo dan masuk ke folder
```bash
git clone https://github.com/username/project-kafka-spark.git
cd project-kafka-spark
```

2. Buat virtual environment dan install dependensi
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Jalankan Docker Kafka + Zookeeper
   ```bash
   docker-compose up -d
   ```

5. Masuk ke container Kafka
   ```bash
   docker exec -it kafka bash
   ```

   Buat topik Kafka dengan nama "netflix-reviews"
   ```bash
   I have no name!@<container_id>:/$ kafka-topics.sh --create \
     --topic netflix-reviews \
     --bootstrap-server localhost:9092 \
     --replication-factor 1 \
     --partitions 1
   ```
6. Jalankan Producer
   ```bash
   python kafka/producer.py
   ```

![448707470-27e251c1-fb38-4cac-9777-40b806f4899c](https://github.com/user-attachments/assets/96ea83e3-1a40-4e53-bba1-ebe48c0286e6)

6. Jalankan Consumer (kumpulkan 500.000 data / 1000 batch untuk tiap model)
   ```bash
   python kafka/consumer.py
   ```

![448708894-ce9d4b4d-9358-43c3-850a-226623527738](https://github.com/user-attachments/assets/a24305db-e64f-4935-8af8-e15001d5b85c)

   Cek apakah consumer sudah berjalan dan menerima data
   ```bash
   kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic netflix-reviews --from-beginning
   ```

7. Jalankan script Spark untuk training model
   - Set environment Java (di WSL jika menggunakan Linux subsystem di Windows)
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   export PATH=$JAVA_HOME/bin:$PATH
   ```

   - Aktifkan virtual environment (pastikan sudah membuatnya sebelumnya)
   ```bash
   source ~/venv-pyspark/bin/activate
   ```

   - Masuk ke folder proyek
     ```bash
     cd "/mnt/c/Users/nasiKucing/Documents/College's/4th Term/Big Data dan Data Lakehouse/Project-2-Kafka-Kelompok-5"
     ```

   - Jalankan spark script
     ```bash
     spark-submit spark/spark_script.py
     ```
   ![448756624-4acd8d9c-2105-4243-9bbe-715f6b2879cd](https://github.com/user-attachments/assets/7b7a62b2-ced2-4d4a-9643-1b9937cedefc)

8. Jalankan Flask API
   - Masuk ke WSL & aktifkan venv
     ```bash
     source ~/venv-pyspark/bin/activate
     ```

   - Masuk ke folder proyek jika belum
     ```bash
     cd "/mnt/c/Users/nasiKucing/Documents/College's/4th Term/Big Data dan Data Lakehouse/Project-2-Kafka-Kelompok-5"
     ```

   - Jalankan server API
     ```bash
     python api/server.py
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

## Output Endpoint API
1. **Model 1**
![448770454-0828fd82-8535-48b1-8d6c-dc4a664e3ccd](https://github.com/user-attachments/assets/0e936bed-0fa2-4704-8621-3440272a4dca)

2. **Model 2**
![448772143-59ecc665-c6c5-403e-b724-bb7aaf31ebfc](https://github.com/user-attachments/assets/61db6620-5d8f-4cfa-a0df-7d3f2c0d5b06)

3. **Model 3**
![448772333-1fc647d4-2576-4cae-9d52-93475642773e](https://github.com/user-attachments/assets/c0229fb2-0993-4746-bbf5-0c541cc2840c)

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

