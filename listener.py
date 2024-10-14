import psutil
import subprocess
import time
import os

# Path to your GUI app executable
gui_app_path = os.path.abspath("./TSS-BROWSERLOCK.exe")

def is_gui_app_running():
    """Check if the GUI application is already running."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'TSS-BROWSERLOCK.exe':
            return True
    return False

while True:
    edge_running = False
    valid_instance_found = False  # Flag to track valid Edge instance

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'msedge.exe':
            edge_running = True
            
            if '--browserlock-verified=true' in proc.info['cmdline']:
                print("Verified Edge is open.")
                valid_instance_found = True  # Set flag for valid instance
                break  # Edge is verified; do nothing
            
            # Check if the parent process has the verified flag
            parent = proc.parent()
            if parent and '--browserlock-verified=true' not in parent.cmdline():
                print(f"Terminating non-verified Edge process: {proc.pid}")
                proc.terminate()  # Kill the Edge process
                try:
                    proc.wait(timeout=5)  # Wait for up to 5 seconds for termination
                except psutil.TimeoutExpired:
                    print("Process did not terminate in time, forcing kill.")
                    proc.kill()  # Forcefully kill if not terminated

    # Only start your GUI app if no valid instance was found
    if edge_running and not valid_instance_found:
        if not is_gui_app_running():
            subprocess.Popen(gui_app_path)

    if not edge_running:
        print("Edge is not running.")
    
    time.sleep(3)  # Wait before checking again to avoid rapid looping