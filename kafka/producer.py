import csv
import json
import random
import time
from kafka import KafkaProducer

# Konfigurasi Kafka
KAFKA_TOPIC = 'netflix-reviews'
KAFKA_BROKER = 'localhost:9092'
CSV_PATH = '../dataset-kafka2/NETFLIX_REVIEWS.csv'  # Sesuaikan dengan path-mu

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_csv():
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Kirim data ke Kafka
            producer.send(KAFKA_TOPIC, value=row)
            review_id = row.get("review_id") or row.get("id") or "-"
            rating = row.get("review_rating") or "-"
            likes = row.get("review_likes") or "-"
            text = row.get("review_text", "")
            length = len(text)

            print(f"Sent [ID: {review_id}] Rating: {rating} Likes: {likes} Length: {length} | {text[:60]}...")

            time.sleep(random.uniform(0.2, 1.0))  # Delay 200ms–1s

    print("✅ Semua data berhasil dikirim ke Kafka.")

if __name__ == "__main__":
    try:
        stream_csv()
    except KeyboardInterrupt:
        print("🛑 Streaming dihentikan manual.")
