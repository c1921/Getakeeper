import random
import time
from dataclasses import dataclass
from enum import Enum, auto

class EnemyType(Enum):
    """敌人类型枚举"""
    NORMAL = auto()
    FAST = auto()

@dataclass
class EnemyStats:
    """敌人属性数据类"""
    radius: float
    damage: int
    damage_interval: float
    speed: float

# 使用枚举值作为键
ENEMY_STATS = {
    EnemyType.NORMAL: EnemyStats(
        radius=8.0,
        damage=1,
        damage_interval=1.0,
        speed=0.15
    ),
    EnemyType.FAST: EnemyStats(
        radius=4.0,
        damage=1,
        damage_interval=0.5,
        speed=0.225
    )
}

class Enemy:
    """统一的敌人类"""
    def __init__(self, enemy_type: EnemyType):
        self.enemy_type = enemy_type
        self.stats = ENEMY_STATS[enemy_type]
        self.x = 100
        self.y = round(random.uniform(0, 100), 2)
        self.r = self.stats.radius
        self.last_damage_time = 0
        
    def update_position(self) -> None:
        """更新敌人位置"""
        if self.x > 0:
            self.x = round(max(0, self.x - self.stats.speed), 2)
            
    def deal_damage(self) -> bool:
        """处理伤害逻辑"""
        current_time = time.time()
        if self.x == 0 and current_time - self.last_damage_time >= self.stats.damage_interval:
            self.last_damage_time = current_time
            return True
        return False
        
    def reduce_radius(self, amount: float = 1.5) -> None:
        """减小半径"""
        self.r = round(max(0, self.r - amount), 2)
        
    def is_dead(self) -> bool:
        """检查是否应该移除"""
        return self.r <= 0
        
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "x": self.x,
            "y": self.y,
            "r": self.r,
            "last_damage_time": self.last_damage_time,
            "type": self.enemy_type.name
        }

def create_enemy(enemy_type: EnemyType = None) -> Enemy:
    """敌人工厂函数"""
    if enemy_type is None:
        enemy_type = random.choices(
            list(EnemyType),
            weights=[2, 1]  # 普通敌人:快速敌人 = 2:1
        )[0]
    
    return Enemy(enemy_type) 