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

def generate_random_points(count: int = 100) -> List[dict]:
    """生成指定数量的随机数据点"""
    return [
        {
            "x": round(random.uniform(0, 100), 2),
            "y": round(random.uniform(0, 100), 2),
            "r": round(random.uniform(1, 10), 2)
        }
        for _ in range(count)
    ]

def update_data_points():
    """更新数据点的x值"""
    while True:
        for point in data_points:
            if point["x"] > 0:
                # 每25ms减少0.15，保留两位小数
                point["x"] = round(max(0, point["x"] - 0.15), 2)
        time.sleep(0.025)  # 25ms更新一次

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化数据并启动更新线程"""
    # 生成初始数据
    global data_points
    data_points = generate_random_points()
    
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
    data_points = generate_random_points()
    return {"status": "success"} 