import json
import pathlib
from typing import Dict, Any

SAVE_FILE = pathlib.Path("save/game_data.json")

def load_data() -> Dict[str, Any]:
    """加载存档数据"""
    if not SAVE_FILE.exists():
        return {"gold": 0}
    
    try:
        with SAVE_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"gold": 0}

def save_data(data: Dict[str, Any]) -> None:
    """保存数据到文件"""
    SAVE_FILE.parent.mkdir(exist_ok=True)
    with SAVE_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f)

def save_gold(gold: int) -> None:
    """保存金币数据"""
    data = load_data()
    data["gold"] = gold
    save_data(data) 