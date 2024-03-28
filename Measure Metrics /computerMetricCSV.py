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
    ----------------- [ psutil() module notes ] -----------------
    
    Documentation found here : https://psutil.readthedocs.io/en/latest/
    
    The following functions I thought were useful in the context of the videoWriting testing
    
    psutil.cpu_percent(interval=None, percpu=False)
        - Returns float 
        - Represents SYSTEM-WIDE CPU usage as a percentage 
        - When interval > 0.0
            - compares system CPU time elapsed before/after the interval (blocking)
        - When interval is either 0.0 or NONE
            - Compares CPU time since 
                - Last call
                - Module import 
            - Returns immediately
                - First time it's called will return meaningless 0.0 that you can ignore 
                - In this case, recommendation for accuracy is for the function to be called at least 0.1 seconds between calls
        - percpu
            - When True
                - returns list of floats representing CPU useage for each CPU element
            - Internally the function maintains a global map/dictionary where the key is the ID of the calling thread
            
    memory_full_info()
        - Returns same info as memory_info()
        - Also provides additional metrics
            - USS
            - PSS
            - swap
            - These metrics provide better representation of 'eccective' process memory consumption 
        - Does so by passing through the whole process address
            - Needs higher user privledges than memory_info()
        - Considerably slower
        
    psutil.getloadavg()
        - Returns average system load in the last 1,5,15 mins as a tuple
        - The "load" represents the processess that are in a 
            - Running state
            - Either using/waiting to use the CPU
            
            
    psutil.swap_memory()
        - Return system swap memory statistics as a named tuple including the following fields:
            - total: total swap memory in bytes
            - used: used swap memory in bytes
            - free: free swap memory in bytes
            - percent: the percentage usage calculated as (total - available) / total * 100
            - sin: the number of bytes the system has swapped in from disk (cumulative)
            - sout: the number of bytes the system has swapped out from disk (cumulative)

        sin and sout on Windows are always set to 0. See meminfo.py script providing an example on how to convert bytes in a human readable form.
        
        
    psutil.virtual_memory()
        - Return statistics about system memory usage as a named tuple including the following fields, expressed in bytes.

        Main metrics:

            - total: total physical memory (exclusive swap).
            - available: 
                - the memory that can be given instantly to processes without the system going into swap. This is calculated by summing different memory metrics that vary depending on the platform. It is supposed to be used to monitor actual memory usage in a cross platform fashion.
            - percent: 
                - the percentage usage calculated as (total - available) / total * 100.

        Other metrics:
            - used: 
                - memory used, calculated differently depending on the platform and designed for informational purposes only. total - free does not necessarily match used.
            - free: 
                - memory not being used at all (zeroed) that is readily available; 
                - note that this doesn’t reflect the actual memory available (use available instead). 
                - total - used does not necessarily match free.
            - active (UNIX): 
                - memory currently in use or very recently used, and so it is in RAM.
            - inactive (UNIX): 
                - memory that is marked as not used.
            - buffers (Linux, BSD): 
                - cache for things like file system metadata.
            - cached (Linux, BSD): 
                - cache for various things.
            - shared (Linux, BSD): 
                - memory that may be simultaneously accessed by multiple processes.
            - slab (Linux): 
                - in-kernel data structures cache.
            - wired (BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk.

    The sum of used and available does not necessarily equal total. 
    On Windows available and free are the same. 
    See meminfo.py script providing an example on how to convert bytes in a human readable form.

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
