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
                        gender TEXT,
                        weight INTEGER,
                        height INTEGER,
                        goal TEXT,
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
                # Create meals table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS meals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT,
                        name TEXT,
                        calories INTEGER,
                        protein INTEGER,
                        carbs INTEGER,
                        fat INTEGER,
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
                    (user_id, age, gender, weight, height, goal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    data['age'],
                    data['gender'],
                    data['weight'],
                    data['height'],
                    data['goal']
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
                    SELECT age, gender, weight, height, goal
                    FROM user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    profile = {
                        'age': result[0],
                        'gender': result[1],
                        'weight': result[2],
                        'height': result[3],
                        'goal': result[4]
                    }
                    logging.info(f"Found profile: {profile}")
                    return profile
                logging.info("No profile found")
                return None
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            return None

    def update_subscription(self, user_id: int, plan: str, duration_days: int) -> bool:
        """Update user subscription"""
        try:
            logging.info(f"Updating subscription for user {user_id} with plan {plan} for {duration_days} days")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                end_date = datetime.now().timestamp() + (duration_days * 24 * 60 * 60)
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

    def get_user_meals(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Get user's recent meals"""
        try:
            logging.info(f"Getting meals for user {user_id} with limit {limit}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT type, name, calories, protein, carbs, fat, created_at
                    FROM meals
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, limit))
                results = cursor.fetchall()
                
                meals = [{
                    'type': r[0],
                    'name': r[1],
                    'calories': r[2],
                    'protein': r[3],
                    'carbs': r[4],
                    'fat': r[5],
                    'timestamp': r[6]
                } for r in results]
                logging.info(f"Found {len(meals)} meals")
                return meals
        except Exception as e:
            logging.error(f"Error getting user meals: {e}")
            return []

    def save_meal(self, user_id: int, meal_data: Dict) -> bool:
        """Save a meal to the database"""
        try:
            logging.info(f"Saving meal for user {user_id}: {meal_data}")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO meals 
                    (user_id, type, name, calories, protein, carbs, fat)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    meal_data['type'],
                    meal_data['name'],
                    meal_data['calories'],
                    meal_data['protein'],
                    meal_data['carbs'],
                    meal_data['fat']
                ))
                conn.commit()
                logging.info("Meal saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving meal: {e}")
            return False 