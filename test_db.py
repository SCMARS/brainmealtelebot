from bot.services.database import DatabaseService
import os

def test_database():
    """Test database functionality"""
    # Initialize database
    db = DatabaseService("test.db")
    
    # Test profile operations
    test_user_id = 123456
    test_profile = {
        'age': 25,
        'weight': 70,
        'height': 175,
        'goal': 'lose_weight',
        'dietary_restrictions': 'vegan'
    }
    
    # Test saving profile
    print("Testing profile save...")
    if db.save_profile(test_user_id, test_profile):
        print("✅ Profile saved successfully")
    else:
        print("❌ Failed to save profile")
        return
    
    # Test getting profile
    print("\nTesting profile retrieval...")
    profile = db.get_profile(test_user_id)
    if profile:
        print("✅ Profile retrieved successfully")
        print(f"Profile data: {profile}")
    else:
        print("❌ Failed to retrieve profile")
        return
    
    # Test subscription operations
    print("\nTesting subscription operations...")
    if db.update_subscription(test_user_id, "month"):
        print("✅ Subscription updated successfully")
    else:
        print("❌ Failed to update subscription")
        return
    
    # Test subscription status
    is_subscribed = db.get_subscription_status(test_user_id)
    print(f"Subscription status: {'Active' if is_subscribed else 'Inactive'}")
    
    # Test generation history
    print("\nTesting generation history...")
    if db.save_generation(test_user_id, "daily", 2000):
        print("✅ Generation saved successfully")
    else:
        print("❌ Failed to save generation")
        return
    
    history = db.get_generation_history(test_user_id)
    print(f"Generation history: {history}")
    
    # Clean up
    try:
        os.remove("test.db")
        print("\n✅ Test database cleaned up")
    except:
        print("\n❌ Failed to clean up test database")

if __name__ == "__main__":
    test_database() 