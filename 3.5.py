from os import times
import time
import psutil
import os
import hashlib
import json
import requests
from ctypes import windll, wintypes, byref

# 常量定义
CONFIG_URL = 'http://json.yyyweb.top:10086/config.json'  # 替换为您的配置文件URL
COUNTER_FILE = 'ZBKV8-UEFI.txt'
MD5_CACHE_FILE = 'md5_cache.json'


# 辅助函数
def load_config_json():
    response = requests.get(CONFIG_URL)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Failed to load config from {CONFIG_URL} with status code {response.status_code}")
        return None


def load_md5_cache():
    try:
        with open(MD5_CACHE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_md5_cache(md5_cache):
    with open(MD5_CACHE_FILE, 'w') as f:
        json.dump(md5_cache, f)


def calculate_md5(file_path, md5_cache):
    if file_path in md5_cache:
        return md5_cache[file_path]
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    md5 = md5_hash.hexdigest()
    md5_cache[file_path] = md5
    return md5


def get_foreground_window_process_md5():
    hwnd = windll.user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process = psutil.Process(pid.value)
    exe_path = process.exe()
    md5_cache = load_md5_cache()
    md5 = calculate_md5(exe_path, md5_cache)
    save_md5_cache(md5_cache)
    return md5


def get_current_run_count():
    try:
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


def save_run_count(count):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(count))


def close_target_app(process):
    try:
        process.kill()
        print(f"Killed process {process.pid} with name '{process.name()}'")
    except (psutil.NoSuchProcess, PermissionError) as e:
        print(f"Failed to kill process: {e}")


def main():
    config = load_config_json()
    if not config:
        return

    target_md5s = config.get('config-md5', [])
    max_runs = config.get('max_runs', 1)  # -1 表示无限次运行

    run_count = get_current_run_count()
    while run_count < max_runs or max_runs == 1:
        try:
            foreground_md5 = get_foreground_window_process_md5()
            if foreground_md5 in target_md5s:
                hwnd = windll.user32.GetForegroundWindow()
                pid = wintypes.DWORD()
                windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
                process = psutil.Process(pid.value)
                close_target_app(process)
                run_count += 1
                save_run_count(run_count)
                print(f"Run count increased to {run_count}. Process with MD5 {foreground_md5} was closed.")
            else:
                print(f"Foreground process MD5 {foreground_md5} is not in the target list.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # 等待一段时间再次检查
        time.sleep(5)

    print("Max runs reached or the program was manually stopped.")


# 主程序入口
if __name__ == '__main__':
    main()
