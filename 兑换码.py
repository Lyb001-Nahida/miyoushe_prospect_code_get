import requests
import json
import time
import re
import random
import uuid
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, List, Tuple

def generate_device_fp() -> str:
    """
    生成38开头的13位16进制数
    格式：38 + 11位16进制数
    """
    # 生成11位随机16进制数
    hex_chars = ''.join(random.choices('0123456789abcdef', k=11))
    return f"38{hex_chars}"

def generate_device_id() -> str:
    """
    生成32位的UUID
    返回格式：标准的UUID格式（8-4-4-4-12）
    """
    return str(uuid.uuid4()).upper()

class MihoyobbsClient:
    def __init__(self, stuid: str, stoken: str, mid: str):
        """
        初始化米游社客户端
        
        Args:
            stuid: 用户ID
            stoken: 登录token
            mid: 设备mid
        """
        self.stuid = stuid
        self.stoken = stoken
        self.mid = mid
        
        # 生成随机的设备指纹和设备ID
        self.device_fp = generate_device_fp()
        self.device_id = generate_device_id()
        
        # 游戏配置映射 (gids -> 游戏名称)
        self.games = {
            "2": "原神",
            "6": "崩坏：星穹铁道", 
            "8": "绝区零"
        }
        
        # 基础URL
        self.bbs_api_url = "https://bbs-api.miyoushe.com"
        self.takumi_api_url = "https://api-takumi-static.mihoyo.com"
        
        # 公共请求头
        self.common_headers = {
            "Host": "bbs-api.miyoushe.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Hyperion/547 CFNetwork/1209 Darwin/20.2.0",
            "x-rpc-client_type": "1",
            "x-rpc-app_version": "2.102.0",
            "x-rpc-sys_version": "14.3",
            "x-rpc-channel": "appstore",
            "x-rpc-device_name": "iPad (38)",
            "x-rpc-device_model": "iPad11,6",
            "x-rpc-device_id": self.device_id,  # 使用随机生成的device_id
            "x-rpc-device_fp": self.device_fp,  # 使用随机生成的device_fp
            "x-rpc-ver
