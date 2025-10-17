#!/usr/bin/env python3
"""
Test record serialization to fix JSON serialization issues
"""

from services.pocketbase_service import pocketbase_service, serialize_record
import json

def test_serialization():
    print("🔄 Testing Record Serialization...")
    
    # Test the serialize_record function with a mock object
    class MockRecord:
        def __init__(self):
            self.id = "test123"
            self.name = "Test Achievement"
            self.description = "Test Description"
            self.expand = MockExpandedRecord()  # Simulate expanded relation
    
    class MockExpandedRecord:
        def __init__(self):
            self.id = "user456"
            self.email = "test@example.com"
    
    # Test serialization
    mock_record = MockRecord()
    try:
        serialized = serialize_record(mock_record)
        print(f"✅ Serialization successful:")
        print(f"   Type: {type(serialized)}")
        print(f"   Content: {serialized}")
        
        # Test JSON serialization
        json_str = json.dumps(serialized, indent=2)
        print(f"✅ JSON serialization successful:")
        print(f"   Length: {len(json_str)} characters")
        
    except Exception as e:
        print(f"❌ Serialization failed: {e}")
    
    # Test with None
    try:
        empty_result = serialize_record(None)
        print(f"✅ None handling: {empty_result}")
    except Exception as e:
        print(f"❌ None handling failed: {e}")

def test_service_connectivity():
    print("\n🔄 Testing Service Connectivity...")
    print(f"   Service URL: {pocketbase_service.base_url}")
    print(f"   Current token: {pocketbase_service.get_auth_token() or 'None'}")
    print("   Ready for authentication testing!")

if __name__ == "__main__":
    test_serialization()
    test_service_connectivity()
