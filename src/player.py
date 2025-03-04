from dataclasses import dataclass
from typing import Dict, Any
from .storage import load_data, save_data

@dataclass
class PlayerStats:
    """玩家属性"""
    attack_speed: float = 0.1  # 攻击间隔（秒）
    attack_damage: float = 1.5  # 每次攻击减少的r值
    max_health: int = 100      # 最大生命值

class Player:
    """玩家类"""
    def __init__(self):
        self.stats = PlayerStats()
        self.health = self.stats.max_health
        self.exp = 0.0
        self.gold = load_data().get("gold", 0)
        self.game_over = False
        
    def take_damage(self, damage: int) -> None:
        """受到伤害"""
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.game_over = True
            
    def reset(self) -> None:
        """重置状态（保留金币）"""
        self.health = self.stats.max_health
        self.exp = 0.0
        self.game_over = False
        
    def add_rewards(self, exp: float, gold: int) -> None:
        """增加奖励"""
        self.exp += exp
        self.gold += gold
        # 保存金币数据
        data = load_data()
        data["gold"] = self.gold
        save_data(data) 