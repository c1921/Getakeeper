from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib
import threading
import time
from contextlib import asynccontextmanager
from src import state, logic
from src.enemy import Enemy, EnemyType

@asynccontextmanager
async def lifespan(_: FastAPI):
    """服务生命周期管理"""
    # 启动时执行
    state.generation_state["start_time"] = time.time()
    state.generation_state["last_generation"] = time.time()
    state.generation_state["last_area_update"] = time.time()
    state.generation_state["points_generated"] = 0
    state.target_index = -1
    state.player_health = state.MAX_HEALTH
    
    update_thread = threading.Thread(target=logic.update_data_points, daemon=True)
    update_thread.start()
    
    yield
    
    # 关闭时执行
    pass

app = FastAPI(lifespan=lifespan)

# 挂载静态文件目录
templates_path = pathlib.Path("templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = (templates_path / "index.html").read_text(encoding="utf-8")
    return html_content

@app.get("/generate-data")
def generate_data():
    # 将敌人按类型分组
    normal_enemies = [e.to_dict() for e in state.enemies if e.enemy_type == EnemyType.NORMAL]
    fast_enemies = [e.to_dict() for e in state.enemies if e.enemy_type == EnemyType.FAST]
    
    return {
        "normal_enemies": normal_enemies,
        "fast_enemies": fast_enemies,
        "area_sums": state.area_sums,
        "target_index": state.target_index,
        "player_health": state.player_health,
        "max_health": state.MAX_HEALTH
    }

@app.post("/reset-data")
def reset_data():
    """重置所有数据点"""
    state.enemies.clear()
    state.area_sums = []
    state.target_index = -1
    state.player_health = state.MAX_HEALTH
    state.game_over = False
    
    state.generation_state["start_time"] = time.time()
    state.generation_state["last_generation"] = time.time()
    state.generation_state["last_area_update"] = time.time()
    state.generation_state["points_generated"] = 0
    return {"status": "success"}