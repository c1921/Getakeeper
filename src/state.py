# 存储游戏状态的全局变量
from typing import List

# 玩家相关
MAX_HEALTH = 100
player_health: int = MAX_HEALTH
game_over: bool = False

# 数据点相关
data_points: List[dict] = []
area_sums: List[dict] = []
target_index: int = -1

# 生成控制
generation_state = {
    "points_generated": 0,
    "last_generation": 0,
    "start_time": 0,
    "last_area_update": 0
} 