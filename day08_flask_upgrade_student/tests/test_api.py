import sys
from pathlib import Path
# 把项目根目录加入Python搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from app import app

# 模拟登录工具
def login(client):
    client.post("/login", data={"username":"student","password":"day07"})

# 测试1：健康接口 /health 无需登录，返回200
def test_health_ok():
    client = app.test_client()
    resp = client.get("/health")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["ok"] == True

# 测试2：未登录访问API，被拦截返回401
def test_api_no_login():
    client = app.test_client()
    resp = client.get("/api/metrics")
    data = resp.get_json()
    assert resp.status_code == 401
    assert data["ok"] == False

# 测试3：登录后正常获取指标接口数据
def test_api_metrics_login():
    client = app.test_client()
    login(client)
    resp = client.get("/api/metrics")
    data = resp.get_json()
    assert data["ok"] == True
    assert len(data["metrics"]) == 4

# 测试4：category筛选参数生效（加分用例）
def test_api_category_filter():
    client = app.test_client()
    login(client)
    resp = client.get("/api/categories?category=Fashion")
    data = resp.get_json()
    assert data["category"] == "Fashion"