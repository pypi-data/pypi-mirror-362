#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:37 p.m.
"""Threads manager

This file allows the user to call functions n times per second with precise RPS control.

This file requires the following imports: 'time', 'threading'.

This file contains the following functions:
    * start_threads - starts threads for requested functions with precise RPS control
    * start_threads_precise - starts threads with precise RPS control for threshold testing
"""
import time
import threading
import math

from curt.repeated_timer import RepeatedTimer


def start_threads(time_length: 'int',
                  functions: 'list',
                  threads_number: 'int'):
    """
    Calls a function threads_number times per second during time_length seconds.
    
    .. deprecated:: 0.0.5
        This function is deprecated and will be removed in a future release.
        Use :func:`start_threads_precise` instead for accurate RPS control.
        This function has timing issues that prevent precise RPS delivery.
    
    Parameters
    ----------
    time_length : int
        Process length in seconds
    functions : list
        Functions names list
    threads_number : int
        Number of threads per second

    Returns
    -------
    None
    """
    import warnings
    warnings.warn(
        "start_threads() is deprecated and will be removed in a future release. "
        "Use start_threads_precise() instead for accurate RPS control.",
        DeprecationWarning,
        stacklevel=2
    )
    print('starting threads')
    threads = []
    for i in range(threads_number):
        for function in functions:
            threads.append(RepeatedTimer(1, function))
        time.sleep(1 / threads_number)
    try:
        time.sleep(time_length - 1)
    finally:
        for thread in threads:
            thread.stop()
    print('threads stopped')


def start_threads_precise(time_length: 'int',
                         functions: 'list',
                         rps: 'int',
                         calibration_factor: 'float' = 1.05):
    """
    Starts threads with precise RPS control for threshold testing.
    
    Parameters
    ----------
    time_length : int
        Test duration in seconds
    functions : list
        List of functions to execute
    rps : int
        Target requests per second (total across all functions)
    calibration_factor : float
        Compensation factor to achieve 100%+ accuracy (default: 1.05)
    
    Returns
    -------
    None
    """
    # Apply calibration factor for precise RPS control
    compensated_rps = int(rps * calibration_factor)
    
    print(f'Starting precise RPS test: {rps} RPS → {compensated_rps} RPS (factor: {calibration_factor:.2f})')
    print(f'Test duration: {time_length} seconds')
    print(f'Functions: {[f.__name__ for f in functions]}')
    
    def worker(worker_id):
        """Worker function that maintains precise RPS"""
        end_time = time.time() + time_length
        total_functions = len(functions)
        
        # Calculate precise timing
        # Each thread should execute all functions in sequence
        # Total requests per second = threads × functions_per_cycle × cycles_per_second
        # We want: rps = threads × total_functions × cycles_per_second
        # So: cycles_per_second = rps / (threads × total_functions)
        # And: sleep_time = 1 / cycles_per_second = (threads × total_functions) / rps
        
        optimal_threads = min(max(1, compensated_rps // 10), 20)  # 1 thread per 10 RPS, max 20 threads
        cycles_per_second = compensated_rps / (optimal_threads * total_functions)
        sleep_time = 1.0 / cycles_per_second if cycles_per_second > 0 else 1.0
        
        request_count = 0
        cycle_count = 0
        last_cycle_time = time.time()
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Execute all functions in this cycle
            for func in functions:
                if current_time >= end_time:
                    break
                try:
                    func()
                    request_count += 1
                except Exception as e:
                    print(f"Error in worker {worker_id}: {e}")
            
            cycle_count += 1
            
            # Calculate next cycle time
            next_cycle_time = last_cycle_time + sleep_time
            
            # Sleep until next cycle
            if next_cycle_time > current_time:
                time.sleep(next_cycle_time - current_time)
            
            last_cycle_time = next_cycle_time
        
        print(f"Worker {worker_id} completed {request_count} requests in {cycle_count} cycles")
    
    # Calculate optimal number of threads
    optimal_threads = min(max(1, compensated_rps // 10), 20)  # 1 thread per 10 RPS, max 20 threads
    
    print(f"Using {optimal_threads} threads for {compensated_rps} RPS")
    print(f"Functions per cycle: {len(functions)}")
    print(f"Expected cycles per second: {compensated_rps / (optimal_threads * len(functions)):.2f}")
    
    # Create and start threads
    threads = []
    for i in range(optimal_threads):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("All threads completed")


def start_threads_calibrated(time_length: 'int',
                           functions: 'list',
                           rps: 'int',
                           calibration_factors: 'dict' = None):
    """
    Starts threads with calibrated precise RPS control
    
    Parameters
    ----------
    time_length : int
        Test duration in seconds
    functions : list
        List of functions to execute
    rps : int
        Target requests per second (total across all functions)
    calibration_factors : dict, optional
        Calibration factors from calibration system
        
    Returns
    -------
    None
    """
    # Default calibration factor
    default_factor = 1.05
    
    # Get the appropriate factor
    if calibration_factors is None:
        factor = default_factor
    elif 'universal' in calibration_factors:
        factor = calibration_factors['universal']
    else:
        # Find closest RPS level
        available_rps = list(calibration_factors.keys())
        closest_rps = min(available_rps, key=lambda x: abs(x - rps))
        factor = calibration_factors[closest_rps]
    
    # Use the precise threading approach with the calculated factor
    start_threads_precise(time_length, functions, rps, factor)
