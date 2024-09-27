import psutil
import subprocess
import time
import os

# Path to your GUI app executable
gui_app_path = os.path.abspath("./TSS-BROWSERLOCK.exe")

while True:
    # Check if Edge is running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'msedge.exe':
            proc.kill()  # Kill the Edge process
            break
    
    # Start your GUI app
    subprocess.Popen(gui_app_path)
    time.sleep(5)  # Wait before checking again to avoid rapid looping
