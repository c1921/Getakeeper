# 存储游戏状态的全局变量
from typing import List
from .enemy import Enemy
from .storage import load_data, save_gold

# 玩家相关
MAX_HEALTH = 100
player_health: int = MAX_HEALTH
game_over: bool = False
exp: float = 0  # 经验值（本局）
gold: int = load_data()["gold"]  # 从存档加载金币数据

# 敌人相关
enemies: List[Enemy] = []
area_sums: List[dict] = []
target_index: int = -1

# 生成控制
generation_state = {
    "points_generated": 0,
    "last_generation": 0,
    "start_time": 0,
    "last_area_update": 0
} 