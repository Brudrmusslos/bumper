# bumper/plugins/logger_plugin.py

import json
import logging
from datetime import datetime
from pathlib import Path

_LOGGER = logging.getLogger("bumper.plugins.logger")

LOG_FILE_PATH = Path("/bumper/data/mqtt_packets.jsonl")

def log_mqtt_packet(topic: str, payload: str, client_id: str):
    timestamp = datetime.utcnow().isoformat()
    packet = {
        "timestamp": timestamp,
        "client_id": client_id,
        "topic": topic,
        "raw_payload": payload,
    }

    try:
        packet["parsed_payload"] = json.loads(payload)
    except json.JSONDecodeError:
        packet["parsed_payload"] = None

    try:
        LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(packet) + "\n")
    except Exception as e:
        _LOGGER.error(f"Failed to write MQTT packet to file: {e}", exc_info=True)


