# logservice

An async Python module for sending structured JSON logs to AWS CloudWatch Logs from any Python application, including FastAPI, Flask, background workers, and CLI tools.

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install logservice

from fastapi import FastAPI
from logservice import AsyncCloudWatchLogService, LogEntry

app = FastAPI()

log_service = AsyncCloudWatchLogService(
    aws_access_key="...",
    aws_secret_key="...",
    region_name="us-east-1",
    log_group_name="app-logs",
    log_stream_name="login-events"
)

@app.post("/login")
async def login():
    await log_service.log(LogEntry(
        level="INFO",
        message="User logged in",
        service_name="LoginService",
        extra={"user_id": 123}"
    ))
    return {"message": "Logged"}
```