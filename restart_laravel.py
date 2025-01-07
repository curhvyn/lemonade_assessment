import psutil
import os
import time

# Function to get current CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to restart Laravel backend service
def restart_laravel():
    print("CPU usage exceeded 80%. Restarting Laravel backend service...")
    os.system("sudo systemctl restart laravel-worker")  

if __name__ == "__main__":
    while True:
        cpu_usage = get_cpu_usage()
        print(f"Current CPU Usage: {cpu_usage}%")
        
        if cpu_usage > 80:
            restart_laravel()
        
        time.sleep(10)  # Check CPU usage every 10 seconds
