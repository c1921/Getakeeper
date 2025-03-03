from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import pathlib
import asyncio
from typing import List
import threading
import time

app = FastAPI()

# 挂载静态文件目录
templates_path = pathlib.Path("templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# 存储数据点的全局变量
data_points: List[dict] = []
# 控制数据生成的全局变量
generation_state = {
    "points_generated": 0,
    "last_generation": 0,
    "start_time": 0
}

def generate_data_point() -> dict:
    """生成单个数据点"""
    return {
        "x": 100,  # 固定初始x值为100
        "y": round(random.uniform(0, 100), 2),
        "r": round(random.uniform(1, 10), 2)
    }

def update_data_points():
    """更新数据点的x值并在6秒内生成新点"""
    last_r_update = time.time()
    generation_interval = 6 / 100  # 6秒内生成100个点的间隔

    while True:
        current_time = time.time()
        
        # 在6秒内生成新的数据点
        if generation_state["points_generated"] < 100 and current_time - generation_state["last_generation"] >= generation_interval:
            data_points.append(generate_data_point())
            generation_state["points_generated"] += 1
            generation_state["last_generation"] = current_time
        
        # 更新所有点的x值
        for point in data_points:
            if point["x"] > 0:
                point["x"] = round(max(0, point["x"] - 0.15), 2)
        
        # 每0.6秒更新一次r值
        if current_time - last_r_update >= 0.6:
            if data_points:  # 确保还有数据点
                min_x_point = min(data_points, key=lambda p: p["x"])
                # 减小r值
                min_x_point["r"] = round(max(0, min_x_point["r"] - 15), 2)
                # 如果r值为0，移除该数据点
                if min_x_point["r"] == 0:
                    data_points.remove(min_x_point)
                last_r_update = current_time
            
        time.sleep(0.025)  # 25ms更新一次

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化数据并启动更新线程"""
    # 初始化生成状态
    generation_state["start_time"] = time.time()
    generation_state["last_generation"] = time.time()
    generation_state["points_generated"] = 0
    
    # 启动更新线程
    update_thread = threading.Thread(target=update_data_points, daemon=True)
    update_thread.start()

@app.get("/", response_class=HTMLResponse)
async def root():
    # 读取并返回 HTML 文件
    html_content = (templates_path / "index.html").read_text(encoding="utf-8")
    return html_content

@app.get("/generate-data")
def generate_data():
    return data_points

@app.post("/reset-data")
def reset_data():
    """重置所有数据点"""
    global data_points
    data_points.clear()  # 清空现有数据点
    # 重置生成状态
    generation_state["start_time"] = time.time()
    generation_state["last_generation"] = time.time()
    generation_state["points_generated"] = 0
    return {"status": "success"}