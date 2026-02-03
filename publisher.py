import json
import os,redis

# High priority = higher score
PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

def publish_articles():
    r = redis.Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True
        )

    with open("articles.json") as f:
        articles = json.load(f)
        articles = articles["articles"]  

    for article in articles:
        score = PRIORITY_MAP.get(article["priority"].lower(), 1)
        r.zadd("article_queue", {json.dumps(article): score})
        print(f"Published task: {article['id']} - {article['url']} (priority {article['priority']})")

if __name__ == "__main__":
    publish_articles()
