# plugins/jd_sign/data_store.py
import json
import random
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "user_data.json"

def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {}

def save_data(data: dict):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def update_user(user_id: str, pt_key: str, pt_pin: str):
    data = load_data()
    data[user_id] = {
        "pt_key": pt_key,
        "pt_pin": pt_pin,
        "autosign": data.get(user_id, {}).get("autosign", False),
        "last_update": _now()
    }
    save_data(data)

def get_user(user_id: str):
    return load_data().get(user_id)

def set_autosign(user_id: str, enable: bool = True):
    data = load_data()
    if user_id in data:
        data[user_id]["autosign"] = enable
        # data[user_id]["last_update"] = _now()
        save_data(data)

def update_last_time(user_id: str):
    data = load_data()
    if user_id in data:
        data[user_id]["last_update"] = _now()
        save_data(data)

def get_all_autosign_users():
    data = load_data()
    return {uid: info for uid, info in data.items() if info.get("autosign")}
