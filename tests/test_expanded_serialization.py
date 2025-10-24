#!/usr/bin/env python3
"""
Test the improved record serialization
"""

from services.pocketbase_service import serialize_record

# Mock the problematic data structure you showed
class MockRecord:
    def __init__(self, record_id, name):
        self.id = record_id
        self.name = name
        self.title = f"Achievement {name}"

def test_serialization():
    print("🔄 Testing Improved Record Serialization...")
    
    # Create mock data similar to what you're seeing
    mock_achievement_record1 = MockRecord('w2k83vnglz1fwfn', 'First Achievement')
    mock_achievement_record2 = MockRecord('8gl22oaxmwlalye', 'Second Achievement')
    
    # Mock the problematic data structure
    test_data = [
        {
            'id': 'u84ahrfaw48c1pm',
            'created': '',
            'updated': '',
            'expand': {'achievement': mock_achievement_record1},  # This was causing issues
            'achievement': 'w2k83vnglz1fwfn',
            'collection_id': 'pbc_1001000004',
            'collection_name': 'user_achievements',
            'unlocked_at': '2025-10-15 05:33:54.959Z',
            'user': '1wl76h4t3bfv5ak'
        },
        {
            'id': 'ff1trq36crs07ui',
            'created': '',
            'updated': '',
            'expand': {'achievement': mock_achievement_record2},  # This was causing issues
            'achievement': '8gl22oaxmwlalye',
            'collection_id': 'pbc_1001000004',
            'collection_name': 'user_achievements',
            'unlocked_at': '2025-10-15 04:56:20.034Z',
            'user': '1wl76h4t3bfv5ak'
        }
    ]
    
    print(f"📋 Original data structure (problematic):")
    for i, item in enumerate(test_data):
        print(f"   Item {i+1}: expand.achievement = {item['expand']['achievement']}")
    
    # Test serialization on each item
    serialized_data = []
    for item in test_data:
        try:
            serialized_item = serialize_record(type('MockRecord', (), item)())
            serialized_data.append(serialized_item)
            print(f"✅ Successfully serialized item with ID: {item['id']}")
        except Exception as e:
            print(f"❌ Failed to serialize item: {e}")
    
    # Test JSON serialization
    import json
    try:
        json_str = json.dumps(serialized_data, indent=2)
        print(f"✅ JSON serialization successful!")
        print(f"   Result length: {len(json_str)} characters")
        print(f"   First expanded achievement: {serialized_data[0].get('expand', {}).get('achievement', {}).get('title', 'Not found')}")
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")

if __name__ == "__main__":
    test_serialization()
