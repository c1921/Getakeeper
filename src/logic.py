import random
import time
from . import state
from .enemy import create_enemy

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
    last_r_update = time.time()
    generation_interval = 6 / 50

    while True:
        if state.game_over:
            time.sleep(0.025)
            continue
            
        current_time = time.time()
        
        # 生成新敌人
        if state.generation_state["points_generated"] < 100 and current_time - state.generation_state["last_generation"] >= generation_interval:
            state.enemies.append(create_enemy())  # 使用工厂函数创建敌人
            state.generation_state["points_generated"] += 1
            state.generation_state["last_generation"] = current_time
        
        # 更新敌人
        for i, enemy in enumerate(state.enemies):
            enemy.update_position()
            if enemy.deal_damage():
                state.player_health = max(0, state.player_health - 1)
                if state.player_health == 0:
                    state.game_over = True
                    break

        if state.game_over:
            continue
            
        # 更新目标敌人
        if current_time - last_r_update >= 0.1 and state.enemies:
            state.target_index = min(range(len(state.enemies)), key=lambda i: state.enemies[i].x)
            state.enemies[state.target_index].reduce_radius()
            
            if state.enemies[state.target_index].is_dead():
                state.enemies.pop(state.target_index)
                state.target_index = -1
            last_r_update = current_time

        # 更新区域总和
        if current_time - state.generation_state["last_area_update"] >= 0.5:
            state.area_sums = calculate_area_sums()
            state.generation_state["last_area_update"] = current_time
            
        time.sleep(0.025) 