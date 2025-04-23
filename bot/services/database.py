import sqlite3
from typing import Dict, Optional, List
from datetime import datetime
import logging

class DatabaseService:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Create user profiles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_profiles (
                        user_id INTEGER PRIMARY KEY,
                        age INTEGER,
                        weight INTEGER,
                        height INTEGER,
                        goal TEXT,
                        dietary_restrictions TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create subscriptions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS subscriptions (
                        user_id INTEGER PRIMARY KEY,
                        plan TEXT,
                        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        end_date TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE,
                        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                    )
                """)
                # Create generation history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS generation_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        plan_type TEXT,
                        calories INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                    )
                """)
                conn.commit()
                logging.info("Database initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
            raise

    def save_profile(self, user_id: int, data: Dict) -> bool:
        """Save user profile to database"""
        try:
            logging.info(f"Saving profile for user {user_id} with data: {data}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_profiles 
                    (user_id, age, weight, height, goal, dietary_restrictions)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    data['age'],
                    data['weight'],
                    data['height'],
                    data['goal'],
                    data['dietary_restrictions']
                ))
                conn.commit()
                logging.info("Profile saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving profile: {e}")
            return False

    def get_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile from database"""
        try:
            logging.info(f"Getting profile for user {user_id}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT age, weight, height, goal, dietary_restrictions
                    FROM user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    profile = {
                        'age': result[0],
                        'weight': result[1],
                        'height': result[2],
                        'goal': result[3],
                        'dietary_restrictions': result[4]
                    }
                    logging.info(f"Found profile: {profile}")
                    return profile
                logging.info("No profile found")
                return None
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            return None

    def update_subscription(self, user_id: int, plan: str) -> bool:
        """Update user subscription"""
        try:
            logging.info(f"Updating subscription for user {user_id} with plan {plan}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                end_date = datetime.now().timestamp() + (30 * 24 * 60 * 60)
                cursor.execute("""
                    INSERT OR REPLACE INTO subscriptions 
                    (user_id, plan, end_date, is_active)
                    VALUES (?, ?, ?, ?)
                """, (user_id, plan, end_date, True))
                conn.commit()
                logging.info("Subscription updated successfully")
            return True
        except Exception as e:
            logging.error(f"Error updating subscription: {e}")
            return False

    def get_subscription_status(self, user_id: int) -> bool:
        """Check if user has active subscription"""
        try:
            logging.info(f"Checking subscription status for user {user_id}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT is_active, end_date
                    FROM subscriptions
                    WHERE user_id = ? AND is_active = TRUE
                """, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    is_active, end_date = result
                    if is_active and datetime.now().timestamp() < end_date:
                        logging.info("Active subscription found")
                        return True
                logging.info("No active subscription found")
                return False
        except Exception as e:
            logging.error(f"Error checking subscription: {e}")
            return False

    def save_generation(self, user_id: int, plan_type: str, calories: int) -> bool:
        """Save generation history"""
        try:
            logging.info(f"Saving generation for user {user_id}: {plan_type}, {calories} calories")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO generation_history 
                    (user_id, plan_type, calories)
                    VALUES (?, ?, ?)
                """, (user_id, plan_type, calories))
                conn.commit()
                logging.info("Generation saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving generation: {e}")
            return False

    def get_generation_history(self, user_id: int) -> List[Dict]:
        """Get user's generation history"""
        try:
            logging.info(f"Getting generation history for user {user_id}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT plan_type, calories, created_at
                    FROM generation_history
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                """, (user_id,))
                results = cursor.fetchall()
                
                history = [{
                    'plan_type': r[0],
                    'calories': r[1],
                    'timestamp': r[2]
                } for r in results]
                logging.info(f"Found {len(history)} generations")
                return history
        except Exception as e:
            logging.error(f"Error getting generation history: {e}")
            return [] 