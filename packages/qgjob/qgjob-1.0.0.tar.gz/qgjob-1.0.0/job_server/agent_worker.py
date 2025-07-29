import time
import requests
import random
import argparse
from job_server.config import API_BASE_URL

POLL_INTERVAL = 5  # seconds

def poll_and_execute(target: str, app_version_id: str):
    print(f"[Agent] Starting agent for target: {target}, app_version_id: {app_version_id}")

    while True:
        try:
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

            try:
                job = res.json()
                print("[Agent] Raw job response:", job)
                job_id = job["job_id"]
                test_path = job["test_path"]
            except Exception as e:
                print(f"[Agent] Failed to parse job response or missing fields: {e}")
                print("[Agent] Raw response text:", res.text)
                time.sleep(POLL_INTERVAL)
                continue

            print(f"[Agent] Running test: {test_path} (Job ID: {job_id})")

            # Simulate test execution
            time.sleep(3)
            status = random.choice(["completed", "failed"])
            print(f"[Agent] Job {job_id} finished with status: {status}")

            # Report job completion
            response = requests.post(
                f"{API_BASE_URL}/jobs/{job_id}/status",
                json={"status": status},
                timeout=5
            )
            if response.status_code != 200:
                print(f"[Agent] Failed to update job status: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[Agent] Error: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent worker to process jobs.")
    parser.add_argument("--target", type=str, default="emulator", help="Target type (emulator, device, browserstack)")
    parser.add_argument("--app-version-id", type=str, default="abc123", help="App version ID")
    args = parser.parse_args()

    poll_and_execute(args.target, args.app_version_id)
