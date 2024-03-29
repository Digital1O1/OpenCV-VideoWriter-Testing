import psutil
from sshkeyboard import listen_keyboard, stop_listening
import time
import threading
import os
import csv
import cv2

# Global boolean to exit program
exit_flag = False

# Filename for CSV
file_name = 'computerMetrics.csv'

duration = 20
interval = 0.1


'''


'''



 # Set end time for data collection

end_time = time.time() + duration 

#while not exit_flag:

print("Starting sampling now")
while time.time() < end_time:
    with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'CPU Usage System Wide (%)', 'Swap Memory Total (bytes)', 'Swap Memory Used (bytes)', 'Swap Memory Free (bytes)', 'Swap Memory Percentage (%)', 'Individual CPU Usage (%)', 'Virtual Memory Total (bytes)', 'Virtual Memory Available (bytes)', 'Virtual Memory Percentage (%)', 'Virtual Memory Used (bytes)', 'Virtual Memory Free (bytes)', 'Virtual Memory Active (bytes)', 'Virtual Memory Buffer (bytes)', 'Virtual Memory Cache (bytes)', 'Virtual Memory Shared (bytes)'])

            
            end_time = time.time() + duration
            while time.time() < end_time and not exit_flag:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                systemWideCPUUsage = psutil.cpu_percent(interval=interval)
                
                # Swapped memory variables
                swap_memory = psutil.swap_memory()
                swapMemoryTotal = swap_memory.total
                swapMemoryUsed = swap_memory.used
                swapMemoryFree = swap_memory.free
                swapMemoryPercentage = swap_memory.percent
                
                # Get CPU usage per core
                individual_cpu_usage = psutil.cpu_percent(percpu=True)
                
                # Virtual variables 
                virtual_memory = psutil.virtual_memory()
                virtualMemoryTotal = virtual_memory.total
                virtualMemoryAvailable = virtual_memory.available
                virtualMemoryPercentage = virtual_memory.percent
                virtualMemoryUsed = virtual_memory.used
                virtualMemoryFree = virtual_memory.free
                virtualMemoryActive = virtual_memory.active
                virtualMemoryBuffer = virtual_memory.buffers
                virtualMemoryCache = virtual_memory.cached
                virtualMemoryShared = virtual_memory.shared

                writer.writerow([timestamp, systemWideCPUUsage, swapMemoryTotal, swapMemoryUsed, swapMemoryFree, swapMemoryPercentage, individual_cpu_usage, virtualMemoryTotal, virtualMemoryAvailable, virtualMemoryPercentage, virtualMemoryUsed, virtualMemoryFree, virtualMemoryActive, virtualMemoryBuffer, virtualMemoryCache, virtualMemoryShared])
                
                time.sleep(interval)
                
print("Sampling complete...")
