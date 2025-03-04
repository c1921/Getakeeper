import random
import time
from abc import ABC, abstractmethod
from enum import Enum, auto

class EnemyType(Enum):
    """敌人类型枚举"""
    NORMAL = auto()
    FAST = auto()

class BaseEnemy(ABC):
    """敌人基类"""
    def __init__(self):
        self.x = 100
        self.y = round(random.uniform(0, 100), 2)
        self.r = round(random.uniform(1, 10), 2)
        self.last_damage_time = 0
        
    @abstractmethod
    def update_position(self) -> None:
        """更新敌人位置"""
        pass
            
    def deal_damage(self) -> bool:
        """处理伤害逻辑"""
        current_time = time.time()
        if self.x == 0 and current_time - self.last_damage_time >= 1:
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
            "type": self.__class__.__name__
        }

class NormalEnemy(BaseEnemy):
    """普通敌人：匀速移动"""
    def update_position(self) -> None:
        if self.x > 0:
            self.x = round(max(0, self.x - 0.15), 2)

class FastEnemy(BaseEnemy):
    """快速敌人：速度是普通敌人的1.5倍，但半径较小"""
    def __init__(self):
        super().__init__()
        self.r = round(random.uniform(1, 5), 2)  # 更小的半径
        
    def update_position(self) -> None:
        if self.x > 0:
            self.x = round(max(0, self.x - 0.6), 2)  # 1.5倍速度

def create_enemy(enemy_type: EnemyType = None) -> BaseEnemy:
    """敌人工厂函数"""
    enemy_classes = {
        EnemyType.NORMAL: NormalEnemy,
        EnemyType.FAST: FastEnemy
    }
    
    if enemy_type is None:
        enemy_type = random.choices(
            list(enemy_classes.keys()),
            weights=[2, 1]  # 普通敌人:快速敌人 = 2:1
        )[0]
        
    return enemy_classes[enemy_type]() 