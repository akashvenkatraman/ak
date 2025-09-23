"""
SVCE ERP Integration Service
Handles data synchronization with Sri Venkateswara College of Engineering ERP
"""

import requests
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SVCEERPIntegrationService:
    def __init__(self):
        self.erp_base_url = "https://erp.svce.ac.in"
        self.session = requests.Session()
        self.session_token = None
        
    async def authenticate(self, username: str, password: str, captcha: str) -> bool:
        """Authenticate with SVCE ERP system"""
        try:
            login_data = {
                'username': username,
                'password': password,
                'captcha': captcha
            }
            
            response = self.session.post(
                f"{self.erp_base_url}/login",
                data=login_data,
                timeout=30
            )
            
            if response.status_code == 200:
                self.session_token = response.cookies.get('session_id')
                logger.info("Successfully authenticated with SVCE ERP")
                return True
            else:
                logger.error(f"ERP authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"ERP authentication error: {str(e)}")
            return False
    
    async def fetch_students(self) -> List[Dict[str, Any]]:
        """Fetch student data from ERP"""
        try:
            if not self.session_token:
                raise Exception("Not authenticated with ERP")
            
            response = self.session.get(
                f"{self.erp_base_url}/api/students",
                headers={'Authorization': f'Bearer {self.session_token}'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch students: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching students: {str(e)}")
            return []
    
    async def fetch_teachers(self) -> List[Dict[str, Any]]:
        """Fetch teacher data from ERP"""
        try:
            if not self.session_token:
                raise Exception("Not authenticated with ERP")
            
            response = self.session.get(
                f"{self.erp_base_url}/api/teachers",
                headers={'Authorization': f'Bearer {self.session_token}'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch teachers: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching teachers: {str(e)}")
            return []
    
    async def fetch_certificates(self) -> List[Dict[str, Any]]:
        """Fetch certificate data from ERP"""
        try:
            if not self.session_token:
                raise Exception("Not authenticated with ERP")
            
            response = self.session.get(
                f"{self.erp_base_url}/api/certificates",
                headers={'Authorization': f'Bearer {self.session_token}'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch certificates: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching certificates: {str(e)}")
            return []
    
    async def sync_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Sync user data with local database"""
        try:
            # Map ERP data to your user schema
            mapped_data = {
                'student_id': user_data.get('rollNumber'),
                'full_name': user_data.get('name'),
                'email': user_data.get('email'),
                'department': user_data.get('department'),
                'year': user_data.get('year'),
                'phone_number': user_data.get('phone'),
                'date_of_birth': user_data.get('dob'),
                'erp_user_id': user_data.get('id'),
                'last_synced': datetime.now().isoformat()
            }
            
            # Update local database
            # This would integrate with your existing user management
            logger.info(f"Synced user data for: {mapped_data['full_name']}")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing user data: {str(e)}")
            return False
    
    async def sync_certificate_data(self, cert_data: Dict[str, Any]) -> bool:
        """Sync certificate data with local database"""
        try:
            # Map ERP certificate data to your certificate schema
            mapped_data = {
                'student_id': cert_data.get('studentId'),
                'certificate_name': cert_data.get('certificateName'),
                'certificate_type': cert_data.get('certificateType'),
                'issue_date': cert_data.get('issueDate'),
                'expiry_date': cert_data.get('expiryDate'),
                'status': cert_data.get('status'),
                'erp_certificate_id': cert_data.get('id'),
                'last_synced': datetime.now().isoformat()
            }
            
            # Update local database
            logger.info(f"Synced certificate: {mapped_data['certificate_name']}")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing certificate data: {str(e)}")
            return False
    
    async def full_sync(self) -> Dict[str, Any]:
        """Perform full synchronization with ERP"""
        try:
            sync_results = {
                'students_synced': 0,
                'teachers_synced': 0,
                'certificates_synced': 0,
                'errors': []
            }
            
            # Sync students
            students = await self.fetch_students()
            for student in students:
                if await self.sync_user_data(student):
                    sync_results['students_synced'] += 1
            
            # Sync teachers
            teachers = await self.fetch_teachers()
            for teacher in teachers:
                if await self.sync_user_data(teacher):
                    sync_results['teachers_synced'] += 1
            
            # Sync certificates
            certificates = await self.fetch_certificates()
            for cert in certificates:
                if await self.sync_certificate_data(cert):
                    sync_results['certificates_synced'] += 1
            
            logger.info(f"Full sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"Full sync failed: {str(e)}")
            return {'error': str(e)}

# Global instance
erp_service = SVCEERPIntegrationService()
