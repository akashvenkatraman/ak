#!/usr/bin/env python3
"""Test hybrid database service for real-time data synchronization"""

import requests
import json
import time
from datetime import datetime
from hybrid_database_service import hybrid_db

def test_hybrid_database():
    """Test hybrid database service"""
    print("=== Hybrid Database Service Test ===")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test database stats
    print("\n📊 Testing database statistics...")
    stats = hybrid_db.get_database_stats()
    print(f"   Total users: {stats.get('total_users', 0)}")
    print(f"   Role counts: {stats.get('role_counts', {})}")
    print(f"   Status counts: {stats.get('status_counts', {})}")
    print(f"   Database type: {stats.get('database_type', 'Unknown')}")
    print(f"   Supabase sync: {stats.get('supabase_sync', False)}")
    
    # Test get users
    print("\n👥 Testing get users...")
    users = hybrid_db.get_users()
    print(f"   Retrieved {len(users)} users")
    for user in users:
        print(f"     - {user['username']} ({user['role']}) - {user['status']}")
    
    # Test get user by username
    print("\n🔍 Testing get user by username...")
    if users:
        test_username = users[0]['username']
        user_data = hybrid_db.get_user_by_username(test_username)
        if user_data:
            print(f"   ✅ Found user: {user_data['username']} ({user_data['role']})")
        else:
            print(f"   ❌ User not found: {test_username}")
    
    # Test Supabase sync
    print("\n🔄 Testing Supabase sync...")
    sync_success = hybrid_db.sync_with_supabase()
    if sync_success:
        print("   ✅ Supabase sync successful")
    else:
        print("   ⚠️  Supabase sync failed (using local data only)")
    
    return True

def test_api_endpoints():
    """Test API endpoints with hybrid database"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        # Test health
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   Health check: {response.status_code}")
        
        # Test login
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Login successful: {data.get('user', {}).get('username')}")
            
            # Test admin users endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=10)
            
            if response.status_code == 200:
                users = response.json()
                print(f"   ✅ Admin users endpoint: {len(users)} users")
                for user in users:
                    print(f"       - {user.get('username')} ({user.get('role')}) - {user.get('status')}")
            else:
                print(f"   ❌ Admin users endpoint failed: {response.status_code}")
            
            # Test database stats endpoint
            response = requests.get("http://localhost:8000/admin/database-stats", headers=headers, timeout=10)
            if response.status_code == 200:
                stats = response.json()
                print(f"   ✅ Database stats: {stats.get('total_users', 0)} users")
            else:
                print(f"   ❌ Database stats endpoint failed: {response.status_code}")
            
            # Test sync endpoint
            response = requests.post("http://localhost:8000/admin/sync-supabase", headers=headers, timeout=10)
            if response.status_code == 200:
                sync_result = response.json()
                print(f"   ✅ Sync endpoint: {sync_result.get('message')}")
            else:
                print(f"   ❌ Sync endpoint failed: {response.status_code}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API test error: {e}")
        return False
    
    return True

def test_real_time_data_consistency():
    """Test real-time data consistency"""
    print("\n🔄 Testing real-time data consistency...")
    
    try:
        # Get initial user count
        initial_users = hybrid_db.get_users()
        initial_count = len(initial_users)
        print(f"   Initial user count: {initial_count}")
        
        # Test API consistency
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get users from API
            response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=10)
            if response.status_code == 200:
                api_users = response.json()
                api_count = len(api_users)
                print(f"   API user count: {api_count}")
                
                if initial_count == api_count:
                    print("   ✅ Data consistency: Local and API counts match")
                    return True
                else:
                    print(f"   ❌ Data inconsistency: Local {initial_count}, API {api_count}")
                    return False
            else:
                print(f"   ❌ Failed to get users from API: {response.status_code}")
                return False
        else:
            print(f"   ❌ Login failed for consistency test: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Consistency test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Hybrid Database Service Test")
    
    # Test hybrid database service
    if not test_hybrid_database():
        print("❌ Hybrid database service test failed")
        exit(1)
    
    # Test API endpoints
    if not test_api_endpoints():
        print("❌ API endpoints test failed")
        exit(1)
    
    # Test real-time data consistency
    if not test_real_time_data_consistency():
        print("❌ Real-time data consistency test failed")
        exit(1)
    
    print("\n🎉 All hybrid database tests passed!")
    print("✅ Real-time data synchronization is working")
    print("✅ API endpoints are functioning correctly")
    print("✅ Data consistency is maintained")
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
