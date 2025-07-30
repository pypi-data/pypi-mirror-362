#!/usr/bin/env python3
"""
Simple CSV output example using the Axioforce Python SDK.

This example demonstrates how to use the SDK to output sensor data in CSV format,
similar to the original capi_device.py functionality.
"""

import sys
import os
import time
import argparse

# Change to the sensor directory where config files are located
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from axioforce_sdk import AxioforceSDK, create_csv_collector


def main():
    """Main function demonstrating CSV output."""
    parser = argparse.ArgumentParser(description="Axioforce SDK CSV Output Example")
    parser.add_argument("--output", "-o", default="sensor_output.csv", 
                       help="Output CSV file path")
    parser.add_argument("--duration", "-d", type=float, default=5.0,
                       help="Data collection duration in seconds")
    parser.add_argument("--log-level", default="info",
                       choices=["debug", "info", "warning", "error"],
                       help="Log level")
    
    args = parser.parse_args()
    
    print("Axioforce SDK - CSV Output Example")
    print("=" * 40)
    print(f"Output file: {args.output}")
    print(f"Duration: {args.duration} seconds")
    print(f"Log level: {args.log_level}")
    print()
    
    # Create SDK instance
    sdk = AxioforceSDK()
    
    try:
        # Initialize simulator
        print("Initializing simulator...")
        if not sdk.initialize_simulator(log_level=args.log_level):
            print("✗ Failed to initialize simulator")
            return 1
        print("✓ Simulator initialized")
        
        # Create CSV collector
        print(f"Setting up CSV output to {args.output}...")
        csv_collector = create_csv_collector(args.output, include_header=True)
        sdk.on_data_received = csv_collector
        print("✓ CSV collector configured")
        
        # Start data collection
        print("Starting data collection...")
        if sdk.start_data_collection(timeout=10.0):
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


if __name__ == "__main__":
    sys.exit(main()) 