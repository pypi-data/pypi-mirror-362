
# Flag to track whether the header has been written
header_written = False


# Decorator to profile functions and log runtime and memory usage
def _profile_function(log_file='runtime_analysis.txt'):
    """
    Decorator to profile a function, recording memory usage and runtime.

    Args:
        log_file (str): The path to the log file where profiling results will be recorded.
    """
    from memory_profiler import memory_usage
    from time import time
    from functools import wraps
    import numpy as np
    from datetime import datetime


    def _decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            global header_written
            # Start the timer
            start_time = time()

            # Start memory profiling
            mem_usage = memory_usage((func, args, kwargs), interval=0.1)  # Check memory usage every 0.1 seconds

            # Execute the function
            result = func(*args, **kwargs)

            # Stop the timer
            end_time = time()
            execution_time = end_time - start_time

            # Calculate peak memory usage and average memory usage
            peak_memory = max(mem_usage)  # Peak memory usage during the function call
            avg_memory = np.mean(mem_usage)  # Average memory usage during the function call

            # Log the profiling results to the file
            with open(log_file, 'a') as log:
                # Write the header only once at the beginning of the run
                if not header_written:
                    log.write("\n\n\n")  # Add extra spaces before the header
                    log.write("=" * 40 + "\n")
                    log.write(f"Profiling Report\n")
                    log.write(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log.write("=" * 40 + "\n\n")
                    header_written = True

                # Add a smaller header between function calls
                log.write(f"\nFunction: {func.__name__} (Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
                log.write(f"Execution Time: {execution_time:.6f} seconds\n")
                log.write(f"Peak Memory Usage: {peak_memory:.6f} MiB\n")
                log.write(f"Average Memory Usage: {avg_memory:.6f} MiB\n")
                log.write("-" * 30 + "\n")

            return result

        return _wrapper
    return _decorator



