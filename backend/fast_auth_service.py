#!/usr/bin/env python3
"""Fast authentication service using only local database"""

from typing import Optional, Dict, Any, List
from app.core.database import SessionLocal
from sqlalchemy import text

class FastAuthService:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username from local database only - no external calls"""
        try:
            result = self.db.execute(text("""
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
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID from local database only"""
        try:
            result = self.db.execute(text("""
                SELECT id, email, username, full_name, hashed_password, role, status, is_active, phone_number, 
                       department, student_id, employee_id, performance_score, total_credits_earned,
                       profile_picture, bio, date_of_birth, address, city, state, country, postal_code,
                       linkedin_url, twitter_url, website_url, is_oauth_user, verification_code,
                       verification_expires, created_at, updated_at
                FROM users 
                WHERE id = :user_id
            """), {"user_id": user_id})
            
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
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users from local database only"""
        try:
            result = self.db.execute(text("""
                SELECT id, email, username, full_name, hashed_password, role, status, is_active, phone_number, 
                       department, student_id, employee_id, performance_score, total_credits_earned,
                       profile_picture, bio, date_of_birth, address, city, state, country, postal_code,
                       linkedin_url, twitter_url, website_url, is_oauth_user, verification_code,
                       verification_expires, created_at, updated_at
                FROM users 
                ORDER BY created_at DESC
            """))
            
            users = []
            for row in result.fetchall():
                users.append({
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
                })
            
            return users
            
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            users = self.get_users()
            
            # Count by role
            role_counts = {}
            status_counts = {}
            
            for user in users:
                role = user.get('role', 'unknown')
                status = user.get('status', 'unknown')
                
                role_counts[role] = role_counts.get(role, 0) + 1
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "total_users": len(users),
                "role_counts": role_counts,
                "status_counts": status_counts,
                "database_type": "SQLite (Local)",
                "last_updated": "now"
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}

# Global fast auth service instance
fast_auth = FastAuthService()
