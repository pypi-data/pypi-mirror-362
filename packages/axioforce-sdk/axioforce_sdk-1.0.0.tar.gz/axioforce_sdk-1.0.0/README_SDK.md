# Axioforce Python SDK

A clean, object-oriented Python wrapper around the Axioforce C API that provides easy-to-use interfaces for device management and data collection.

## Features

- **Simple API**: Clean, Pythonic interface that hides the complexity of the C API
- **Device Management**: Easy device discovery, connection, and control
- **Data Collection**: Flexible data collection with customizable callbacks
- **Simulator Support**: Built-in simulator mode for testing and development
- **Context Manager**: Automatic resource cleanup with `with` statements
- **Type Safety**: Full type hints and dataclass structures
- **Convenience Functions**: Pre-built callbacks for common use cases

## Quick Start

### Basic Usage

```python
from axioforce_sdk import AxioforceSDK

# Create SDK instance
sdk = AxioforceSDK()

# Initialize for real devices
sdk.initialize(log_level="info")

# Or use simulator
sdk.initialize_simulator(csv_file="data.csv", log_level="info")

# Define callbacks
def on_device_discovered(device):
    print(f"Found device: {device.name}")

def on_data_received(event):
    print(f"Data from {event.device_name}: {event.sensors}")

sdk.on_device_discovered = on_device_discovered
sdk.on_data_received = on_data_received

# Start collecting data
sdk.start_data_collection()

# Stop when done
sdk.shutdown()
```

### Using Context Manager

```python
from axioforce_sdk import AxioforceSDK

# Automatic cleanup with context manager
with AxioforceSDK() as sdk:
    sdk.initialize_simulator(log_level="info")
    
    def data_handler(event):
        print(f"Received data: {event.timestamp}")
    
    sdk.on_data_received = data_handler
    sdk.start_data_collection()
    
    # SDK automatically cleaned up when exiting context
```

## Installation

1. Ensure the Axioforce C API library is available in your system:
   - `axioforce_c_api.dll` (Windows)
   - `libaxioforce_c_api.dylib` (macOS)

2. Place the `axioforce_sdk.py` file in your project directory or Python path.

3. Import and use the SDK:
   ```python
   from axioforce_sdk import AxioforceSDK
   ```

## API Reference

### Main Classes

#### `AxioforceSDK`

The main SDK class that provides all functionality.

**Methods:**

- `initialize(log_level="info") -> bool`: Initialize for real hardware devices
- `initialize_simulator(csv_file=None, log_level="info") -> bool`: Initialize for simulator mode
- `start_data_collection(timeout=15.0) -> bool`: Start data collection
- `stop_data_collection()`: Stop data collection
- `shutdown()`: Cleanup resources
- `get_discovered_devices() -> List[DeviceInfo]`: Get list of discovered devices
- `get_event_count() -> int`: Get total number of events received
- `is_data_collection_active() -> bool`: Check if data collection is active

**Properties:**

- `on_device_discovered`: Callback for device discovery events
- `on_data_received`: Callback for data events

#### `DeviceInfo`

Information about a discovered device.

**Fields:**
- `id: str`: Device identifier
- `name: str`: Device name
- `type: str`: Device type
- `state: DeviceState`: Current device state

#### `SensorEvent`

Complete sensor data for a single event.

**Fields:**
- `timestamp: float`: Event timestamp
- `device_name: str`: Name of the device
- `raw_data: List[float]`: Raw sensor values
- `sensors: List[SensorData]`: Processed sensor data
- `model_output: List[List[float]]`: Model output data

#### `SensorData`

Data from a single sensor.

**Fields:**
- `forces: List[float]`: [Fx, Fy, Fz] force values
- `moments: List[float]`: [Mx, My, Mz] moment values
- `cop: List[float]`: [CoPx, CoPy] center of pressure values
- `sensor_id: int`: Sensor identifier
- `raw_values: List[float]`: Raw sensor values
- `name: str`: Sensor name

#### `DeviceState`

Enumeration of device states.

**Values:**
- `CONNECTED`: Device is connected but not running
- `RUNNING`: Device is running and collecting data
- `STOPPED`: Device is stopped
- `ERROR`: Device is in error state

### Convenience Functions

#### `create_csv_collector(output_file, include_header=True)`

Create a callback function that saves data to a CSV file.

```python
from axioforce_sdk import create_csv_collector

csv_callback = create_csv_collector("output.csv", include_header=True)
sdk.on_data_received = csv_callback
```

#### `create_console_printer(print_raw=False, print_sensors=True, print_model=True)`

Create a callback function that prints data to console.

```python
from axioforce_sdk import create_console_printer

printer = create_console_printer(print_sensors=True, print_model=False)
sdk.on_data_received = printer
```

## Examples

### Example 1: Basic Data Collection

```python
from axioforce_sdk import AxioforceSDK

sdk = AxioforceSDK()

try:
    # Initialize simulator
    sdk.initialize_simulator(log_level="info")
    
    # Set up data handler
    def handle_data(event):
        if event.sensors:
            sensor = event.sensors[0]
            print(f"Force: {sensor.forces}, Moment: {sensor.moments}")
    
    sdk.on_data_received = handle_data
    
    # Start collection
    if sdk.start_data_collection(timeout=10.0):
        print("Collecting data...")
        time.sleep(5)  # Collect for 5 seconds
        print(f"Collected {sdk.get_event_count()} events")
    
finally:
    sdk.shutdown()
```

### Example 2: CSV Output

```python
from axioforce_sdk import AxioforceSDK, create_csv_collector

with AxioforceSDK() as sdk:
    sdk.initialize_simulator(log_level="info")
    
    # Create CSV collector
    csv_handler = create_csv_collector("sensor_data.csv")
    sdk.on_data_received = csv_handler
    
    # Collect data
    sdk.start_data_collection(timeout=10.0)
    time.sleep(3)
    
    print(f"Data saved to sensor_data.csv")
```

### Example 3: Device Control

```python
from axioforce_sdk import AxioforceSDK, DeviceState

sdk = AxioforceSDK()

try:
    sdk.initialize(log_level="info")
    
    # Wait for device discovery
    if sdk.start_data_collection(timeout=15.0):
        devices = sdk.get_discovered_devices()
        
        for device in devices:
            print(f"Device: {device.name} - State: {device.state.name}")
            
            # Stop and restart device
            if device.state == DeviceState.RUNNING:
                sdk.stop_device(device.name)
                time.sleep(1)
                sdk.start_device(device.name)
    
finally:
    sdk.shutdown()
```

### Example 4: Custom Data Processing

```python
from axioforce_sdk import AxioforceSDK

# Track statistics
stats = {'total_force': 0.0, 'event_count': 0}

def custom_processor(event):
    stats['event_count'] += 1
    
    if event.sensors:
        for sensor in event.sensors:
            # Calculate force magnitude
            force_mag = (sensor.forces[0]**2 + sensor.forces[1]**2 + sensor.forces[2]**2)**0.5
            stats['total_force'] += force_mag

with AxioforceSDK() as sdk:
    sdk.initialize_simulator(log_level="info")
    sdk.on_data_received = custom_processor
    
    sdk.start_data_collection(timeout=10.0)
    time.sleep(3)
    
    if stats['event_count'] > 0:
        avg_force = stats['total_force'] / stats['event_count']
        print(f"Average force: {avg_force:.2f}")
```

## Error Handling

The SDK provides clear error handling:

```python
try:
    sdk = AxioforceSDK()
    
    if not sdk.initialize(log_level="info"):
        print("Failed to initialize SDK")
        return
    
    if not sdk.start_data_collection(timeout=10.0):
        print("No devices discovered")
        return
    
    # ... use SDK ...
    
except RuntimeError as e:
    print(f"SDK error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    sdk.shutdown()
```


## Troubleshooting

### Common Issues

1. **Library not found**: Ensure `axioforce_c_api.dll` or `libaxioforce_c_api.dylib` is in the search path
2. **No devices discovered**: Check device connections and drivers
3. **Import errors**: Ensure `axioforce_sdk.py` is in your Python path

### Debug Mode

Enable debug logging for more detailed information:

```python
sdk.initialize(log_level="debug")
```

## License

This SDK is part of the Axioforce project and follows the same licensing terms. 