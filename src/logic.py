import random
import time
from . import state

def calculate_area_sums():
    """计算每个区域的r值总和"""
    areas = []
    for i in range(0, 100, 10):
        area_sum = sum(
            point["r"] for point in state.data_points 
            if i <= point["x"] < i + 10
        )
        areas.append({
            "x": i + 5,
            "y": round(area_sum, 2)
        })
    return areas

def generate_data_point() -> dict:
    """生成单个数据点"""
    return {
        "x": 100,
        "y": round(random.uniform(0, 100), 2),
        "r": round(random.uniform(1, 10), 2),
        "last_damage_time": 0
    }

def update_data_points():
    """更新数据点的x值并在6秒内生成新点"""
    last_r_update = time.time()
    generation_interval = 6 / 50

    while True:
        if state.game_over:
            time.sleep(0.025)
            continue
            
        current_time = time.time()
        
        if state.generation_state["points_generated"] < 100 and current_time - state.generation_state["last_generation"] >= generation_interval:
            state.data_points.append(generate_data_point())
            state.generation_state["points_generated"] += 1
            state.generation_state["last_generation"] = current_time
        
        for point in state.data_points:
            if point["x"] > 0:
                point["x"] = round(max(0, point["x"] - 0.15), 2)
            elif current_time - point["last_damage_time"] >= 1:
                state.player_health = max(0, state.player_health - 1)
                point["last_damage_time"] = current_time
                if state.player_health == 0:
                    state.game_over = True
                    break

        if state.game_over:
            continue
            
        if current_time - last_r_update >= 0.1:
            if state.data_points:
                state.target_index = min(range(len(state.data_points)), key=lambda i: state.data_points[i]["x"])
                state.data_points[state.target_index]["r"] = round(max(0, state.data_points[state.target_index]["r"] - 1.5), 2)
                if state.data_points[state.target_index]["r"] == 0:
                    state.data_points.pop(state.target_index)
                    state.target_index = -1
                last_r_update = current_time

        if current_time - state.generation_state["last_area_update"] >= 0.5:
            state.area_sums = calculate_area_sums()
            state.generation_state["last_area_update"] = current_time
            
        time.sleep(0.025) 