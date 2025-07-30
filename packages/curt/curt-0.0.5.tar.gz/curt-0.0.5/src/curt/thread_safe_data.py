#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:47 p.m.
"""Thread Safe Data Collection

This file provides thread-safe data collection for high RPS load testing.
It uses temporary files to prevent data loss due to race conditions.

This file requires the following imports: 'os', 'tempfile', 'json', 'uuid', 'time', 'pandas'.
"""

import os
import tempfile
import json
import uuid
import time
import pandas as pd
from pathlib import Path


class ThreadSafeDataCollector:
    """
    Thread-safe data collector that uses temporary files to prevent data loss.
    Each request gets its own temporary file, eliminating race conditions.
    """
    
    def __init__(self, temp_dir=None):
        """
        Initialize the data collector.
        
        Parameters
        ----------
        temp_dir : str, optional
            Directory for temporary files. If None, uses system temp directory.
        """
        if temp_dir is None:
            # Try multiple fallback locations for temp directory
            temp_locations = [
                None,  # System default temp
                './curt_temp',  # Local directory
                os.path.expanduser('~/curt_temp'),  # User home
                os.path.join(os.getcwd(), 'curt_temp')  # Current working directory
            ]
            
            for location in temp_locations:
                try:
                    if location is None:
                        self.temp_dir = tempfile.mkdtemp(prefix='curt_data_')
                    else:
                        self.temp_dir = location
                        os.makedirs(self.temp_dir, exist_ok=True)
                    
                    # Test if we can actually write to this directory
                    test_file = os.path.join(self.temp_dir, 'test_write.tmp')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    
                    print(f"ThreadSafeDataCollector initialized with temp directory: {self.temp_dir}")
                    break
                    
                except (OSError, PermissionError, IOError) as e:
                    print(f"Failed to use temp location {location}: {e}")
                    continue
            else:
                # If all locations failed
                raise RuntimeError(
                    "CRITICAL ERROR: Cannot create or write to any temporary directory. "
                    "This is likely a permissions issue. Tried locations:\n"
                    f"  - System temp directory\n"
                    f"  - ./curt_temp\n"
                    f"  - ~/curt_temp\n"
                    f"  - {os.path.join(os.getcwd(), 'curt_temp')}\n"
                    "Please check file permissions or specify a custom temp_dir."
                )
        else:
            self.temp_dir = temp_dir
            try:
                os.makedirs(self.temp_dir, exist_ok=True)
                # Test write permissions
                test_file = os.path.join(self.temp_dir, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print(f"ThreadSafeDataCollector initialized with custom temp directory: {self.temp_dir}")
            except (OSError, PermissionError, IOError) as e:
                raise RuntimeError(
                    f"CRITICAL ERROR: Cannot write to specified temp directory '{temp_dir}': {e}\n"
                    "This is a permissions issue. Please check directory permissions."
                )
        
        self.temp_files = []
    
    def add_request_data(self, request_dict):
        """
        Add request data to a temporary file (thread-safe).
        
        Parameters
        ----------
        request_dict : dict
            Dictionary containing request data (start, end, method, response, etc.)
            
        Returns
        -------
        str
            Path to the temporary file created
        """
        # Create unique filename using timestamp + UUID to ensure uniqueness
        timestamp = time.time()
        unique_id = str(uuid.uuid4())
        filename = f"request_{timestamp}_{unique_id}.json"
        filepath = os.path.join(self.temp_dir, filename)
        
        try:
            # Write data to temporary file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(request_dict, f, ensure_ascii=False, default=str)
            
            self.temp_files.append(filepath)
            return filepath
            
        except Exception as e:
            print(f"Error writing temporary file {filepath}: {e}")
            return None
    
    def collect_all_data(self):
        """
        Collect all data from temporary files and create a DataFrame.
        
        Returns
        -------
        pandas.DataFrame
            DataFrame containing all collected request data
        """
        all_data = []
        
        for filepath in self.temp_files:
            try:
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data.append(data)
            except Exception as e:
                print(f"Error reading temporary file {filepath}: {e}")
        
        if all_data:
            return pd.DataFrame(all_data)
        else:
            return pd.DataFrame()
    
    def cleanup(self):
        """
        Remove all temporary files and clean up the temporary directory.
        """
        for filepath in self.temp_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Error removing temporary file {filepath}: {e}")
        
        try:
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Error removing temporary directory {self.temp_dir}: {e}")
        
        self.temp_files.clear()
        print(f"Cleanup completed for {self.temp_dir}")


# Global instance for easy access
_data_collector = None


def initialize_data_collector(temp_dir=None):
    """
    Initialize the global data collector.
    
    Parameters
    ----------
    temp_dir : str, optional
        Directory for temporary files
    """
    global _data_collector
    _data_collector = ThreadSafeDataCollector(temp_dir)


def add_request_data(request_dict):
    """
    Add request data using the global collector.
    
    Parameters
    ----------
    request_dict : dict
        Request data dictionary
    """
    global _data_collector
    if _data_collector is None:
        initialize_data_collector()
    
    return _data_collector.add_request_data(request_dict)


def get_all_data():
    """
    Get all collected data as a DataFrame.
    
    Returns
    -------
    pandas.DataFrame
        All collected request data
    """
    global _data_collector
    if _data_collector is None:
        return pd.DataFrame()
    
    return _data_collector.collect_all_data()


def cleanup_data_collector():
    """
    Clean up the global data collector.
    """
    global _data_collector
    if _data_collector is not None:
        _data_collector.cleanup()
        _data_collector = None 