import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import redis
from database import get_db  # clean database.py

# Connect to Redis
r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

# Connect to MongoDB
collection = get_db()
try:
    collection.insert_one({"test_connection": True})
    print("✓ MongoDB connection works!")
except Exception as e:
    print("✗ MongoDB insert failed:", e)

def scrape_title(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title Found"
        return title
    except requests.RequestException as e:
        print(f"  ⚠ Request error for {url}: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        print(f"  ⚠ Parsing error for {url}: {e}")
        return f"Parse Error: {str(e)}"

def consume():
    print("="*60)
    print("Consumer started - processing articles from Redis queue")
    print("="*60)

    while True:
        try:
            # Pop highest priority task
            result = r.zpopmax("article_queue", count=1)

            if not result:
                print("Queue empty. Waiting for new tasks...")
                time.sleep(5)
                continue

            task_data, score = result[0]
            task = json.loads(task_data)
            url = task.get("url")
            article_id = task.get("id", "unknown")
            priority = task.get("priority", "medium")

            if not url:
                print(f"✗ Task missing URL, skipping")
                continue

            print(f"\nProcessing article: {article_id}")
            print(f"  URL: {url}")
            print(f"  Priority: {priority} (score: {score})")

            # Scrape title
            title = scrape_title(url)

            # Prepare document for MongoDB
            doc = {
                "id": article_id,
                "url": url,
                "title": title,
                "priority": priority,
                "processed_at": datetime.now().isoformat()
            }

            # Insert/update in MongoDB
            result = collection.update_one(
                {"url": url},
                {"$set": doc},
                upsert=True
            )
            print(f"  ✓ Mongo update result: {result.raw_result}")

            # Small delay to avoid hammering websites
            time.sleep(1.5)

        except Exception as e:
            print(f"✗ Error processing task: {e}")
            time.sleep(2)

if __name__ == "__main__":
    consume()
