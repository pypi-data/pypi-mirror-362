#!/usr/bin/env python3
"""
Example usage of the Axioforce Python SDK.

This script demonstrates various ways to use the SDK for different use cases.
"""

import sys
import time
import argparse
from axioforce_sdk import (
    AxioforceSDK, 
    DeviceState, 
    create_csv_collector, 
    create_console_printer
)


def example_basic_usage():
    """Basic usage example with real devices."""
    print("=== Basic Usage Example ===")
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize for real devices
        if not sdk.initialize(log_level="info"):
            print("Failed to initialize SDK")
            return
        
        print(f"Environment: {sdk.get_environment()}")
        
        # Define callbacks
        def on_device_discovered(device):
            print(f"Found device: {device.name} ({device.type}) - State: {device.state.name}")
        
        def on_data_received(event):
            print(f"Data from {event.device_name}: {len(event.sensors)} sensors")
            if event.sensors:
                sensor = event.sensors[0]
                print(f"  Forces: {sensor.forces}")
                print(f"  Moments: {sensor.moments}")
        
        sdk.on_device_discovered = on_device_discovered
        sdk.on_data_received = on_data_received
        
        # Start data collection
        if sdk.start_data_collection(timeout=10.0):
            print("Data collection started successfully")
            
            # Collect data for 5 seconds
            time.sleep(5)
            
            print(f"Collected {sdk.get_event_count()} events")
        else:
            print("Failed to start data collection")
    
    finally:
        sdk.shutdown()


def example_simulator_usage():
    """Example using simulator mode."""
    print("=== Simulator Usage Example ===")
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize simulator (you can specify a CSV file here)
        if not sdk.initialize_simulator(log_level="info"):
            print("Failed to initialize simulator")
            return
        
        print(f"Environment: {sdk.get_environment()}")
        
        # Use console printer for data output
        sdk.on_data_received = create_console_printer(
            print_raw=False, 
            print_sensors=True, 
            print_model=True
        )
        
        # Start data collection
        if sdk.start_data_collection(timeout=5.0):
            print("Simulator data collection started")
            
            # Collect data for 3 seconds
            time.sleep(3)
            
            print(f"Collected {sdk.get_event_count()} events")
        else:
            print("Failed to start simulator data collection")
    
    finally:
        sdk.shutdown()


def example_csv_output():
    """Example that outputs data to CSV file."""
    print("=== CSV Output Example ===")
    
    output_file = "sensor_data.csv"
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize simulator
        if not sdk.initialize_simulator(log_level="info"):
            print("Failed to initialize simulator")
            return
        
        # Create CSV collector
        csv_collector = create_csv_collector(output_file, include_header=True)
        sdk.on_data_received = csv_collector
        
        # Start data collection
        if sdk.start_data_collection(timeout=5.0):
            print(f"Collecting data to {output_file}...")
            
            # Collect data for 2 seconds
            time.sleep(2)
            
            print(f"Collected {sdk.get_event_count()} events")
            print(f"Data saved to {output_file}")
        else:
            print("Failed to start data collection")
    
    finally:
        sdk.shutdown()


def example_context_manager():
    """Example using context manager for automatic cleanup."""
    print("=== Context Manager Example ===")
    
    # Use context manager for automatic cleanup
    with AxioforceSDK() as sdk:
        # Initialize simulator
        if not sdk.initialize_simulator(log_level="info"):
            print("Failed to initialize simulator")
            return
        
        # Simple data printer
        def simple_printer(event):
            if event.sensors:
                sensor = event.sensors[0]
                print(f"[{event.timestamp:.3f}] Fx={sensor.forces[0]:.2f}, Fy={sensor.forces[1]:.2f}, Fz={sensor.forces[2]:.2f}")
        
        sdk.on_data_received = simple_printer
        
        # Start collection
        if sdk.start_data_collection(timeout=5.0):
            print("Collecting data...")
            time.sleep(2)
            print(f"Collected {sdk.get_event_count()} events")
    
    # SDK is automatically cleaned up here


def example_device_control():
    """Example showing device control operations."""
    print("=== Device Control Example ===")
    
    sdk = AxioforceSDK()
    
    try:
        # Initialize for real devices
        if not sdk.initialize(log_level="info"):
            print("Failed to initialize SDK")
            return
        
        # Wait for device discovery
        if sdk.start_data_collection(timeout=10.0):
            devices = sdk.get_discovered_devices()
            print(f"Discovered {len(devices)} devices:")
            
            for device in devices:
                print(f"  - {device.name} ({device.type}) - {device.state.name}")
                
                # Example: Stop and restart a device
                if device.state == DeviceState.RUNNING:
                    print(f"    Stopping {device.name}...")
                    if sdk.stop_device(device.name):
                        print(f"    ✓ {device.name} stopped")
                        
                        time.sleep(1)
                        
                        print(f"    Starting {device.name}...")
                        if sdk.start_device(device.name):
                            print(f"    ✓ {device.name} started")
                        else:
                            print(f"    ✗ Failed to start {device.name}")
                    else:
                        print(f"    ✗ Failed to stop {device.name}")
            
            # Collect some data
            time.sleep(3)
            print(f"Collected {sdk.get_event_count()} events")
        else:
            print("No devices discovered")
    
    finally:
        sdk.shutdown()


def example_custom_data_processing():
    """Example showing custom data processing."""
    print("=== Custom Data Processing Example ===")
    
    # Track statistics
    stats = {
        'total_events': 0,
        'total_force_magnitude': 0.0,
        'max_force': 0.0,
        'min_force': float('inf')
    }
    
    def custom_processor(event):
        stats['total_events'] += 1
        
        if event.sensors:
            for sensor in event.sensors:
                # Calculate force magnitude
                force_mag = (sensor.forces[0]**2 + sensor.forces[1]**2 + sensor.forces[2]**2)**0.5
                stats['total_force_magnitude'] += force_mag
                stats['max_force'] = max(stats['max_force'], force_mag)
                stats['min_force'] = min(stats['min_force'], force_mag)
    
    sdk = AxioforceSDK()
    
    try:
        # Initialize simulator
        if not sdk.initialize_simulator(log_level="info"):
            print("Failed to initialize simulator")
            return
        
        sdk.on_data_received = custom_processor
        
        # Start collection
        if sdk.start_data_collection(timeout=5.0):
            print("Processing data...")
            time.sleep(3)
            
            # Print statistics
            if stats['total_events'] > 0:
                avg_force = stats['total_force_magnitude'] / stats['total_events']
                print(f"Statistics:")
                print(f"  Total events: {stats['total_events']}")
                print(f"  Average force magnitude: {avg_force:.2f}")
                print(f"  Max force: {stats['max_force']:.2f}")
                print(f"  Min force: {stats['min_force']:.2f}")
            else:
                print("No data processed")
        else:
            print("Failed to start data collection")
    
    finally:
        sdk.shutdown()


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Axioforce SDK Examples")
    parser.add_argument("--example", choices=[
        "basic", "simulator", "csv", "context", "control", "custom", "all"
    ], default="all", help="Which example to run")
    
    args = parser.parse_args()
    
    examples = {
        "basic": example_basic_usage,
        "simulator": example_simulator_usage,
        "csv": example_csv_output,
        "context": example_context_manager,
        "control": example_device_control,
        "custom": example_custom_data_processing,
    }
    
    if args.example == "all":
        for name, func in examples.items():
            print(f"\n{'='*50}")
            func()
            print(f"{'='*50}")
    else:
        examples[args.example]()


if __name__ == "__main__":
    main() 