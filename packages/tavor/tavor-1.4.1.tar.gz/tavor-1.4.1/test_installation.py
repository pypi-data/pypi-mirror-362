#!/usr/bin/env python3
"""
Test script to verify Tavor SDK installation.

Run this script to ensure the Tavor SDK is properly installed and functional.
"""

import sys


def test_installation():
    """Test that the Tavor SDK is properly installed."""
    print("🧪 Testing Tavor SDK Installation")
    print("=" * 40)

    try:
        # Test basic imports
        print("1. Testing imports...")
        import tavor

        print(f"   ✓ Tavor SDK version: {tavor.__version__}")

        # Test core classes
        from tavor import (
            Tavor,
            BoxConfig,
            BoxStatus,
            CommandResult,
            CommandStatus,
            TavorError,
        )

        print("   ✓ Core classes imported successfully")

        # Test async classes if available
        try:
            from tavor import AsyncTavor, AsyncBoxHandle

            print("   ✓ Async classes imported successfully")
            async_available = True
        except ImportError:
            print(
                "   ⚠ Async classes not available (install with: pip install tavor[async])"
            )
            async_available = False

        # Test client initialization
        print("\n2. Testing client initialization...")
        try:
            client = Tavor(api_key="test-key")
            print("   ✓ Sync client initialized")
        except Exception as e:
            print(f"   ✗ Sync client failed: {e}")
            return False

        if async_available:
            try:
                import asyncio

                async def test_async():
                    async with AsyncTavor(api_key="test-key") as client:
                        return True

                asyncio.run(test_async())
                print("   ✓ Async client initialized")
            except Exception as e:
                print(f"   ✗ Async client failed: {e}")

        # Test configuration
        print("\n3. Testing configuration...")
        config = BoxConfig(
            template=BoxTemplate.PRO, timeout=3600, metadata={"test": "installation"}
        )
        print("   ✓ BoxConfig created successfully")

        # Test enum values
        print("\n4. Testing enums...")
        assert BoxStatus.RUNNING == "running"
        assert CommandStatus.DONE == "done"
        assert BoxTemplate.BASIC == "Basic"
        assert BoxTemplate.PRO == "Pro"
        print("   ✓ Enum values correct")

        # Test exception handling
        print("\n5. Testing exceptions...")
        try:
            raise TavorError("Test error")
        except TavorError:
            print("   ✓ Exception handling works")

        print("\n" + "=" * 40)
        print("🎉 All tests passed! Tavor SDK is ready to use.")
        print("\nTo get started:")
        print("1. Get your API key from https://tavor.dev")
        print("2. Replace 'your-api-key' in your code")
        print("3. Start creating boxes!")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("\nPlease install the Tavor SDK:")
        print("  pip install tavor")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)
