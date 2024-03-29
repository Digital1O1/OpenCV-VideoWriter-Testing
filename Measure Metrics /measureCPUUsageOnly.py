import psutil
import time
import csv

# Filename for CSV
file_name = "cpuMetrics.csv"

duration = 5
interval = 0.1

# Set end time for data collection
end_time = time.time() + duration
start_time = time.time()  # Store the start time


print(f"Sampling for : {duration:.2f} seconds")

print("Starting sampling now")

with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Timestamp",
            "CPU Usage System Wide (%)",
            "Individual CPU Usage Per Core(%)",
            "User CPU Usage (%)",
            "CPU Frequency Per CPU (%)",
        ]
    )

    while time.time() < end_time:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Gets SYSTEM WIDE CPU useage as a SINGULAR value
        systemWideCPUUsage = psutil.cpu_percent(interval=interval, percpu=False)

        # Get CPU usage per core
        # CPU1 CPU2 CPU3 CPU4
        individual_cpu_usage = psutil.cpu_percent(interval=interval, percpu=True)

        # Gets CPU usage and breaks it down to user/nice/system/etc...
        # utilizationUsageCPU = psutil.cpu_times_percent(interval=0.1, percpu=False)

        user_cpu_usage = individual_cpu_usage[
            0
        ]  # Assuming the first core represents overall user CPU usage

        cpuFrequencyPerCPU = psutil.cpu_freq(percpu=False)

        writer.writerow(
            [
                timestamp,
                systemWideCPUUsage,
                individual_cpu_usage,
                user_cpu_usage,
                cpuFrequencyPerCPU,
            ]
        )

        # print(
        #     f"Timestamp: {timestamp}, System Wide CPU Usage: {systemWideCPUUsage}%, Individual CPU Usage: {individual_cpu_usage}%, User_cpu_usage: {user_cpu_usage}%"
        # )

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        time.sleep(interval)
        print(f"Time elapsed: {elapsed_time:.2f} seconds")  # Print elapsed time

print("Sampling complete...")
