import random
import time
from . import state
from .enemy import create_enemy
from .storage import save_gold  # 添加导入

def calculate_area_sums():
    """计算每个区域的r值总和"""
    areas = []
    for i in range(0, 100, 10):
        area_sum = sum(
            enemy.r for enemy in state.enemies 
            if i <= enemy.x < i + 10
        )
        areas.append({
            "x": i + 5,
            "y": round(area_sum, 2)
        })
    return areas

def update_data_points():
    """更新数据点并在6秒内生成新点"""
    last_attack_time = time.time()
    generation_interval = 6 / 50

    while True:
        if state.player.game_over:
            time.sleep(0.025)
            continue
            
        current_time = time.time()
        
        # 生成新敌人
        if state.generation_state["points_generated"] < 100 and current_time - state.generation_state["last_generation"] >= generation_interval:
            state.enemies.append(create_enemy())  # 使用工厂函数创建敌人
            state.generation_state["points_generated"] += 1
            state.generation_state["last_generation"] = current_time
        
        # 更新敌人
        for enemy in state.enemies:
            enemy.update_position()
            if enemy.deal_damage():
                state.player.take_damage(enemy.stats.damage)
                break  # 如果游戏结束，会在下一次循环时检测到

        if state.player.game_over:
            continue
            
        # 更新目标敌人
        if current_time - last_attack_time >= state.player.stats.attack_speed and state.enemies:
            state.target_index = min(range(len(state.enemies)), key=lambda i: state.enemies[i].x)
            state.enemies[state.target_index].reduce_radius(state.player.stats.attack_damage)
            
            if state.enemies[state.target_index].is_dead():
                enemy = state.enemies.pop(state.target_index)
                # 击杀奖励
                state.player.add_rewards(
                    exp=enemy.stats.radius,
                    gold=int(enemy.stats.radius)
                )
                state.target_index = -1
            last_attack_time = current_time

        # 更新区域总和
        if current_time - state.generation_state["last_area_update"] >= 0.5:
            state.area_sums = calculate_area_sums()
            state.generation_state["last_area_update"] = current_time
            
        time.sleep(0.025) 