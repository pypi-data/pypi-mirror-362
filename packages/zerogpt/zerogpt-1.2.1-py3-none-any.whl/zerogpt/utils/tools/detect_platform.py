#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os

def get_os():
    """
    Определяет операционную систему пользователя
    Возвращает название ОС (Windows, Linux, macOS, Android)
    """
    system = platform.system()
    
    if system == 'Windows':
        return 'Windows'
    elif system == 'Linux':
        # Проверяем, является ли это Android
        if any(os.path.exists(path) for path in ['/system/build.prop', '/system/bin/getprop', '/data/data', '/system/app']):
            return 'Android'
        return 'Linux'
    elif system == 'Darwin':
        return 'macOS'
    
    return 'Unknown'