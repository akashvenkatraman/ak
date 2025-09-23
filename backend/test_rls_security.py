#!/usr/bin/env python3
"""
RLS Security Test Script for Smart Student Hub
Tests if Row Level Security policies are working correctly
"""

import os
import sys
import requests
import json
from typing import Dict, List, Any

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

class RLSSecurityTester:
    def __init__(self):
        self.config = Config()
        self.base_url = "http://localhost:8000"
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_api_health(self) -> bool:
        """Test if the API is running"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.log_test("API Health Check", True, "API is running")
                return True
            else:
                self.log_test("API Health Check", False, f"API returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"API is not accessible: {str(e)}")
            return False

    def test_authentication(self) -> bool:
        """Test if authentication is working"""
        try:
            # Test login endpoint
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"email": "test@example.com", "password": "testpass"},
                                   timeout=5)
            
            if response.status_code in [200, 401, 422]:  # 401/422 are expected for invalid credentials
                self.log_test("Authentication Endpoint", True, "Authentication endpoint is accessible")
                return True
            else:
                self.log_test("Authentication Endpoint", False, f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication Endpoint", False, f"Authentication test failed: {str(e)}")
            return False

    def test_database_connection(self) -> bool:
        """Test if database connection is working"""
        try:
            from app.core.database import get_db
            db = next(get_db())
            self.log_test("Database Connection", True, "Database connection successful")
            return True
        except Exception as e:
            self.log_test("Database Connection", False, f"Database connection failed: {str(e)}")
            return False

    def test_supabase_connection(self) -> bool:
        """Test if Supabase connection is working"""
        try:
            from app.core.supabase_client import supabase
            # Try to get a simple query
            result = supabase.table('users').select('id').limit(1).execute()
            self.log_test("Supabase Connection", True, "Supabase connection successful")
            return True
        except Exception as e:
            self.log_test("Supabase Connection", False, f"Supabase connection failed: {str(e)}")
            return False

    def test_rls_policies(self) -> bool:
        """Test if RLS policies are working"""
        try:
            from app.core.supabase_client import supabase
            
            # Test 1: Try to access users table without authentication
            try:
                result = supabase.table('users').select('*').execute()
                if result.data:
                    self.log_test("RLS Policy - Users Table", False, 
                                "Users table accessible without authentication - RLS may not be working")
                    return False
                else:
                    self.log_test("RLS Policy - Users Table", True, 
                                "Users table properly protected by RLS")
            except Exception as e:
                if "Row Level Security" in str(e) or "permission denied" in str(e).lower():
                    self.log_test("RLS Policy - Users Table", True, 
                                "Users table properly protected by RLS")
                else:
                    self.log_test("RLS Policy - Users Table", False, 
                                f"Unexpected error: {str(e)}")
                    return False

            # Test 2: Try to access file_storage table
            try:
                result = supabase.table('file_storage').select('*').execute()
                if result.data:
                    self.log_test("RLS Policy - File Storage", False, 
                                "File storage table accessible without authentication")
                    return False
                else:
                    self.log_test("RLS Policy - File Storage", True, 
                                "File storage table properly protected")
            except Exception as e:
                if "Row Level Security" in str(e) or "permission denied" in str(e).lower():
                    self.log_test("RLS Policy - File Storage", True, 
                                "File storage table properly protected")
                else:
                    self.log_test("RLS Policy - File Storage", False, 
                                f"Unexpected error: {str(e)}")
                    return False

            return True
            
        except Exception as e:
            self.log_test("RLS Policy Test", False, f"RLS test failed: {str(e)}")
            return False

    def test_storage_buckets(self) -> bool:
        """Test if storage buckets are accessible"""
        try:
            from app.core.supabase_client import supabase
            
            # Test if buckets exist
            try:
                result = supabase.storage.list_buckets()
                buckets = [bucket['name'] for bucket in result]
                
                required_buckets = ['user-images', 'profile-pictures', 'activity-documents']
                missing_buckets = [bucket for bucket in required_buckets if bucket not in buckets]
                
                if missing_buckets:
                    self.log_test("Storage Buckets", False, 
                                f"Missing buckets: {missing_buckets}")
                    return False
                else:
                    self.log_test("Storage Buckets", True, 
                                f"All required buckets found: {buckets}")
                    return True
                    
            except Exception as e:
                self.log_test("Storage Buckets", False, f"Storage bucket test failed: {str(e)}")
                return False
                
        except Exception as e:
            self.log_test("Storage Buckets", False, f"Storage test failed: {str(e)}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all security tests"""
        print("🔒 RLS Security Test Suite for Smart Student Hub")
        print("=" * 60)
        print()
        
        tests = [
            self.test_api_health,
            self.test_authentication,
            self.test_database_connection,
            self.test_supabase_connection,
            self.test_rls_policies,
            self.test_storage_buckets
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_test(test.__name__, False, f"Test crashed: {str(e)}")
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        print()
        
        if passed == total:
            print("🎉 All security tests passed! Your system is secure.")
        else:
            print("⚠️  Some tests failed. Please review the issues above.")
            print()
            print("🔧 To fix RLS issues:")
            print("1. Go to your Supabase Dashboard")
            print("2. Open SQL Editor")
            print("3. Run the fix_rls_security.sql script")
            print("4. Verify all policies are created")
        
        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "results": self.test_results
        }

def main():
    """Main function"""
    tester = RLSSecurityTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("rls_security_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Detailed results saved to: rls_security_test_results.json")
    
    # Exit with appropriate code
    if results["passed_tests"] == results["total_tests"]:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()

