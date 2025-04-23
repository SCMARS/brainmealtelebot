from datetime import datetime, timedelta
from bot.services.firestore import FirestoreService

class LimiterService:
    @staticmethod
    async def can_generate(user_id: int) -> bool:
        """Check if user can generate a meal plan"""
        profile = await FirestoreService.get_profile(user_id)
        
        if not profile:
            return False
            
        if profile.get('is_subscribed', False):
            return True
            
        last_generation = profile.get('last_generation')
        if not last_generation:
            return True
            
        last_generation_date = datetime.fromisoformat(last_generation)
        return datetime.now() - last_generation_date > timedelta(days=1)

    @staticmethod
    async def update_last_generation(user_id: int):
        """Update last generation timestamp"""
        await FirestoreService.save_profile(user_id, {
            'last_generation': datetime.now().isoformat()
        }) 