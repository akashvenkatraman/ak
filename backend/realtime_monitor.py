#!/usr/bin/env python3
"""Real-time database monitoring script"""

import time
import requests
from datetime import datetime
from app.core.database import SessionLocal
from sqlalchemy import text

def get_database_stats():
    """Get current database statistics"""
    try:
        db = SessionLocal()
        
        # Get user counts by role
        result = db.execute(text("""
            SELECT role, COUNT(*) as count 
            FROM users 
            GROUP BY role
        """))
        role_counts = dict(result.fetchall())
        
        # Get user counts by status
        result = db.execute(text("""
            SELECT status, COUNT(*) as count 
            FROM users 
            GROUP BY status
        """))
        status_counts = dict(result.fetchall())
        
        # Get total users
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        total_users = result.fetchone()[0]
        
        # Get recent users (last 5)
        result = db.execute(text("""
            SELECT username, role, status, created_at 
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 5
        """))
        recent_users = result.fetchall()
        
        db.close()
        
        return {
            'total_users': total_users,
            'role_counts': role_counts,
            'status_counts': status_counts,
            'recent_users': recent_users
        }
    except Exception as e:
        print(f"Database error: {e}")
        return None

def test_api_endpoints():
    """Test API endpoints for real-time data"""
    try:
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        health_status = health_response.status_code == 200
        
        # Test login
        login_data = {"username": "admin", "password": "admin123"}
        login_response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=5)
        login_success = login_response.status_code == 200
        
        if login_success:
            token = login_response.json().get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test user data endpoint
            me_response = requests.get("http://localhost:8000/auth/me", headers=headers, timeout=5)
            me_success = me_response.status_code == 200
            
            # Test admin users endpoint
            users_response = requests.get("http://localhost:8000/admin/users", headers=headers, timeout=5)
            users_success = users_response.status_code == 200
            
            return {
                'health': health_status,
                'login': login_success,
                'user_data': me_success,
                'admin_users': users_success
            }
        else:
            return {
                'health': health_status,
                'login': False,
                'user_data': False,
                'admin_users': False
            }
    except Exception as e:
        print(f"API test error: {e}")
        return None

def display_realtime_data():
    """Display real-time data in a formatted way"""
    print("=" * 80)
    print(f"🕐 REAL-TIME DATABASE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get database stats
    db_stats = get_database_stats()
    if db_stats:
        print(f"\n📊 DATABASE STATISTICS:")
        print(f"   Total Users: {db_stats['total_users']}")
        
        print(f"\n👥 Users by Role:")
        for role, count in db_stats['role_counts'].items():
            print(f"   {role.title()}: {count}")
        
        print(f"\n📋 Users by Status:")
        for status, count in db_stats['status_counts'].items():
            print(f"   {status.title()}: {count}")
        
        print(f"\n🆕 Recent Users:")
        for user in db_stats['recent_users']:
            print(f"   - {user[0]} ({user[1]}) - {user[2]} - {user[3]}")
    
    # Test API endpoints
    api_status = test_api_endpoints()
    if api_status:
        print(f"\n🌐 API STATUS:")
        print(f"   Health Check: {'✅' if api_status['health'] else '❌'}")
        print(f"   Login: {'✅' if api_status['login'] else '❌'}")
        print(f"   User Data: {'✅' if api_status['user_data'] else '❌'}")
        print(f"   Admin Users: {'✅' if api_status['admin_users'] else '❌'}")
    
    print("\n" + "=" * 80)

def monitor_realtime_data(interval=5, duration=60):
    """Monitor real-time data for specified duration"""
    print("🚀 Starting real-time database monitoring...")
    print(f"⏱️  Update interval: {interval} seconds")
    print(f"⏰ Duration: {duration} seconds")
    print("Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            display_realtime_data()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")
    
    print(f"\n✅ Monitoring completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
            monitor_realtime_data(interval, duration)
        else:
            print("Usage: python realtime_monitor.py [monitor] [interval] [duration]")
            print("Example: python realtime_monitor.py monitor 5 60")
    else:
        # Single display
        display_realtime_data()
