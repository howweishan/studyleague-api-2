#!/usr/bin/env python3
"""
Comprehensive diagnostic for achievements data
"""

from services.pocketbase_service import pocketbase_service

def diagnose_achievements_data():
    print("🔍 COMPREHENSIVE ACHIEVEMENTS DIAGNOSTIC")
    print("=" * 60)
    
    user_id = "1wl76h4t3bfv5ak"  # The user ID from your debug output
    
    print(f"\n1. 📋 Checking if user exists: {user_id}")
    try:
        user = pocketbase_service.get_record("users", user_id)
        print(f"   ✅ User found: {user.get('email', 'No email')} (ID: {user.get('id', 'No ID')})")
    except Exception as e:
        print(f"   ❌ User not found: {e}")
        return
    
    print(f"\n2. 📊 Checking total users in database")
    try:
        all_users = pocketbase_service.get_records("users", "", "", per_page=10)
        print(f"   Total users: {all_users['total_items']}")
        if all_users['items']:
            print("   Sample users:")
            for user in all_users['items'][:3]:
                print(f"     - {user.get('email', 'No email')} (ID: {user.get('id', 'No ID')})")
    except Exception as e:
        print(f"   ❌ Error getting users: {e}")
    
    print(f"\n3. 🏆 Checking total achievements available")
    try:
        all_achievements = pocketbase_service.get_records("achievements", "", "")
        print(f"   Total achievements: {all_achievements['total_items']}")
        if all_achievements['items']:
            print("   Sample achievements:")
            for ach in all_achievements['items'][:3]:
                print(f"     - {ach.get('title', 'No title')} (ID: {ach.get('id', 'No ID')})")
    except Exception as e:
        print(f"   ❌ Error getting achievements: {e}")
    
    print(f"\n4. 🎖️ Checking total user_achievements in database")
    try:
        all_user_achievements = pocketbase_service.get_records("user_achievements", "", "", per_page=10)
        print(f"   Total user_achievements: {all_user_achievements['total_items']}")
        if all_user_achievements['items']:
            print("   Sample user_achievements:")
            for ua in all_user_achievements['items'][:5]:
                user_ref = ua.get('user', 'No user')
                achievement_ref = ua.get('achievement', 'No achievement')
                unlocked_at = ua.get('unlockedAt', 'No date')
                print(f"     - User: {user_ref}, Achievement: {achievement_ref}, Unlocked: {unlocked_at}")
        else:
            print("   ⚠️  No user_achievements records found in database!")
    except Exception as e:
        print(f"   ❌ Error getting user_achievements: {e}")
    
    print(f"\n5. 🔍 Checking user_achievements for specific user: {user_id}")
    try:
        user_specific = pocketbase_service.get_records(
            "user_achievements", 
            f"user = '{user_id}'", 
            "-unlockedAt"
        )
        print(f"   User-specific achievements: {user_specific['total_items']}")
        if user_specific['items']:
            for ua in user_specific['items']:
                print(f"     - Achievement: {ua.get('achievement', 'No achievement')}, Unlocked: {ua.get('unlockedAt', 'No date')}")
        else:
            print(f"   ⚠️  User {user_id} has no achievements yet!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n6. 🧪 Testing different user IDs (if available)")
    try:
        all_users = pocketbase_service.get_records("users", "", "", per_page=5)
        if all_users['items'] and len(all_users['items']) > 1:
            for test_user in all_users['items'][:2]:
                test_id = test_user.get('id')
                if test_id != user_id:
                    print(f"   Testing user: {test_user.get('email', 'No email')} (ID: {test_id})")
                    test_achievements = pocketbase_service.get_records(
                        "user_achievements", 
                        f"user = '{test_id}'", 
                        "-unlockedAt"
                    )
                    print(f"     -> Has {test_achievements['total_items']} achievements")
    except Exception as e:
        print(f"   ❌ Error testing other users: {e}")
    
    print(f"\n7. 💡 RECOMMENDATIONS:")
    print("   - If no user_achievements exist, you need to create some test data")
    print("   - Check your PocketBase admin panel to verify data structure")
    print("   - Consider adding a route to unlock achievements for testing")
    print("   - Verify the user_achievements collection has the correct relations")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    diagnose_achievements_data()
