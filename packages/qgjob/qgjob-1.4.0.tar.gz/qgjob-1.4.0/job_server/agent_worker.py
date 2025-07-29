import time
import requests
import random
import argparse
import redis
from job_server.config import API_BASE_URL, REDIS_URL

POLL_INTERVAL = 5  # seconds

def poll_and_execute(target: str, app_version_id: str):
    print(f"[Agent] Starting agent for target: {target}, app_version_id: {app_version_id}")
    r = redis.Redis.from_url(REDIS_URL)

    while True:
        try:
            if app_version_id == "all":
                # List all app_version_ids for this target
                keys = r.keys(f"queue:{target}:*")
                found_job = False
                for key in keys:
                    app_ver = key.decode().split(":")[-1]
                    res = requests.get(
                        f"{API_BASE_URL}/agents/next-job",
                        params={"target": target, "app_version_id": app_ver},
                        timeout=5
                    )
                    if res.status_code == 200:
                        found_job = True
                        job = res.json()
                        job_id = job["job_id"]
                        test_path = job["test_path"]
                        print(f"[Agent] Running test: {test_path} (Job ID: {job_id})")
                        time.sleep(3)
                        if "fail" in test_path:
                            status = "failed"
                        elif "pass" in test_path or "onboarding" in test_path:
                            status = "completed"
                        else:
                            status = "completed"
                        print(f"[Agent] Job {job_id} finished with status: {status}")
                        response = requests.post(
                            f"{API_BASE_URL}/jobs/{job_id}/status",
                            json={"status": status},
                            timeout=5
                        )
                        if response.status_code != 200:
                            print(f"[Agent] Failed to update job status: {response.status_code} - {response.text}")
                        break
                if not found_job:
                    print("[Agent] No jobs available. Sleeping 5s...")
                    time.sleep(POLL_INTERVAL)
                    continue
            else:
                res = requests.get(
                    f"{API_BASE_URL}/agents/next-job",
                    params={"target": target, "app_version_id": app_version_id},
                    timeout=5
                )
                if res.status_code == 204:
                    print("[Agent] No jobs available. Sleeping 5s...")
                    time.sleep(POLL_INTERVAL)
                    continue
                if res.status_code != 200:
                    print(f"[Agent] Unexpected status code {res.status_code}: {res.text}")
                    time.sleep(POLL_INTERVAL)
                    continue
                job = res.json()
                if "message" in job and job["message"] == "No job available":
                    print("[Agent] No jobs available. Sleeping 5s...")
                    time.sleep(POLL_INTERVAL)
                    continue
                job_id = job["job_id"]
                test_path = job["test_path"]
                print(f"[Agent] Running test: {test_path} (Job ID: {job_id})")
                time.sleep(3)
                if "fail" in test_path:
                    status = "failed"
                elif "pass" in test_path or "onboarding" in test_path:
                    status = "completed"
                else:
                    status = "completed"
                print(f"[Agent] Job {job_id} finished with status: {status}")
                response = requests.post(
                    f"{API_BASE_URL}/jobs/{job_id}/status",
                    json={"status": status},
                    timeout=5
                )
                if response.status_code != 200:
                    print(f"[Agent] Failed to update job status: {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[Agent] Error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent worker to process jobs.")
    parser.add_argument("--target", type=str, default="emulator", help="Target type (emulator, device, browserstack)")
    parser.add_argument("--app-version-id", type=str, default="abc123", help="App version ID")
    args = parser.parse_args()

    poll_and_execute(args.target, args.app_version_id)
