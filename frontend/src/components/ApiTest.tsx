import React, { useState } from 'react';
import { Button, Typography, Alert, Paper } from '@mui/material';
import { authApi } from '../services/api';
import { UserCreate, UserRole } from '../types';

const ApiTest: React.FC = () => {
  const [testResult, setTestResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testApiConnection = async () => {
    setLoading(true);
    setTestResult('Testing API connection...\n');
    
    try {
      // Test 1: Health check
      const healthResponse = await fetch('http://localhost:8000/health');
      const healthData = await healthResponse.json();
      setTestResult(prev => prev + `✅ Health Check: ${healthResponse.status} - ${JSON.stringify(healthData)}\n`);
      
      // Test 2: Database health
      const dbResponse = await fetch('http://localhost:8000/health/database');
      const dbData = await dbResponse.json();
      setTestResult(prev => prev + `✅ Database Health: ${dbResponse.status} - ${JSON.stringify(dbData)}\n`);
      
      // Test 3: Registration API
      const timestamp = Date.now();
      const testData: UserCreate = {
        full_name: `Test User ${timestamp}`,
        email: `test${timestamp}@example.com`,
        username: `testuser${timestamp}`,
        password: 'password123',
        role: UserRole.STUDENT,
        department: 'engineering',
        student_id: '12345',
        phone_number: '1234567890'
      };
      
      setTestResult(prev => prev + `🧪 Testing registration with data: ${JSON.stringify(testData, null, 2)}\n`);
      
      const regResponse = await authApi.register(testData);
      setTestResult(prev => prev + `✅ Registration Test: ${regResponse.status} - User ID: ${regResponse.data.id}\n`);
      
      setTestResult(prev => prev + `\n🎉 All tests passed! API is working correctly.`);
      
    } catch (error: any) {
      console.error('API Test Error:', error);
      setTestResult(prev => prev + `\n❌ Error: ${error.message}\n`);
      if (error.response) {
        setTestResult(prev => prev + `Response Status: ${error.response.status}\n`);
        setTestResult(prev => prev + `Response Data: ${JSON.stringify(error.response.data)}\n`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, m: 2 }}>
      <Typography variant="h6" gutterBottom>
        API Connection Test
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        This component tests the API connection and registration functionality.
      </Typography>
      
      <Button
        variant="contained"
        onClick={testApiConnection}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? 'Testing...' : 'Test API Connection'}
      </Button>
      
      {testResult && (
        <Alert severity={testResult.includes('❌') ? 'error' : 'success'} sx={{ mt: 2 }}>
          <Typography component="pre" sx={{ fontSize: '0.8rem', whiteSpace: 'pre-wrap' }}>
            {testResult}
          </Typography>
        </Alert>
      )}
    </Paper>
  );
};

export default ApiTest;
