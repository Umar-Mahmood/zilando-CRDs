import time
import psycopg2
from kubernetes import client, config, watch

# Load Kubernetes config
config.load_incluster_config()

v1 = client.CustomObjectsApi()

DB_HOST = "acid-minimal-cluster"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "your_postgres_password"

def create_user(username, password, roles, database):
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE USER {username} WITH PASSWORD '{password}';")
        for role in roles:
            cur.execute(f"GRANT {role} TO {username};")
        cur.execute(f"GRANT CONNECT ON DATABASE {database} TO {username};")
        conn.close()
        print(f"User {username} created successfully.")
    except Exception as e:
        print(f"Error creating user: {e}")

def watch_users():
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_custom_object, "acid.zalan.do", "v1", "argocd-zilando", "postgresqlusers"):
        user_spec = event["object"]["spec"]
        username = user_spec["username"]
        password = user_spec["password"]
        database = user_spec["database"]
        roles = user_spec["roles"]

        if event["type"] == "ADDED":
            create_user(username, password, roles, database)

if __name__ == "__main__":
    watch_users()
