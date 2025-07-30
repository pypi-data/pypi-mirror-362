#!/usr/bin/env python3
"""
Command-line interface for the Axioforce Python SDK.

This module provides command-line tools for common SDK operations.
"""

import sys
import os
import time
import argparse
from pathlib import Path

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Change to the sensor directory where config files are located
# This is needed for the C API to find the configuration files
sensor_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')
if os.path.exists(sensor_dir):
    os.chdir(sensor_dir)

from axioforce_sdk import AxioforceSDK, create_csv_collector, create_console_printer


def csv_output():
    """Command-line tool for CSV output."""
    parser = argparse.ArgumentParser(
        description="Axioforce SDK - CSV Output Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  axioforce-csv --output data.csv --duration 10
  axioforce-csv --simulator --output test.csv --duration 5
  axioforce-csv --real-devices --output live_data.csv
        """
    )
    
    parser.add_argument("--output", "-o", default="sensor_output.csv",
                       help="Output CSV file path (default: sensor_output.csv)")
    parser.add_argument("--duration", "-d", type=float, default=5.0,
                       help="Data collection duration in seconds (default: 5.0)")
    parser.add_argument("--simulator", action="store_true",
                       help="Use simulator mode (default)")
    parser.add_argument("--real-devices", action="store_true",
                       help="Use real hardware devices")
    parser.add_argument("--log-level", default="info",
                       choices=["debug", "info", "warning", "error"],
                       help="Log level (default: info)")
    parser.add_argument("--csv-file", help="CSV file for simulator data")
    
    args = parser.parse_args()
    
    print("Axioforce SDK - CSV Output Tool")
    print("=" * 40)
    print(f"Output file: {args.output}")
    print(f"Duration: {args.duration} seconds")
    print(f"Mode: {'Simulator' if args.simulator or not args.real_devices else 'Real Devices'}")
    print(f"Log level: {args.log_level}")
    print()
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize based on mode
        if args.real_devices:
            print("Initializing for real devices...")
            if not sdk.initialize(log_level=args.log_level):
                print("✗ Failed to initialize for real devices")
                return 1
        else:
            print("Initializing simulator...")
            if not sdk.initialize_simulator(csv_file=args.csv_file, log_level=args.log_level):
                print("✗ Failed to initialize simulator")
                return 1
        
        print("✓ Initialization successful")
        
        # Create CSV collector
        print(f"Setting up CSV output to {args.output}...")
        csv_collector = create_csv_collector(args.output, include_header=True)
        sdk.on_data_received = csv_collector
        print("✓ CSV collector configured")
        
        # Start data collection
        print("Starting data collection...")
        timeout = 15.0 if args.real_devices else 10.0
        if sdk.start_data_collection(timeout=timeout):
            print("✓ Data collection started")
            print(f"Collecting data for {args.duration} seconds...")
            
            # Collect data for specified duration
            time.sleep(args.duration)
            
            # Get final statistics
            event_count = sdk.get_event_count()
            print(f"✓ Collection complete")
            print(f"  Total events: {event_count}")
            print(f"  Events per second: {event_count / args.duration:.1f}")
            print(f"  Data saved to: {args.output}")
            
        else:
            print("✗ Failed to start data collection")
            return 1
    
    except KeyboardInterrupt:
        print("\n⏹ Collection interrupted by user")
        event_count = sdk.get_event_count()
        print(f"  Events collected: {event_count}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
    
    finally:
        # Cleanup
        print("\nCleaning up...")
        sdk.shutdown()
        print("✓ Cleanup complete")
    
    return 0


def test_sdk():
    """Command-line tool for testing the SDK."""
    parser = argparse.ArgumentParser(
        description="Axioforce SDK - Test Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  axioforce-test
  axioforce-test --verbose
  axioforce-test --quick
        """
    )
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--quick", "-q", action="store_true",
                       help="Quick test (skip data collection)")
    
    args = parser.parse_args()
    
    print("Axioforce SDK - Test Tool")
    print("=" * 30)
    
    # Test 1: Import
    print("1. Testing SDK import...")
    try:
        from axioforce_sdk import AxioforceSDK, DeviceState
        print("✓ SDK imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SDK: {e}")
        return 1
    
    # Test 2: SDK creation
    print("2. Testing SDK creation...")
    try:
        sdk = AxioforceSDK()
        print("✓ SDK instance created successfully")
    except Exception as e:
        print(f"✗ Failed to create SDK instance: {e}")
        return 1
    
    # Test 3: Simulator initialization
    print("3. Testing simulator initialization...")
    try:
        if sdk.initialize_simulator(log_level="info"):
            print("✓ Simulator initialized successfully")
            env = sdk.get_environment()
            if env and args.verbose:
                print(f"  Environment: {env}")
        else:
            print("✗ Failed to initialize simulator")
            sdk.shutdown()
            return 1
    except Exception as e:
        print(f"✗ Exception during simulator initialization: {e}")
        sdk.shutdown()
        return 1
    
    # Test 4: Data collection (if not quick test)
    if not args.quick:
        print("4. Testing data collection...")
        try:
            event_count = 0
            def data_callback(event):
                nonlocal event_count
                event_count += 1
                if args.verbose and event_count <= 3:
                    print(f"  Event {event_count}: {event.device_name} - {len(event.sensors)} sensors")
            
            sdk.on_data_received = data_callback
            
            if sdk.start_data_collection(timeout=5.0):
                print("✓ Data collection started")
                
                # Wait for some events
                time.sleep(2)
                
                final_count = sdk.get_event_count()
                print(f"✓ Collected {final_count} events")
                
                if final_count > 0:
                    print("✓ Data collection working correctly")
                else:
                    print("✗ No events received")
                    sdk.shutdown()
                    return 1
            else:
                print("✗ Failed to start data collection")
                sdk.shutdown()
                return 1
        except Exception as e:
            print(f"✗ Exception during data collection: {e}")
            sdk.shutdown()
            return 1
    
    # Test 5: Context manager
    print("5. Testing context manager...")
    try:
        with AxioforceSDK() as sdk2:
            if sdk2.initialize_simulator(log_level="info"):
                print("✓ Context manager initialization successful")
                env = sdk2.get_environment()
                if env and args.verbose:
                    print(f"  Environment: {env}")
            else:
                print("✗ Failed to initialize in context manager")
                return 1
    except Exception as e:
        print(f"✗ Exception in context manager: {e}")
        return 1
    
    # Cleanup
    sdk.shutdown()
    
    print("\n" + "=" * 30)
    print("✓ All tests passed!")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Axioforce Python SDK Command Line Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available commands:
  csv     Output sensor data to CSV file
  test    Test SDK functionality
  
For help on a specific command:
  axioforce <command> --help
        """
    )
    
    parser.add_argument("command", choices=["csv", "test"],
                       help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "csv":
        return csv_output()
    elif args.command == "test":
        return test_sdk()


if __name__ == "__main__":
    sys.exit(main()) 