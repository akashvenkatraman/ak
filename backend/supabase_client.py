#!/usr/bin/env python3
"""Supabase client for real-time data synchronization"""

import requests
import json
from typing import Dict, List, Optional, Any
from config import settings

class SupabaseClient:
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users from Supabase"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/users",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching users: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Supabase API error: {e}")
            return []
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID from Supabase"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/users?id=eq.{user_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                users = response.json()
                return users[0] if users else None
            else:
                print(f"Error fetching user {user_id}: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Supabase API error: {e}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user in Supabase"""
        try:
            response = requests.post(
                f"{self.url}/rest/v1/users",
                headers=self.headers,
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 201:
                return response.json()[0] if response.json() else None
            else:
                print(f"Error creating user: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Supabase API error: {e}")
            return None
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user in Supabase"""
        try:
            response = requests.patch(
                f"{self.url}/rest/v1/users?id=eq.{user_id}",
                headers=self.headers,
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()[0] if response.json() else None
            else:
                print(f"Error updating user {user_id}: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Supabase API error: {e}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user from Supabase"""
        try:
            response = requests.delete(
                f"{self.url}/rest/v1/users?id=eq.{user_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 204:
                return True
            else:
                print(f"Error deleting user {user_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Supabase API error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test Supabase connection"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/users?select=count",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Supabase connection successful")
                return True
            else:
                print(f"❌ Supabase connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Supabase connection error: {e}")
            return False

# Global Supabase client instance
supabase_client = SupabaseClient()
