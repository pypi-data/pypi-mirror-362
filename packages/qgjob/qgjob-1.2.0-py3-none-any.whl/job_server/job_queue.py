import redis
import json
from job_server.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def enqueue_job(job_data):
    key = f"queue:{job_data['target']}:{job_data['app_version_id']}"
    # Use priority as score (lower = higher priority)
    r.zadd(key, {json.dumps(job_data): job_data['priority']})

def dequeue_job(target, app_version_id):
    key = f"queue:{target}:{app_version_id}"
    # Get the job with the lowest score (highest priority)
    jobs = r.zrange(key, 0, 0)
    if not jobs:
        return None
    job_json = jobs[0]
    if isinstance(job_json, bytes):
        job_json = job_json.decode('utf-8')
    r.zrem(key, job_json)
    return json.loads(job_json)
