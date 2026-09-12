import json
import os
import time

DATA_FILE = os.path.join(os.path.dirname(__file__), "bot_data.json")

_data = None


def _default():
    return {
        "xp": {},
        "settings": {},
        "reaction_roles": {},
    }


def load():
    global _data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            _data = json.load(f)
    else:
        _data = _default()
        save()


def save():
    global _data
    if _data is None:
        _data = _default()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(_data, f, indent=2, ensure_ascii=False)


def _key(guild_id, user_id):
    return f"{guild_id}:{user_id}"


def get_xp(guild_id, user_id):
    return _data["xp"].get(_key(guild_id, user_id), {"xp": 0, "level": 0})


def set_xp(guild_id, user_id, xp_value, level_value=None):
    k = _key(guild_id, user_id)
    if level_value is None:
        level_value = xp_value // 100
    _data["xp"][k] = {"xp": xp_value, "level": level_value}
    save()


def add_xp(guild_id, user_id, amount):
    k = _key(guild_id, user_id)
    entry = _data["xp"].get(k, {"xp": 0, "level": 0})
    entry["xp"] += amount
    new_level = entry["xp"] // 100
    leveled_up = new_level > entry["level"]
    entry["level"] = new_level
    _data["xp"][k] = entry
    save()
    return entry, leveled_up


def remove_xp(guild_id, user_id, amount):
    k = _key(guild_id, user_id)
    entry = _data["xp"].get(k, {"xp": 0, "level": 0})
    entry["xp"] = max(0, entry["xp"] - amount)
    entry["level"] = entry["xp"] // 100
    _data["xp"][k] = entry
    save()
    return entry


def reset_xp(guild_id, user_id):
    k = _key(guild_id, user_id)
    _data["xp"][k] = {"xp": 0, "level": 0}
    save()


def get_all_xp():
    return _data["xp"]


def get_leaderboard(guild_id, limit=10):
    results = []
    prefix = f"{guild_id}:"
    for k, v in _data["xp"].items():
        if k.startswith(prefix):
            uid = int(k.split(":", 1)[1])
            results.append((uid, v["xp"], v["level"]))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]


def get_guild_setting(guild_id, key, default=None):
    g = _data["settings"].get(str(guild_id), {})
    return g.get(key, default)


def set_guild_setting(guild_id, key, value):
    gid = str(guild_id)
    if gid not in _data["settings"]:
        _data["settings"][gid] = {}
    _data["settings"][gid][key] = value
    save()


def get_reaction_role(message_id):
    return _data["reaction_roles"].get(str(message_id))


def set_reaction_role(message_id, emoji, role_id):
    _data["reaction_roles"][str(message_id)] = {"emoji": str(emoji), "role_id": role_id}
    save()


def remove_reaction_role(message_id):
    _data["reaction_roles"].pop(str(message_id), None)
    save()


load()
