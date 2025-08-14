# push.py 支持 PushPlus 、wxpusher、Telegram、Bark 的消息推送模块
import os
import random
import time
import json
import requests
import logging
from config import PUSHPLUS_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN, WXPUSHER_SPT, BARK_DEVICE_TOKEN

logger = logging.getLogger(__name__)


class PushNotification:
    def __init__(self):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.telegram_url = "https://api.telegram.org/bot{}/sendMessage"
        self.bark_url = "https://api.day.app/push"  # Bark推送API
        self.headers = {'Content-Type': 'application/json'}
        # 从环境变量获取代理设置
        self.proxies = {
            'http': os.getenv('http_proxy'),
            'https': os.getenv('https_proxy')
        }
        self.wxpusher_simple_url = "https://wxpusher.zjiecode.com/api/send/message/{}/{}"

    def push_pushplus(self, content, token):
        """PushPlus消息推送"""
        # 原有实现保持不变...
        
    def push_telegram(self, content, bot_token, chat_id):
        """Telegram消息推送，失败时自动尝试直连"""
        # 原有实现保持不变...

    def push_wxpusher(self, content, spt):
        """WxPusher消息推送（极简方式）"""
        # 原有实现保持不变...

    def push_bark(self, content, device_token):
        """Bark消息推送"""
        attempts = 5
        for attempt in range(attempts):
            try:
                payload = {
                    "device_key": device_token,
                    "title": "微信阅读推送",
                    "body": content,
                    "group": "微信阅读"
                }
                response = requests.post(
                    self.bark_url,
                    json=payload,
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                logger.info("✅ Bark响应: %s", response.text)
                return True
            except requests.exceptions.RequestException as e:
                logger.error("❌ Bark推送失败: %s", e)
                if attempt < attempts - 1:
                    sleep_time = random.randint(180, 360)
                    logger.info("将在 %d 秒后重试...", sleep_time)
                    time.sleep(sleep_time)
        return False


"""外部调用"""


def push(content, method):
    """统一推送接口，支持 PushPlus、Telegram、WxPusher 和 Bark"""
    notifier = PushNotification()

    if method == "pushplus":
        token = PUSHPLUS_TOKEN
        return notifier.push_pushplus(content, token)
    elif method == "telegram":
        bot_token = TELEGRAM_BOT_TOKEN
        chat_id = TELEGRAM_CHAT_ID
        return notifier.push_telegram(content, bot_token, chat_id)
    elif method == "wxpusher":
        return notifier.push_wxpusher(content, WXPUSHER_SPT)
    elif method == "bark":
        device_token = BARK_DEVICE_TOKEN
        return notifier.push_bark(content, device_token)
    else:
        raise ValueError("❌ 无效的通知渠道，请选择 'pushplus'、'telegram'、'wxpusher' 或 'bark'")
