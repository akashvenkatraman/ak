#!/usr/bin/env python3
"""Hybrid database service for real-time data synchronization"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from app.core.database import SessionLocal
from sqlalchemy import text
from supabase_client import supabase_client

class HybridDatabaseService:
    def __init__(self):
        self.supabase_client = supabase_client
        self.local_db = SessionLocal()
    
    def sync_with_supabase(self) -> bool:
        """Sync local database with Supabase"""
        try:
            print("🔄 Syncing with Supabase...")
            
            # Test Supabase connection
            if not self.supabase_client.test_connection():
                print("❌ Supabase connection failed, using local data only")
                return False
            
            # Get users from Supabase
            supabase_users = self.supabase_client.get_users()
            print(f"📊 Supabase users: {len(supabase_users)}")
            
            # Get users from local database
            result = self.local_db.execute(text("SELECT * FROM users"))
            local_users = result.fetchall()
            print(f"📊 Local users: {len(local_users)}")
            
            # Sync users to Supabase (if local has more users)
            if len(local_users) > len(supabase_users):
                print("📤 Syncing local users to Supabase...")
                for user in local_users:
                    user_data = {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "full_name": user.full_name,
                        "hashed_password": user.hashed_password,
                        "role": user.role,
                        "status": user.status,
                        "is_active": user.is_active,
                        "phone_number": user.phone_number,
                        "department": user.department,
                        "student_id": user.student_id,
                        "employee_id": user.employee_id,
                        "performance_score": user.performance_score,
                        "total_credits_earned": user.total_credits_earned,
                        "profile_picture": user.profile_picture,
                        "bio": user.bio,
                        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth and hasattr(user.date_of_birth, 'isoformat') else str(user.date_of_birth) if user.date_of_birth else None,
                        "address": user.address,
                        "city": user.city,
                        "state": user.state,
                        "country": user.country,
                        "postal_code": user.postal_code,
                        "linkedin_url": user.linkedin_url,
                        "twitter_url": user.twitter_url,
                        "website_url": user.website_url,
                        "is_oauth_user": user.is_oauth_user,
                        "verification_code": user.verification_code,
                        "verification_expires": user.verification_expires.isoformat() if user.verification_expires and hasattr(user.verification_expires, 'isoformat') else str(user.verification_expires) if user.verification_expires else None,
                    "created_at": user.created_at.isoformat() if user.created_at and hasattr(user.created_at, 'isoformat') else str(user.created_at) if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at and hasattr(user.updated_at, 'isoformat') else str(user.updated_at) if user.updated_at else None
                    }
                    
                    # Check if user exists in Supabase
                    existing_user = self.supabase_client.get_user_by_id(user.id)
                    if not existing_user:
                        # Create user in Supabase
                        created_user = self.supabase_client.create_user(user_data)
                        if created_user:
                            print(f"✅ Created user {user.username} in Supabase")
                        else:
                            print(f"❌ Failed to create user {user.username} in Supabase")
                    else:
                        print(f"ℹ️  User {user.username} already exists in Supabase")
            
            # Sync users from Supabase to local (if Supabase has more users)
            elif len(supabase_users) > len(local_users):
                print("📥 Syncing Supabase users to local...")
                for user_data in supabase_users:
                    # Check if user exists locally
                    result = self.local_db.execute(text("SELECT id FROM users WHERE id = :id"), {"id": user_data["id"]})
                    existing_user = result.fetchone()
                    
                    if not existing_user:
                        # Create user locally
                        self.local_db.execute(text("""
                            INSERT INTO users (id, email, username, full_name, hashed_password, role, status, is_active, 
                                             phone_number, department, student_id, employee_id, performance_score, 
                                             total_credits_earned, profile_picture, bio, date_of_birth, address, 
                                             city, state, country, postal_code, linkedin_url, twitter_url, website_url, 
                                             is_oauth_user, verification_code, verification_expires, created_at, updated_at)
                            VALUES (:id, :email, :username, :full_name, :hashed_password, :role, :status, :is_active,
                                    :phone_number, :department, :student_id, :employee_id, :performance_score,
                                    :total_credits_earned, :profile_picture, :bio, :date_of_birth, :address,
                                    :city, :state, :country, :postal_code, :linkedin_url, :twitter_url, :website_url,
                                    :is_oauth_user, :verification_code, :verification_expires, :created_at, :updated_at)
                        """), user_data)
                        print(f"✅ Created user {user_data['username']} locally")
                    else:
                        print(f"ℹ️  User {user_data['username']} already exists locally")
                
                self.local_db.commit()
            
            print("✅ Sync completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Sync error: {e}")
            return False
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get users from local database (primary source)"""
        try:
            result = self.local_db.execute(text("""
                SELECT id, email, username, full_name, role, status, is_active, phone_number, 
                       department, student_id, employee_id, performance_score, total_credits_earned,
                       profile_picture, bio, date_of_birth, address, city, state, country, postal_code,
                       linkedin_url, twitter_url, website_url, is_oauth_user, verification_code,
                       verification_expires, created_at, updated_at
                FROM users 
                ORDER BY created_at DESC
            """))
            
            users = []
            for row in result.fetchall():
                user_dict = {
                    "id": row.id,
                    "email": row.email,
                    "username": row.username,
                    "full_name": row.full_name,
                    "role": row.role.lower() if row.role else None,
                    "status": row.status.lower() if row.status else None,
                    "is_active": row.is_active,
                    "phone_number": row.phone_number,
                    "department": row.department,
                    "student_id": row.student_id,
                    "employee_id": row.employee_id,
                    "performance_score": row.performance_score,
                    "total_credits_earned": row.total_credits_earned,
                    "profile_picture": row.profile_picture,
                    "bio": row.bio,
                    "date_of_birth": row.date_of_birth.isoformat() if row.date_of_birth and hasattr(row.date_of_birth, 'isoformat') else str(row.date_of_birth) if row.date_of_birth else None,
                    "address": row.address,
                    "city": row.city,
                    "state": row.state,
                    "country": row.country,
                    "postal_code": row.postal_code,
                    "linkedin_url": row.linkedin_url,
                    "twitter_url": row.twitter_url,
                    "website_url": row.website_url,
                    "is_oauth_user": row.is_oauth_user,
                    "verification_code": row.verification_code,
                    "verification_expires": row.verification_expires.isoformat() if row.verification_expires and hasattr(row.verification_expires, 'isoformat') else str(row.verification_expires) if row.verification_expires else None,
                "created_at": row.created_at.isoformat() if row.created_at and hasattr(row.created_at, 'isoformat') else str(row.created_at) if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at and hasattr(row.updated_at, 'isoformat') else str(row.updated_at) if row.updated_at else None
                }
                users.append(user_dict)
            
            return users
            
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username from local database"""
        try:
            result = self.local_db.execute(text("""
                SELECT id, email, username, full_name, hashed_password, role, status, is_active, phone_number, 
                       department, student_id, employee_id, performance_score, total_credits_earned,
                       profile_picture, bio, date_of_birth, address, city, state, country, postal_code,
                       linkedin_url, twitter_url, website_url, is_oauth_user, verification_code,
                       verification_expires, created_at, updated_at
                FROM users 
                WHERE username = :username
            """), {"username": username})
            
            row = result.fetchone()
            if row:
                return {
                    "id": row.id,
                    "email": row.email,
                    "username": row.username,
                    "full_name": row.full_name,
                    "hashed_password": row.hashed_password,
                    "role": row.role.lower() if row.role else None,
                    "status": row.status.lower() if row.status else None,
                    "is_active": row.is_active,
                    "phone_number": row.phone_number,
                    "department": row.department,
                    "student_id": row.student_id,
                    "employee_id": row.employee_id,
                    "performance_score": row.performance_score,
                    "total_credits_earned": row.total_credits_earned,
                    "profile_picture": row.profile_picture,
                    "bio": row.bio,
                    "date_of_birth": row.date_of_birth.isoformat() if row.date_of_birth and hasattr(row.date_of_birth, 'isoformat') else str(row.date_of_birth) if row.date_of_birth else None,
                    "address": row.address,
                    "city": row.city,
                    "state": row.state,
                    "country": row.country,
                    "postal_code": row.postal_code,
                    "linkedin_url": row.linkedin_url,
                    "twitter_url": row.twitter_url,
                    "website_url": row.website_url,
                    "is_oauth_user": row.is_oauth_user,
                    "verification_code": row.verification_code,
                    "verification_expires": row.verification_expires.isoformat() if row.verification_expires and hasattr(row.verification_expires, 'isoformat') else str(row.verification_expires) if row.verification_expires else None,
                "created_at": row.created_at.isoformat() if row.created_at and hasattr(row.created_at, 'isoformat') else str(row.created_at) if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at and hasattr(row.updated_at, 'isoformat') else str(row.updated_at) if row.updated_at else None
                }
            return None
            
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create user in local database and sync to Supabase"""
        try:
            # Create user in local database
            result = self.local_db.execute(text("""
                INSERT INTO users (email, username, full_name, hashed_password, role, status, is_active, 
                                 phone_number, department, student_id, employee_id, performance_score, 
                                 total_credits_earned, profile_picture, bio, date_of_birth, address, 
                                 city, state, country, postal_code, linkedin_url, twitter_url, website_url, 
                                 is_oauth_user, verification_code, verification_expires, created_at)
                VALUES (:email, :username, :full_name, :hashed_password, :role, :status, :is_active,
                        :phone_number, :department, :student_id, :employee_id, :performance_score,
                        :total_credits_earned, :profile_picture, :bio, :date_of_birth, :address,
                        :city, :state, :country, :postal_code, :linkedin_url, :twitter_url, :website_url,
                        :is_oauth_user, :verification_code, :verification_expires, datetime('now'))
                RETURNING id, email, username, full_name, role, status, is_active, phone_number, 
                          department, student_id, employee_id, performance_score, total_credits_earned,
                          profile_picture, bio, date_of_birth, address, city, state, country, postal_code,
                          linkedin_url, twitter_url, website_url, is_oauth_user, verification_code,
                          verification_expires, created_at, updated_at
            """), user_data)
            
            new_user = result.fetchone()
            self.local_db.commit()
            
            if new_user:
                user_dict = {
                    "id": new_user.id,
                    "email": new_user.email,
                    "username": new_user.username,
                    "full_name": new_user.full_name,
                    "role": new_user.role.lower() if new_user.role else None,
                    "status": new_user.status.lower() if new_user.status else None,
                    "is_active": new_user.is_active,
                    "phone_number": new_user.phone_number,
                    "department": new_user.department,
                    "student_id": new_user.student_id,
                    "employee_id": new_user.employee_id,
                    "performance_score": new_user.performance_score,
                    "total_credits_earned": new_user.total_credits_earned,
                    "profile_picture": new_user.profile_picture,
                    "bio": new_user.bio,
                    "date_of_birth": new_user.date_of_birth.isoformat() if new_user.date_of_birth else None,
                    "address": new_user.address,
                    "city": new_user.city,
                    "state": new_user.state,
                    "country": new_user.country,
                    "postal_code": new_user.postal_code,
                    "linkedin_url": new_user.linkedin_url,
                    "twitter_url": new_user.twitter_url,
                    "website_url": new_user.website_url,
                    "is_oauth_user": new_user.is_oauth_user,
                    "verification_code": new_user.verification_code,
                    "verification_expires": new_user.verification_expires.isoformat() if new_user.verification_expires else None,
                    "created_at": new_user.created_at.isoformat() if new_user.created_at else None,
                    "updated_at": new_user.updated_at.isoformat() if new_user.updated_at else None
                }
                
                # Try to sync to Supabase
                try:
                    self.supabase_client.create_user(user_dict)
                    print(f"✅ User {new_user.username} synced to Supabase")
                except Exception as e:
                    print(f"⚠️  User {new_user.username} created locally but not synced to Supabase: {e}")
                
                return user_dict
            
            return None
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            # Get user counts by role
            result = self.local_db.execute(text("""
                SELECT role, COUNT(*) as count 
                FROM users 
                GROUP BY role
            """))
            role_counts = dict(result.fetchall())
            
            # Get user counts by status
            result = self.local_db.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM users 
                GROUP BY status
            """))
            status_counts = dict(result.fetchall())
            
            # Get total users
            result = self.local_db.execute(text("SELECT COUNT(*) FROM users"))
            total_users = result.fetchone()[0]
            
            return {
                "total_users": total_users,
                "role_counts": role_counts,
                "status_counts": status_counts,
                "database_type": "SQLite (Local)",
                "supabase_sync": self.supabase_client.test_connection()
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}

# Global hybrid database service instance
hybrid_db = HybridDatabaseService()
