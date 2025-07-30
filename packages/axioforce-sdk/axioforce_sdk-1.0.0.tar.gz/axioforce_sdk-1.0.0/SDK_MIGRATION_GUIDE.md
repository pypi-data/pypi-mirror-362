# Axioforce SDK Migration Guide

This guide shows how to migrate from the original `capi_device.py` approach to the new `axioforce_sdk.py` approach.

## Overview

The new SDK provides a clean, object-oriented interface that encapsulates all the complexity of the C API, making it much easier to use in Python applications.

## Key Improvements

### 1. **Simplified Setup**
**Old Way (capi_device.py):**
```python
import ctypes
import ctypes.util
import os
import sys
import time
from enum import IntEnum

# Complex C structure definitions
class DeviceInfoC(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_char * 256),
        ("name", ctypes.c_char * 256),
        ("type", ctypes.c_char * 256),
        ("state", ctypes.c_int),
    ]

# Manual library loading
def load_library():
    lib_names = ['axioforce_c_api.dll', 'libaxioforce_c_api.dylib']
    # ... complex library loading logic ...

# Manual function signature setup
lib.axf_api_initialize.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.axf_api_initialize.restype = ctypes.c_bool
# ... many more function signatures ...
```

**New Way (SDK):**
```python
from axioforce_sdk import AxioforceSDK

sdk = AxioforceSDK()
sdk.initialize_simulator(log_level="info")
```

### 2. **Clean Data Structures**
**Old Way:**
```python
# Manual C structure handling
device = devices_ptr[i]
device_info = {
    'id': device.id.decode('utf-8').rstrip('\x00'),
    'name': device.name.decode('utf-8').rstrip('\x00'),
    'type': device.type.decode('utf-8').rstrip('\x00'),
    'state': device.state
}
```

**New Way:**
```python
# Clean dataclass structures
@dataclass
class DeviceInfo:
    id: str
    name: str
    type: str
    state: DeviceState

# Automatic conversion from C structures
device_info = DeviceInfo.from_c_struct(device_c)
```

### 3. **Simplified Callbacks**
**Old Way:**
```python
# Global variables to prevent garbage collection
device_callback_func = None
data_callback_func = None

def device_discovery_callback(devices_ptr, device_count, user_data):
    # Manual C structure handling
    for i in range(device_count):
        device = devices_ptr[i]
        # ... complex processing ...

# Manual callback registration
device_callback_func = DeviceCallback(device_discovery_callback)
lib.axf_api_register_device_callback(device_callback_func, None)
```

**New Way:**
```python
# Simple callback assignment
def on_device_discovered(device):
    print(f"Found device: {device.name}")

def on_data_received(event):
    print(f"Data: {event.sensors}")

sdk.on_device_discovered = on_device_discovered
sdk.on_data_received = on_data_received
```

### 4. **Automatic Resource Management**
**Old Way:**
```python
try:
    # ... setup code ...
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Initiating graceful shutdown...")
    lib.axf_api_shutdown()
    time.sleep(0.2)
finally:
    lib.axf_api_cleanup()
```

**New Way:**
```python
# Context manager for automatic cleanup
with AxioforceSDK() as sdk:
    sdk.initialize_simulator(log_level="info")
    sdk.start_data_collection()
    # SDK automatically cleaned up when exiting context
```

## Migration Examples

### Example 1: Basic CSV Output

**Old Way (capi_device.py):**
```python
#!/usr/bin/env python3
"""
Enhanced CSV output for the Axioforce C API wrapper using the new device control paradigm.
"""

import ctypes
import ctypes.util
import os
import sys
import time
from enum import IntEnum

# ... 400+ lines of C API setup code ...

def data_event_callback(events_ptr, event_count, user_data):
    """Called when sensor data is received - outputs comprehensive CSV format."""
    global output_device_count
    
    # Print header once
    if not hasattr(data_event_callback, 'header_printed'):
        header_parts = ["timestamp", "device_name"]
        # ... complex header generation ...
        print(",".join(header_parts))
        data_event_callback.header_printed = True
        
    output_device_count += event_count
    
    for i in range(event_count):
        event = events_ptr[i]
        # ... complex CSV line generation ...
        csv_line = ",".join(csv_parts)
        print(csv_line)

def main():
    """Main function using the new device control paradigm."""
    global device_callback_func, data_callback_func, output_device_count
    
    # Parse command line arguments
    use_simulator, csv_file_path, log_level = parse_args()
    
    # ... complex initialization code ...
    
    try:
        # Initialize the API
        if not lib.axf_api_initialize(b"testing", log_level.encode('utf-8')):
            print("✗ Failed to initialize API")
            return 1
        
        # Register callbacks
        device_callback_func = DeviceCallback(device_discovery_callback)
        data_callback_func = DataCallback(data_event_callback)
        
        lib.axf_api_register_device_callback(device_callback_func, None)
        data_handle = lib.axf_api_register_data_listener(data_callback_func, None)
        
        # ... more complex setup ...
        
    except KeyboardInterrupt:
        # ... complex cleanup ...
    finally:
        # ... complex cleanup ...
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**New Way (SDK):**
```python
#!/usr/bin/env python3
"""
Simple CSV output using the Axioforce Python SDK.
"""

import sys
import os
import time
import argparse

from axioforce_sdk import AxioforceSDK, create_csv_collector

def main():
    parser = argparse.ArgumentParser(description="Axioforce SDK CSV Output")
    parser.add_argument("--output", "-o", default="sensor_output.csv")
    parser.add_argument("--duration", "-d", type=float, default=5.0)
    
    args = parser.parse_args()
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize simulator
        sdk.initialize_simulator(log_level="info")
        
        # Create CSV collector
        csv_collector = create_csv_collector(args.output, include_header=True)
        sdk.on_data_received = csv_collector
        
        # Start data collection
        if sdk.start_data_collection(timeout=10.0):
            time.sleep(args.duration)
            print(f"Collected {sdk.get_event_count()} events")
    
    finally:
        sdk.shutdown()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Example 2: Custom Data Processing

**Old Way:**
```python
def data_event_callback(events_ptr, event_count, user_data):
    for i in range(event_count):
        event = events_ptr[i]
        
        # Manual C structure access
        if event.sensors and event.sensors_count > 0:
            for j in range(event.sensors_count):
                sensor = event.sensors[j]
                # Manual array access
                fx = sensor.forces[0]
                fy = sensor.forces[1]
                fz = sensor.forces[2]
                # ... process data ...
```

**New Way:**
```python
def on_data_received(event):
    for sensor in event.sensors:
        # Clean Python list access
        fx, fy, fz = sensor.forces
        mx, my, mz = sensor.moments
        copx, copy = sensor.cop
        # ... process data ...
```

## Feature Comparison

| Feature | Old Way (capi_device.py) | New Way (SDK) |
|---------|-------------------------|---------------|
| **Lines of Code** | 400+ lines | 50-100 lines |
| **Setup Complexity** | High (manual C API setup) | Low (simple initialization) |
| **Error Handling** | Manual try/catch blocks | Built-in error handling |
| **Resource Management** | Manual cleanup | Automatic with context manager |
| **Type Safety** | None (manual C structures) | Full type hints and dataclasses |
| **Data Access** | Manual C structure access | Clean Python object access |
| **Callback Management** | Global variables and manual registration | Simple property assignment |
| **Testing** | Difficult (complex setup) | Easy (simple SDK interface) |
| **Reusability** | Limited (monolithic script) | High (modular SDK) |

## Migration Steps

1. **Replace imports:**
   ```python
   # Old
   import ctypes
   import ctypes.util
   # ... other imports ...
   
   # New
   from axioforce_sdk import AxioforceSDK, DeviceState, create_csv_collector
   ```

2. **Replace initialization:**
   ```python
   # Old
   lib = load_library()
   lib.axf_api_initialize(b"testing", log_level.encode('utf-8'))
   
   # New
   sdk = AxioforceSDK()
   sdk.initialize_simulator(log_level="info")
   ```

3. **Replace callbacks:**
   ```python
   # Old
   device_callback_func = DeviceCallback(device_discovery_callback)
   lib.axf_api_register_device_callback(device_callback_func, None)
   
   # New
   sdk.on_device_discovered = your_device_callback
   sdk.on_data_received = your_data_callback
   ```

4. **Replace data processing:**
   ```python
   # Old
   device = devices_ptr[i]
   device_name = device.name.decode('utf-8').rstrip('\x00')
   
   # New
   device_name = device.name
   ```

5. **Replace cleanup:**
   ```python
   # Old
   lib.axf_api_shutdown()
   lib.axf_api_cleanup()
   
   # New
   sdk.shutdown()
   # Or use context manager: with AxioforceSDK() as sdk:
   ```

## Benefits of Migration

1. **Reduced Code Complexity**: From 400+ lines to 50-100 lines
2. **Better Error Handling**: Built-in error handling and graceful degradation
3. **Type Safety**: Full type hints and dataclass structures
4. **Easier Testing**: Simple SDK interface makes testing straightforward
5. **Better Maintainability**: Clean, object-oriented design
6. **Reusability**: SDK can be easily integrated into other Python applications
7. **Documentation**: Comprehensive docstrings and type hints
8. **Convenience Functions**: Pre-built callbacks for common use cases

## Testing the Migration

After migrating, test your application:

```bash
# Test basic functionality
python simple_sdk_test.py

# Test CSV output
python sdk_csv_example.py --duration 5 --output test.csv

# Run all examples
python sdk_example.py --example all
```

## Support

If you encounter issues during migration:

1. Check the SDK documentation in `README_SDK.md`
2. Review the examples in `sdk_example.py`
3. Run the test suite with `test_sdk.py`
4. Ensure the C API library is available in the correct location 