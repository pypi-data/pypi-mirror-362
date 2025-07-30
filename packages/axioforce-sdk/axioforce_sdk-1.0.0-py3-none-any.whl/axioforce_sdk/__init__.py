"""
Axioforce Python SDK

A clean, object-oriented Python wrapper around the Axioforce C API that provides
easy-to-use interfaces for device management and data collection.

Example usage:
    from axioforce_sdk import AxioforceSDK
    
    with AxioforceSDK() as sdk:
        sdk.initialize_simulator(log_level="info")
        sdk.on_data_received = your_data_handler
        sdk.start_data_collection()
"""

from .sdk import (
    AxioforceSDK,
    DeviceState,
    DeviceInfo,
    SensorData,
    SensorEvent,
    create_csv_collector,
    create_console_printer,
)

__version__ = "1.0.0"
__author__ = "Axioforce Team"
__email__ = "support@axioforce.com"

__all__ = [
    "AxioforceSDK",
    "DeviceState", 
    "DeviceInfo",
    "SensorData",
    "SensorEvent",
    "create_csv_collector",
    "create_console_printer",
] 