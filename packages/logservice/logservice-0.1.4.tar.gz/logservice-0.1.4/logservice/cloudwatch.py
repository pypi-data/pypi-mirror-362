import aioboto3
import json
import time
import uuid
from .schema import LogEntry

MAX_LOG_SIZE = 256 * 1024  # 256 KB

class CloudWatchLogService:
    def __init__(self, aws_access_key, aws_secret_key, region_name, log_group_name, log_stream_name):
        self.config = {
            "aws_access_key_id": aws_access_key,
            "aws_secret_access_key": aws_secret_key,
            "region_name": region_name
        }
        self.log_group = log_group_name
        self.log_stream = log_stream_name
        self.sequence_token = None

    async def _ensure_stream(self, client):
        streams = await client.describe_log_streams(
            logGroupName=self.log_group,
            logStreamNamePrefix=self.log_stream
        )
        if streams["logStreams"]:
            self.sequence_token = streams["logStreams"][0].get("uploadSequenceToken")
        else:
            await client.create_log_stream(
                logGroupName=self.log_group,
                logStreamName=self.log_stream
            )

    async def log(self, entry: LogEntry):
        # Ensure correlation_id is present
        if entry.extra is None:
            entry.extra = {}
        if "correlation_id" not in entry.extra:
            entry.extra["correlation_id"] = str(uuid.uuid4())

        log_dict = entry.dict()
        log_dict["timestamp"] = log_dict["timestamp"].isoformat()

        message_str = json.dumps(log_dict, default=str)

        if len(message_str.encode("utf-8")) > MAX_LOG_SIZE:
            # Truncate log
            message_str = json.dumps({
                "level": entry.level,
                "message": "Log message too large. Truncated to fit CloudWatch limits.",
                "service_name": entry.service_name,
                "timestamp": entry.timestamp.isoformat(),
                "extra_summary": {
                    "original_keys": list(log_dict.keys()),
                    "note": "Log was too large and has been trimmed."
                }
            })

        log_event = {
            "timestamp": int(time.time() * 1000),
            "message": message_str
        }

        kwargs = {
            "logGroupName": self.log_group,
            "logStreamName": self.log_stream,
            "logEvents": [log_event]
        }

        if self.sequence_token:
            kwargs["sequenceToken"] = self.sequence_token

        async with aioboto3.client("logs", **self.config) as client:
            await self._ensure_stream(client)

            try:
                response = await client.put_log_events(**kwargs)
                self.sequence_token = response.get("nextSequenceToken")

            except client.exceptions.InvalidSequenceTokenException:
                # Retry with fresh sequence token
                await self._ensure_stream(client)
                kwargs["sequenceToken"] = self.sequence_token
                response = await client.put_log_events(**kwargs)
                self.sequence_token = response.get("nextSequenceToken")
