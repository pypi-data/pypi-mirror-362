#!/usr/bin/env python3
"""
Simple test for the Axioforce Python SDK.

This script tests basic SDK functionality from the correct directory.
"""

import sys
import os
import time

# Change to the sensor directory where config files are located
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

try:
    from axioforce_sdk import AxioforceSDK, create_console_printer
    print("✓ SDK imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SDK: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic SDK functionality."""
    print("\nTesting basic SDK functionality...")
    
    try:
        # Create SDK instance
        sdk = AxioforceSDK()
        print("✓ SDK instance created")
        
        # Initialize simulator
        if sdk.initialize_simulator(log_level="info"):
            print("✓ Simulator initialized")
            
            # Get environment info
            env = sdk.get_environment()
            if env:
                print(f"  Environment: {env}")
            
            # Set up simple data handler
            event_count = 0
            def data_handler(event):
                nonlocal event_count
                event_count += 1
                if event_count <= 3:  # Only print first 3 events
                    print(f"  Event {event_count}: {event.device_name} - {len(event.sensors)} sensors")
            
            sdk.on_data_received = data_handler
            
            # Start data collection
            if sdk.start_data_collection(timeout=5.0):
                print("✓ Data collection started")
                
                # Wait for some events
                time.sleep(2)
                
                final_count = sdk.get_event_count()
                print(f"✓ Collected {final_count} events")
                
                if final_count > 0:
                    print("✓ Data collection working correctly")
                    sdk.shutdown()
                    return True
                else:
                    print("✗ No events received")
                    sdk.shutdown()
                    return False
            else:
                print("✗ Failed to start data collection")
                sdk.shutdown()
                return False
        else:
            print("✗ Failed to initialize simulator")
            return False
    
    except Exception as e:
        print(f"✗ Exception during testing: {e}")
        return False

def test_context_manager():
    """Test context manager functionality."""
    print("\nTesting context manager...")
    
    try:
        with AxioforceSDK() as sdk:
            if sdk.initialize_simulator(log_level="info"):
                print("✓ Context manager initialization successful")
                env = sdk.get_environment()
                if env:
                    print(f"  Environment: {env}")
                return True
            else:
                print("✗ Failed to initialize in context manager")
                return False
    except Exception as e:
        print(f"✗ Exception in context manager: {e}")
        return False

def main():
    """Run tests."""
    print("Axioforce SDK Simple Test")
    print("=" * 30)
    
    # Test basic functionality
    if test_basic_functionality():
        print("\n✓ Basic functionality test passed")
    else:
        print("\n✗ Basic functionality test failed")
        return 1
    
    # Test context manager
    if test_context_manager():
        print("✓ Context manager test passed")
    else:
        print("✗ Context manager test failed")
        return 1
    
    print("\n" + "=" * 30)
    print("✓ All tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 