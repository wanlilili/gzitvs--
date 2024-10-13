import psutil
import os
import time
import sys
import logging
import hashlib
import json
import requests
from ctypes import windll, wintypes, byref

def load_config_json():
    url = 'http://json.yyyweb.top:10086/config.json'
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)


def get_md5s_from_config(config):
    TARGET_APP_MD5S = config['config-md5']
    MAX_RUNS = config['max_runs']
    COUNTER_FILE = 'ZBKV8-UEFI.txt'
    MD5_CACHE_FILE = 'md5_cache.json'
    return (TARGET_APP_MD5S, MAX_RUNS)

MAX_RUNS = 1
COUNTER_FILE = 'ZBKV8-UEFI.txt'
MD5_CACHE_FILE = 'md5_cache.json'
logging.basicConfig(filename = 'ZBKV8-UEFIV7.log', level = logging.DEBUG, format = '%(asctime)s: %(message)s')

def load_md5_cache():
    pass
# WARNING: Decompyle incomplete


def save_md5_cache(md5_cache):
    pass
# WARNING: Decompyle incomplete


def calculate_md5(file_path, md5_cache):
    pass
# WARNING: Decompyle incomplete


def get_foreground_window_process_md5():
    hwnd = windll.user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process = psutil.Process(pid.value)
    exe_path = process.exe()
    md5_cache = load_md5_cache()
    return calculate_md5(exe_path, md5_cache)
# WARNING: Decompyle incomplete


def get_current_run_count():
    pass
# WARNING: Decompyle incomplete


def save_run_count(count):
    pass
# WARNING: Decompyle incomplete


def close_target_app(target_md5):
    closed_processes = []
# WARNING: Decompyle incomplete


def main():
    config = None
    config = load_config_json()
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    main()
    return None
