import pygetwindow as gw
import pyautogui
import pandas as pd
from datetime import datetime
import os
import time

USAGE_LOG = "usage_log.csv"
SCREENSHOT_DIR = "screenshots"

def get_active_window():
    try:
        win = gw.getActiveWindow()
        return win.title if win else "Unknown"
    except:
        return "Error"

def take_screenshot():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(SCREENSHOT_DIR, f"{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

def log_usage(title):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[timestamp, title]], columns=["timestamp", "window"])
    df.to_csv(USAGE_LOG, mode='a', index=False, header=not os.path.exists(USAGE_LOG))

def run_tracker(interval=60):
    print("Screen Tracker started... (press Ctrl+C to stop)")
    while True:
        title = get_active_window()
        log_usage(title)
        take_screenshot()
        time.sleep(interval)
