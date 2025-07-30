import requests
import json
from datetime import datetime
from .utils import get_index_name
from .schema import LogEntry

class ElkLogger:
    def __init__(self, env, application_name, url, user, password, verify_ssl=True):
        self.env = env
        self.app_name = application_name
        self.url = url.rstrip("/")
        self.user = user
        self.password = password
        self.verify_ssl = verify_ssl

    def log(self, entry: LogEntry):
        index = get_index_name(self.env, self.app_name)
        endpoint = f"{self.url}/{index}/_doc"

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "env": self.env,
            "application_name": self.app_name,
            "level": entry.level,
            "message": entry.message,
            **(entry.extra or {})
        }

        headers = {"Content-Type": "application/json"}
        auth = (self.user, self.password)

        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload), auth=auth, verify=self.verify_ssl)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[ELK LOG ERROR] Failed to log: {e}")
