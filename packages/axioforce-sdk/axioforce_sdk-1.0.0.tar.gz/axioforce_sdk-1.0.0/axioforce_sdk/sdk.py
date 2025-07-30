#!/usr/bin/env python3
"""
Axioforce Python SDK

A clean, object-oriented wrapper around the Axioforce C API that provides
easy-to-use Python interfaces for device management and data collection.

Example usage:
    from axioforce_sdk import AxioforceSDK, DeviceState
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    # Initialize with real devices
    sdk.initialize(log_level="info")
    
    # Or use simulator
    sdk.initialize_simulator(csv_file="data.csv", log_level="info")
    
    # Register callbacks
    def on_device_discovered(device):
        print(f"Found device: {device.name}")
    
    def on_data_received(event):
        print(f"Data from {event.device_name}: {event.forces}")
    
    sdk.on_device_discovered = on_device_discovered
    sdk.on_data_received = on_data_received
    
    # Start collecting data
    sdk.start_data_collection()
    
    # Stop when done
    sdk.stop()
"""

import ctypes
import ctypes.util
import os
import sys
import time
from enum import IntEnum
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass
import threading


class DeviceState(IntEnum):
    """Device state enumeration matching the C API."""
    CONNECTED = 0
    RUNNING = 1
    STOPPED = 2
    ERROR = 3


@dataclass
class DeviceInfo:
    """Device information structure."""
    id: str
    name: str
    type: str
    state: DeviceState
    
    @classmethod
    def from_c_struct(cls, device_c):
        """Create DeviceInfo from C structure."""
        return cls(
            id=device_c.id.decode('utf-8').rstrip('\x00'),
            name=device_c.name.decode('utf-8').rstrip('\x00'),
            type=device_c.type.decode('utf-8').rstrip('\x00'),
            state=DeviceState(device_c.state)
        )


@dataclass
class SensorData:
    """Sensor data structure."""
    forces: List[float]  # [Fx, Fy, Fz]
    moments: List[float]  # [Mx, My, Mz]
    cop: List[float]  # [CoPx, CoPy]
    sensor_id: int
    raw_values: List[float]  # [raw_x, raw_y, raw_z]
    name: str
    
    @classmethod
    def from_c_struct(cls, sensor_c):
        """Create SensorData from C structure."""
        return cls(
            forces=[sensor_c.forces[i] for i in range(3)],
            moments=[sensor_c.moments[i] for i in range(3)],
            cop=[sensor_c.cop[i] for i in range(2)],
            sensor_id=sensor_c.sensor_id,
            raw_values=[sensor_c.raw_values[i] for i in range(3)],
            name=sensor_c.name.decode('utf-8').rstrip('\x00')
        )


@dataclass
class SensorEvent:
    """Sensor event structure containing all data for a single event."""
    timestamp: float
    device_name: str
    raw_data: List[float]
    sensors: List[SensorData]
    model_output: List[List[float]]  # 2D array of model outputs
    
    @classmethod
    def from_c_struct(cls, event_c):
        """Create SensorEvent from C structure."""
        # Extract raw data
        raw_data = []
        if event_c.data and event_c.data_count > 0:
            raw_data = [event_c.data[i] for i in range(event_c.data_count)]
        
        # Extract sensor data
        sensors = []
        if event_c.sensors and event_c.sensors_count > 0:
            sensors = [SensorData.from_c_struct(event_c.sensors[i]) 
                      for i in range(event_c.sensors_count)]
        
        # Extract model output
        model_output = []
        if event_c.output and event_c.output_rows > 0:
            for i in range(event_c.output_rows):
                if event_c.output[i] and event_c.output_cols[i] > 0:
                    row = [event_c.output[i][j] for j in range(event_c.output_cols[i])]
                    model_output.append(row)
        
        return cls(
            timestamp=event_c.timestamp,
            device_name=event_c.name.decode('utf-8').rstrip('\x00'),
            raw_data=raw_data,
            sensors=sensors,
            model_output=model_output
        )


class AxioforceSDK:
    """
    Main SDK class that provides a clean interface to the Axioforce C API.
    
    This class handles all the low-level C API interactions and provides
    high-level Python methods for device management and data collection.
    """
    
    def __init__(self):
        """Initialize the SDK (does not connect to devices yet)."""
        self._lib = None
        self._initialized = False
        self._data_collection_active = False
        self._discovered_devices = []
        self._event_count = 0
        
        # Callback functions (can be set by user)
        self.on_device_discovered: Optional[Callable[[DeviceInfo], None]] = None
        self.on_data_received: Optional[Callable[[SensorEvent], None]] = None
        
        # Internal callback references (prevent garbage collection)
        self._device_callback_func = None
        self._data_callback_func = None
        
        # Load the C library
        self._load_library()
        self._setup_function_signatures()
    
    def _load_library(self):
        """Load the Axioforce C API library."""
        lib_names = [
            'axioforce_c_api.dll', 
            'libaxioforce_c_api.dylib',  # macOS shared library
        ]
        
        # Try package directory first (for installed package)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        search_paths = [
            package_dir,  # Package directory
            '.',          # Current directory
            '..',         # Parent directory
            '../release/bin',  # Release directory
        ]
        
        for path in search_paths:
            for lib_name in lib_names:
                lib_path = os.path.join(path, lib_name)
                if os.path.exists(lib_path):
                    try:
                        self._lib = ctypes.CDLL(lib_path)
                        return
                    except Exception as e:
                        print(f"Warning: Failed to load library from {lib_path}: {e}")
                        continue
        
        # If we get here, try to find the library in the current directory
        for lib_name in lib_names:
            if os.path.exists(lib_name):
                try:
                    self._lib = ctypes.CDLL(lib_name)
                    return
                except Exception as e:
                    print(f"Warning: Failed to load library {lib_name}: {e}")
        
        raise RuntimeError("Could not find or load Axioforce C API library. Please ensure the library file is available.")
    
    def _setup_function_signatures(self):
        """Setup C function signatures and return types."""
        lib = self._lib
        
        # Define C structures
        class DeviceInfoC(ctypes.Structure):
            _fields_ = [
                ("id", ctypes.c_char * 256),
                ("name", ctypes.c_char * 256),
                ("type", ctypes.c_char * 256),
                ("state", ctypes.c_int),
            ]

        class SensorDataC(ctypes.Structure):
            _fields_ = [
                ("forces", ctypes.c_double * 3),
                ("moments", ctypes.c_double * 3),
                ("cop", ctypes.c_double * 2),
                ("sensor_id", ctypes.c_int),
                ("raw_values", ctypes.c_float * 3),
                ("name", ctypes.c_char * 256),
            ]

        class SensorEventC(ctypes.Structure):
            _fields_ = [
                ("timestamp", ctypes.c_double),
                ("name", ctypes.c_char * 256),
                ("sensor_count", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_float)),
                ("data_count", ctypes.c_size_t),
                ("sensors", ctypes.POINTER(SensorDataC)),
                ("sensors_count", ctypes.c_size_t),
                ("output", ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("output_rows", ctypes.c_size_t),
                ("output_cols", ctypes.POINTER(ctypes.c_size_t)),
            ]
        
        # Store structures for use in callbacks
        self._DeviceInfoC = DeviceInfoC
        self._SensorEventC = SensorEventC
        
        # Define callback types
        DeviceCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(DeviceInfoC), ctypes.c_size_t, ctypes.c_void_p)
        DataCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(SensorEventC), ctypes.c_size_t, ctypes.c_void_p)
        
        # Setup function signatures
        lib.axf_api_initialize.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.axf_api_initialize.restype = ctypes.c_bool

        lib.axf_api_cleanup.argtypes = []
        lib.axf_api_cleanup.restype = None

        lib.axf_api_shutdown.argtypes = []
        lib.axf_api_shutdown.restype = None

        lib.axf_api_is_shutdown_requested.argtypes = []
        lib.axf_api_is_shutdown_requested.restype = ctypes.c_bool

        lib.axf_api_register_device_callback.argtypes = [DeviceCallback, ctypes.c_void_p]
        lib.axf_api_register_device_callback.restype = None

        lib.axf_api_register_data_listener.argtypes = [DataCallback, ctypes.c_void_p]
        lib.axf_api_register_data_listener.restype = ctypes.c_size_t

        lib.axf_api_connect_simulator_device.argtypes = [ctypes.c_char_p]
        lib.axf_api_connect_simulator_device.restype = ctypes.c_bool

        lib.axf_api_get_environment.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
        lib.axf_api_get_environment.restype = ctypes.c_bool

        lib.axf_api_start_device.argtypes = [ctypes.c_char_p]
        lib.axf_api_start_device.restype = ctypes.c_bool

        lib.axf_api_stop_device.argtypes = [ctypes.c_char_p]
        lib.axf_api_stop_device.restype = ctypes.c_bool

        lib.axf_api_get_available_devices.argtypes = [ctypes.POINTER(ctypes.POINTER(DeviceInfoC)), ctypes.POINTER(ctypes.c_size_t)]
        lib.axf_api_get_available_devices.restype = ctypes.c_bool

        lib.axf_api_recover_device.argtypes = [ctypes.c_char_p]
        lib.axf_api_recover_device.restype = ctypes.c_bool

        lib.axf_api_free_device_info_array.argtypes = [ctypes.POINTER(DeviceInfoC), ctypes.c_size_t]
        lib.axf_api_free_device_info_array.restype = None

        lib.axf_api_set_global_model.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.axf_api_set_global_model.restype = ctypes.c_bool
    
    def _device_discovery_callback(self, devices_ptr, device_count, user_data):
        """Internal device discovery callback."""
        self._discovered_devices.clear()
        
        for i in range(device_count):
            device_c = devices_ptr[i]
            device_info = DeviceInfo.from_c_struct(device_c)
            self._discovered_devices.append(device_info)
            
            # Auto-start devices that are discovered in CONNECTED state
            if device_info.state == DeviceState.CONNECTED:
                self._lib.axf_api_start_device(device_info.name.encode('utf-8'))
            
            # Call user callback if set
            if self.on_device_discovered:
                self.on_device_discovered(device_info)
    
    def _data_event_callback(self, events_ptr, event_count, user_data):
        """Internal data event callback."""
        self._event_count += event_count
        
        for i in range(event_count):
            event_c = events_ptr[i]
            event = SensorEvent.from_c_struct(event_c)
            
            # Call user callback if set
            if self.on_data_received:
                self.on_data_received(event)
    
    def initialize(self, log_level: str = "info") -> bool:
        """
        Initialize the SDK for real hardware devices.
        
        Args:
            log_level: Logging level ("debug", "info", "warning", "error")
            
        Returns:
            True if initialization successful, False otherwise
        """
        if self._initialized:
            return True
        
        # Initialize the API
        if not self._lib.axf_api_initialize(b"testing", log_level.encode('utf-8')):
            return False
        
        # Register callbacks
        self._device_callback_func = ctypes.CFUNCTYPE(
            None, ctypes.POINTER(self._DeviceInfoC), ctypes.c_size_t, ctypes.c_void_p
        )(self._device_discovery_callback)
        
        self._data_callback_func = ctypes.CFUNCTYPE(
            None, ctypes.POINTER(self._SensorEventC), ctypes.c_size_t, ctypes.c_void_p
        )(self._data_event_callback)
        
        self._lib.axf_api_register_device_callback(self._device_callback_func, None)
        self._lib.axf_api_register_data_listener(self._data_callback_func, None)
        
        self._initialized = True
        return True
    
    def initialize_simulator(self, csv_file: Optional[str] = None, log_level: str = "info") -> bool:
        """
        Initialize the SDK for simulator mode.
        
        Args:
            csv_file: Optional path to CSV file for simulation data
            log_level: Logging level ("debug", "info", "warning", "error")
            
        Returns:
            True if initialization successful, False otherwise
        """
        if not self.initialize(log_level):
            return False
        
        # Connect simulator device
        csv_param = csv_file.encode('utf-8') if csv_file else None
        if not self._lib.axf_api_connect_simulator_device(csv_param):
            return False
        
        return True
    
    def get_environment(self) -> Optional[str]:
        """Get environment information."""
        if not self._initialized:
            return None
        
        env_buffer = ctypes.create_string_buffer(256)
        if self._lib.axf_api_get_environment(env_buffer, 256):
            return env_buffer.value.decode('utf-8').rstrip('\x00')
        return None
    
    def get_discovered_devices(self) -> List[DeviceInfo]:
        """Get list of discovered devices."""
        return self._discovered_devices.copy()
    
    def start_device(self, device_name: str) -> bool:
        """Start a specific device by name."""
        if not self._initialized:
            return False
        return self._lib.axf_api_start_device(device_name.encode('utf-8'))
    
    def stop_device(self, device_name: str) -> bool:
        """Stop a specific device by name."""
        if not self._initialized:
            return False
        return self._lib.axf_api_stop_device(device_name.encode('utf-8'))
    
    def recover_device(self, device_name: str) -> bool:
        """Recover a device that's in error state."""
        if not self._initialized:
            return False
        return self._lib.axf_api_recover_device(device_name.encode('utf-8'))
    
    def set_global_model(self, model_path: str, model_type: str) -> bool:
        """Set global model for processing."""
        if not self._initialized:
            return False
        return self._lib.axf_api_set_global_model(
            model_path.encode('utf-8'), 
            model_type.encode('utf-8')
        )
    
    def start_data_collection(self, timeout: float = 15.0) -> bool:
        """
        Start data collection and wait for devices to be discovered.
        
        Args:
            timeout: Maximum time to wait for device discovery (seconds)
            
        Returns:
            True if devices discovered and started, False otherwise
        """
        if not self._initialized:
            return False
        
        # Wait for device discovery
        start_time = time.time()
        while not self._discovered_devices and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if not self._discovered_devices:
            return False
        
        self._data_collection_active = True
        return True
    
    def stop_data_collection(self):
        """Stop data collection."""
        self._data_collection_active = False
    
    def get_event_count(self) -> int:
        """Get total number of events received."""
        return self._event_count
    
    def is_data_collection_active(self) -> bool:
        """Check if data collection is currently active."""
        return self._data_collection_active
    
    def wait_for_events(self, timeout: Optional[float] = None, event_count: Optional[int] = None):
        """
        Wait for data events with optional timeout and event count.
        
        Args:
            timeout: Maximum time to wait (seconds), None for infinite
            event_count: Number of events to wait for, None for any events
        """
        if not self._initialized:
            return
        
        start_time = time.time()
        initial_count = self._event_count
        
        while self._data_collection_active:
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                break
            
            # Check event count
            if event_count and (self._event_count - initial_count) >= event_count:
                break
            
            time.sleep(0.01)  # Small sleep to prevent busy waiting
    
    def shutdown(self):
        """Shutdown the SDK and cleanup resources."""
        if not self._initialized:
            return
        
        # Stop data collection
        self.stop_data_collection()
        
        # Call shutdown
        if not self._lib.axf_api_is_shutdown_requested():
            self._lib.axf_api_shutdown()
            time.sleep(0.2)
        
        # Cleanup
        self._lib.axf_api_cleanup()
        self._initialized = False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()


# Convenience functions for common use cases
def create_csv_collector(output_file: str, include_header: bool = True):
    """
    Create a CSV data collector callback function.
    
    Args:
        output_file: Path to output CSV file
        include_header: Whether to include CSV header
        
    Returns:
        Callback function that can be assigned to sdk.on_data_received
    """
    header_printed = False
    
    def csv_collector(event: SensorEvent):
        nonlocal header_printed
        
        with open(output_file, 'a', newline='') as f:
            if include_header and not header_printed:
                # Create header
                header_parts = ["timestamp", "device_name"]
                
                # Add raw data headers
                for i in range(24):  # Assuming 24 raw values
                    header_parts.append(f"raw_value_{i}")
                
                # Add sensor data headers (per sensor)
                for i in range(8):  # Assuming 8 sensors
                    header_parts.extend([f"Fx_{i}", f"Fy_{i}", f"Fz_{i}"])
                    header_parts.extend([f"Mx_{i}", f"My_{i}", f"Mz_{i}"])
                    header_parts.extend([f"CoPx_{i}", f"CoPy_{i}"])
                
                # Add global model output headers
                header_parts.extend([
                    "global_Fx", "global_Fy", "global_Fz",
                    "global_Mx", "global_My", "global_Mz"
                ])
                
                f.write(",".join(header_parts) + "\n")
                header_printed = True
            
            # Create data row
            csv_parts = [f"{event.timestamp:.6f}", event.device_name]
            
            # Add raw data
            if event.raw_data:
                csv_parts.extend([str(val) for val in event.raw_data])
            else:
                csv_parts.extend(["0.0"] * 24)
            
            # Add sensor data
            if event.sensors:
                for sensor in event.sensors:
                    csv_parts.extend([str(val) for val in sensor.forces])
                    csv_parts.extend([str(val) for val in sensor.moments])
                    csv_parts.extend([str(val) for val in sensor.cop])
            else:
                csv_parts.extend(["0.0"] * (8 * 8))  # 8 sensors * 8 values
            
            # Add model output
            if event.model_output:
                for row in event.model_output:
                    csv_parts.extend([str(val) for val in row])
            else:
                csv_parts.extend(["0.0"] * 6)  # 6 global values
            
            f.write(",".join(csv_parts) + "\n")
    
    return csv_collector


def create_console_printer(print_raw: bool = False, print_sensors: bool = True, print_model: bool = True):
    """
    Create a console printer callback function.
    
    Args:
        print_raw: Whether to print raw data
        print_sensors: Whether to print sensor data
        print_model: Whether to print model output
        
    Returns:
        Callback function that can be assigned to sdk.on_data_received
    """
    def console_printer(event: SensorEvent):
        print(f"[{event.timestamp:.3f}] Device: {event.device_name}")
        
        if print_raw and event.raw_data:
            print(f"  Raw data: {event.raw_data[:6]}...")  # Show first 6 values
        
        if print_sensors and event.sensors:
            for i, sensor in enumerate(event.sensors):
                print(f"  Sensor {i}: F=({sensor.forces[0]:.2f}, {sensor.forces[1]:.2f}, {sensor.forces[2]:.2f}) "
                      f"M=({sensor.moments[0]:.2f}, {sensor.moments[1]:.2f}, {sensor.moments[2]:.2f})")
        
        if print_model and event.model_output:
            for i, row in enumerate(event.model_output):
                print(f"  Model output {i}: {row}")
    
    return console_printer 