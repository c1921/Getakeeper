from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import pathlib
from typing import List
import threading
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_: FastAPI):
    """服务生命周期管理"""
    # 启动时执行
    global target_index, player_health
    generation_state["start_time"] = time.time()
    generation_state["last_generation"] = time.time()
    generation_state["last_area_update"] = time.time()
    generation_state["points_generated"] = 0
    target_index = -1
    player_health = 100
    
    update_thread = threading.Thread(target=update_data_points, daemon=True)
    update_thread.start()
    
    yield
    
    # 关闭时执行
    pass

app = FastAPI(lifespan=lifespan)

# 挂载静态文件目录
templates_path = pathlib.Path("templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# 存储数据点的全局变量
data_points: List[dict] = []
# 存储区域r值总和的全局变量
area_sums: List[dict] = []
# 存储当前目标点的索引
target_index: int = -1
# 存储玩家生命值
player_health: int = 100
# 控制数据生成的全局变量
generation_state = {
    "points_generated": 0,
    "last_generation": 0,
    "start_time": 0,
    "last_area_update": 0
}
# 存储游戏状态
game_over: bool = False

def calculate_area_sums():
    """计算每个区域的r值总和"""
    areas = []
    # 将x轴分成10个区域（每10个单位一个区域）
    for i in range(0, 100, 10):
        area_sum = sum(
            point["r"] for point in data_points 
            if i <= point["x"] < i + 10
        )
        areas.append({
            "x": i + 5,  # 区域中点
            "y": round(area_sum, 2)
        })
    return areas

def generate_data_point() -> dict:
    """生成单个数据点"""
    return {
        "x": 100,  # 固定初始x值为100
        "y": round(random.uniform(0, 100), 2),
        "r": round(random.uniform(1, 10), 2),
        "last_damage_time": 0  # 添加上次造成伤害的时间
    }

def update_data_points():
    """更新数据点的x值并在6秒内生成新点"""
    global area_sums, target_index, player_health, game_over
    last_r_update = time.time()
    generation_interval = 6 / 50  # 6秒内生成50个点的间隔

    while True:
        if game_over:  # 如果游戏结束，停止更新
            time.sleep(0.025)
            continue
            
        current_time = time.time()
        
        # 在6秒内生成新的数据点
        if generation_state["points_generated"] < 100 and current_time - generation_state["last_generation"] >= generation_interval:
            data_points.append(generate_data_point())
            generation_state["points_generated"] += 1
            generation_state["last_generation"] = current_time
        
        # 更新所有点的x值并处理伤害
        for point in data_points:
            if point["x"] > 0:
                point["x"] = round(max(0, point["x"] - 0.15), 2)
            elif current_time - point["last_damage_time"] >= 1:
                player_health = max(0, player_health - 1)
                point["last_damage_time"] = current_time
                if player_health == 0:
                    game_over = True  # 设置游戏结束状态
                    break

        if game_over:  # 如果游戏结束，跳过后续更新
            continue
            
        # 每0.1秒更新一次r值和目标点
        if current_time - last_r_update >= 0.1:
            if data_points:
                # 找到x值最小的点的索引
                target_index = min(range(len(data_points)), key=lambda i: data_points[i]["x"])
                # 减小目标点的r值
                data_points[target_index]["r"] = round(max(0, data_points[target_index]["r"] - 1.5), 2)
                # 如果r值为0，移除该数据点
                if data_points[target_index]["r"] == 0:
                    data_points.pop(target_index)
                    target_index = -1  # 重置目标索引
                last_r_update = current_time

        # 每0.5秒更新一次区域总和
        if current_time - generation_state["last_area_update"] >= 0.5:
            area_sums = calculate_area_sums()
            generation_state["last_area_update"] = current_time
            
        time.sleep(0.025)  # 25ms更新一次

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = (templates_path / "index.html").read_text(encoding="utf-8")
    return html_content

@app.get("/generate-data")
def generate_data():
    return {
        "main_data": data_points,
        "area_sums": area_sums,
        "target_index": target_index,
        "player_health": player_health
    }

@app.post("/reset-data")
def reset_data():
    """重置所有数据点"""
    global data_points, area_sums, target_index, player_health, game_over
    data_points.clear()
    area_sums = []
    target_index = -1
    player_health = 100
    game_over = False  # 重置游戏状态
    # 重置生成状态
    generation_state["start_time"] = time.time()
    generation_state["last_generation"] = time.time()
    generation_state["last_area_update"] = time.time()
    generation_state["points_generated"] = 0
    return {"status": "success"}