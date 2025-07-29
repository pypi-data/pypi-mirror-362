import redis
import json
from job_server.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def enqueue_job(job_data):
    key = f"queue:{job_data['target']}:{job_data['app_version_id']}"
    r.rpush(key, json.dumps(job_data))

def dequeue_job(target, app_version_id):
    key = f"queue:{target}:{app_version_id}"
    job_json = r.lpop(key)
    return json.loads(job_json) if job_json else None
