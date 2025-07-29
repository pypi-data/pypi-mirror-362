from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, Literal
from datetime import datetime

class LogEntry(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    message: str
    service_name: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    extra: Optional[Dict[str, Any]] = None
