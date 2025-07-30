import hmac
import hashlib
import time
import json
import httpx
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from .tools.detect_platform import get_os
from uuid import uuid4
import fake_useragent

def get_server_time(url="https://goldfish-app-fojmb.ondigitalocean.app"):
    """
    Получает серверное время с учетом сетевой задержки и добавляет буфер
    """
    try:
        # Замеряем время запроса для расчета задержки
        start_time = time.time()
        response = httpx.get(url, timeout=10)
        end_time = time.time()
        
        server_date = response.headers.get("Date")
        if server_date:
            # Парсим серверное время
            dt = parsedate_to_datetime(server_date)
            server_timestamp = int(dt.timestamp())
            
            # Рассчитываем сетевую задержку
            network_delay = max(0, end_time - start_time)
            
            # Добавляем сетевую задержку + буфер для компенсации времени
            # между получением времени и отправкой запроса
            buffer_seconds = 2  # Уменьшаем буфер до 2 секунд
            adjusted_timestamp = server_timestamp + int(network_delay) + buffer_seconds
            
            return adjusted_timestamp
            
    except Exception as e:
        print(f"[!] Ошибка при получении серверного времени: {e}")
    
    # Fallback на локальное время с буфером
    return int(time.time()) + 2

def serialize_json_consistently(data):
    """
    Консистентная JSON-сериализация для всех платформ
    Использует настройки, совместимые с httpx и стандартной сериализацией
    """
    # ВАЖНО: Используем минимальные параметры для максимальной совместимости
    # Не используем sort_keys=True, так как это может изменить ожидаемый сервером формат
    return json.dumps(data, ensure_ascii=True, separators=(',', ':'))

def generate_headers(data):
    # Настоящий секретный ключ
    secret_key = "your-super-secret-key-replace-in-production"
    timestamp = str(get_server_time())  # Используем правильное имя функции

    # Используем консистентную сериализацию
    # КРИТИЧНО: Этот JSON должен точно совпадать с тем, что отправляет httpx
    data_json = serialize_json_consistently(data)

    # Подпись HMAC(timestamp + data_json)
    message = timestamp + data_json
    key_bytes = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    signature = hmac_obj.hexdigest()

    # Заголовки
    headers = {
        "X-API-Key": "62852b00cb9e44bca86f0ec7e7455dc6",
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.aiuncensored.info",
        "Referer": "https://www.aiuncensored.info/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    }

    return headers


def generate_image_headers():
    return {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': str(uuid4()),
        'origin': 'https://arting.ai',
        'referer': 'https://arting.ai/',
        'user-agent': fake_useragent.UserAgent().random
    }