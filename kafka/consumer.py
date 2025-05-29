from kafka import KafkaConsumer
import json
import os
import shutil

# === Config ===
TOPIC_NAME = 'netflix-reviews'
KAFKA_BROKER = 'localhost:9092'
BATCH_SIZE = 500
BATCH_FOLDER = 'batches'
GROUPED_FOLDER = 'batches_grouped'
GROUP_SIZE = 1000  # 1000 batch = 1 model
GROUP_PREFIX = 'model'

# Siapkan folder
os.makedirs(BATCH_FOLDER, exist_ok=True)
os.makedirs(GROUPED_FOLDER, exist_ok=True)

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='netflix-consumer-batched'
)

batch = []
batch_num = 1
group_num = 1
print("Mulai menerima data dari Kafka...")

try:
    for message in consumer:
        batch.append(message.value)
        print(f"🟢 Menerima pesan ke-{len(batch)}")

        if len(batch) >= BATCH_SIZE:
            filename = f"batch_{batch_num}.json"
            filepath = os.path.join(BATCH_FOLDER, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(batch, f, indent=2)
            print(f"✅ Simpan {len(batch)} data ke {filename}")
            batch = []
            batch_num += 1

            # Pindahkan setiap 1000 batch ke dalam satu folder model
            if (batch_num - 1) % GROUP_SIZE == 0:
                grouped_path = os.path.join(GROUPED_FOLDER, f"{GROUP_PREFIX}_{group_num}_data")
                os.makedirs(grouped_path, exist_ok=True)

                start = (group_num - 1) * GROUP_SIZE + 1
                end = group_num * GROUP_SIZE + 1
                print(f"📦 Mengelompokkan batch {start}–{end - 1} ke {grouped_path}")

                for i in range(start, end):
                    src = os.path.join(BATCH_FOLDER, f"batch_{i}.json")
                    if os.path.exists(src):
                        shutil.move(src, os.path.join(grouped_path, f"batch_{i}.json"))

                group_num += 1

except KeyboardInterrupt:
    print("🛑 Dihentikan manual.")
    if batch:
        filename = f"batch_{batch_num}_partial.json"
        filepath = os.path.join(BATCH_FOLDER, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2)
        print(f"💾 Simpan sisa data ke {filename}")

finally:
    consumer.close()
