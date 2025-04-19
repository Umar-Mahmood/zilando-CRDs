import os
import time
import yaml
import subprocess
from datetime import datetime

REPO_PATH = "/path/to/zilando-CRDs"  # ← change this
MANIFEST_PATH = os.path.join(REPO_PATH, "UserManifests", "users.yaml")

def write_users(num_users):
    users = []
    for i in range(num_users):
        users.append({
            "username": f"user_{i}",
            "password": "pass123",
            "roles": ["read"],
            "database": "postgres"
        })

    users_yaml = {
        "users": users,
        "timestamp": datetime.now().isoformat()
    }

    with open(MANIFEST_PATH, "w") as f:
        yaml.dump(users_yaml, f)

def commit_and_push():
    subprocess.run(["git", "add", "."], cwd=REPO_PATH)
    subprocess.run(["git", "commit", "-m", f"update @ {datetime.now().isoformat()}"], cwd=REPO_PATH)
    subprocess.run(["git", "push"], cwd=REPO_PATH)

def run_test():
    for delay in [30, 15, 10, 5, 2, 1]:  # seconds between updates
        print(f"\n⏱️ Starting phase: 1 update every {delay}s")
        for i in range(5):  # 5 commits per phase
            write_users(i + 1)
            commit_and_push()
            print(f"✅ Pushed update {i+1} @ delay {delay}s")
            time.sleep(delay)

if __name__ == "__main__":
    run_test()
