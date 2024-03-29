# psutil() module notes

Documentation found here: [psutil Documentation](https://psutil.readthedocs.io/en/latest/)

## Platform-specific fields
- ```user```: 
  - Time spent by normal processes executing in user mode; on Linux this also includes guest time
- ```system```: 
  - Time spent by processes executing in kernel mode
- ```idle```: 
  - Time spent doing nothing
- ```nice``` (UNIX)
  - Time spent by niced (prioritized) processes executing in user mode; on Linux this also includes guest_nice time
- ```iowait``` (Linux)
  - Time spent waiting for I/O to complete. This is not accounted in idle time counter.
- ```irq``` (Linux, BSD): 
  - Time spent for servicing hardware interrupts
- ```softirq``` (Linux): 
  - Time spent for servicing software interrupts
- ```steal``` (Linux 2.6.11+): 
  - Time spent by other operating systems running in a virtualized environment
- ```guest``` (Linux 2.6.24+): 
  - Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel
- ```guest_nice``` (Linux 3.2.0+): 
  - Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel)
- ```interrupt``` (Windows): 
  - Time spent for servicing hardware interrupts ( similar to “irq” on UNIX)
- ```dpc``` (Windows): 
  - Time spent servicing deferred procedure calls (DPCs); DPCs are interrupts that run at a lower priority than standard interrupts.

## psutil.cpu_percent(interval=None, percpu=False)

- Returns float.
- Represents SYSTEM-WIDE CPU usage as a percentage.
- When `interval > 0.0`:
  - Compares system CPU time elapsed before/after the interval (blocking).
- When `interval` is either `0.0` or `None`:
  - Compares CPU time since:
    - Last call.
    - Module import.
  - Returns immediately:
    - First time it's called will return meaningless `0.0` that you can ignore.
    - In this case, recommendation for accuracy is for the function to be called at least `0.1` seconds between calls.
  - If ```interval``` is set to ```NONE```
    - Non-blocking
    - If ```interval``` is set to a ```positive``` value
      - It's now a blocking function
- `percpu`:
  - When `True`:
    - Returns list of floats representing CPU usage for each CPU element.
  - Internally the function maintains a global map/dictionary where the key is the ID of the calling thread.

## memory_full_info()

- Returns same info as `memory_info()`.
- Also provides additional metrics:
  - USS.
  - PSS.
  - swap.
- These metrics provide better representation of 'effective' process memory consumption.
- Does so by passing through the whole process address.
  - Needs higher user privileges than `memory_info()`.
- Considerably slower.

## psutil.getloadavg()

- Returns average system load in the last `1`, `5`, `15` mins as a tuple.
- The "load" represents the processes that are in a:
  - Running state.
  - Either using/waiting to use the CPU.

## psutil.swap_memory()

- Return system swap memory statistics as a named tuple including the following fields:
  - `total`: total swap memory in bytes.
  - `used`: used swap memory in bytes.
  - `free`: free swap memory in bytes.
  - `percent`: the percentage usage calculated as `(total - available) / total * 100`.
  - `sin`: the number of bytes the system has swapped in from disk (cumulative).
  - `sout`: the number of bytes the system has swapped out from disk (cumulative).
  - `sin` and `sout` on Windows are always set to `0`.

## psutil.virtual_memory()

- Return statistics about system memory usage as a named tuple including the following fields, expressed in bytes.
- Main metrics:
  - `total`: total physical memory (exclusive swap).
  - `available`: the memory that can be given instantly to processes without the system going into swap. This is calculated by summing different memory metrics that vary depending on the platform. It is supposed to be used to monitor actual memory usage in a cross-platform fashion.
  - `percent`: the percentage usage calculated as `(total - available) / total * 100`.
- Other metrics:
  - `used`: memory used, calculated differently depending on the platform and designed for informational purposes only. `total - free` does not necessarily match `used`.
  - `free`: memory not being used at all (zeroed) that is readily available;
    - note that this doesn’t reflect the actual memory available (use `available` instead).
    - `total - used` does not necessarily match `free`.
  - `active` (UNIX): memory currently in use or very recently used, and so it is in RAM.
  - `inactive` (UNIX): memory that is marked as not used.
  - `buffers` (Linux, BSD): cache for things like file system metadata.
  - `cached` (Linux, BSD): cache for various things.
  - `shared` (Linux, BSD): memory that may be simultaneously accessed by multiple processes.
  - `slab` (Linux): in-kernel data structures cache.
  - `wired` (BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk.
  
The sum of `used` and `available` does not necessarily equal `total`. On Windows `available` and `free` are the same.
