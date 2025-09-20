import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
} from '@mui/material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { UserCreate, UserRole } from '../types';
import { authApi } from '../services/api';
import ApiTest from '../components/ApiTest';

const RegisterPageDebug: React.FC = () => {
  const [userData, setUserData] = useState<UserCreate>({
    email: '',
    username: '',
    full_name: '',
    password: '',
    role: UserRole.STUDENT,
    phone_number: '',
    department: '',
    student_id: '',
    employee_id: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [debugInfo, setDebugInfo] = useState('');
  
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setDebugInfo('');
    setLoading(true);

    // Validation
    if (userData.password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (userData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      setLoading(false);
      return;
    }

    // Add debug info
    const debugData = {
      timestamp: new Date().toISOString(),
      userData: userData,
      apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
      endpoint: '/auth/register'
    };
    setDebugInfo(JSON.stringify(debugData, null, 2));

    try {
      console.log('🚀 Attempting registration with data:', userData);
      console.log('🌐 API URL:', process.env.REACT_APP_API_URL || 'http://localhost:8000');
      
      const response = await authApi.register(userData);
      console.log('✅ Registration successful:', response.data);
      
      setSuccess('Registration successful! Please wait for admin approval before logging in.');
      setTimeout(() => navigate('/login'), 3000);
    } catch (err: any) {
      console.error('❌ Registration error:', err);
      console.error('❌ Error response:', err.response);
      console.error('❌ Error message:', err.message);
      
      let errorMessage = 'Registration failed. Please try again.';
      
      if (err.response) {
        // Server responded with error status
        errorMessage = err.response.data?.detail || `Server error: ${err.response.status}`;
        console.error('❌ Server error details:', err.response.data);
      } else if (err.request) {
        // Request was made but no response received
        errorMessage = 'Network error: Unable to connect to server. Please check if the backend is running.';
        console.error('❌ Network error:', err.request);
      } else {
        // Something else happened
        errorMessage = `Error: ${err.message}`;
        console.error('❌ Other error:', err.message);
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserData({
      ...userData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRoleChange = (e: any) => {
    setUserData({
      ...userData,
      role: e.target.value as UserRole,
    });
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: 4,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography component="h1" variant="h4" gutterBottom>
              Certificate Management Portal - DEBUG
            </Typography>
            <Typography component="h2" variant="h5" gutterBottom>
              Sign Up (Debug Version)
            </Typography>
            
            <ApiTest />

            {error && (
              <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
                {error}
              </Alert>
            )}

            {success && (
              <Alert severity="success" sx={{ width: '100%', mb: 2 }}>
                {success}
              </Alert>
            )}

            {debugInfo && (
              <Alert severity="info" sx={{ width: '100%', mb: 2 }}>
                <Typography variant="body2" component="pre" sx={{ fontSize: '0.8rem' }}>
                  {debugInfo}
                </Typography>
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="full_name"
                label="Full Name"
                name="full_name"
                autoComplete="name"
                autoFocus
                value={userData.full_name}
                onChange={handleChange}
                disabled={loading}
              />
              
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                type="email"
                value={userData.email}
                onChange={handleChange}
                disabled={loading}
              />
              
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
                value={userData.username}
                onChange={handleChange}
                disabled={loading}
              />

              <FormControl fullWidth margin="normal" required>
                <InputLabel id="role-label">Role</InputLabel>
                <Select
                  labelId="role-label"
                  id="role"
                  value={userData.role}
                  label="Role"
                  onChange={handleRoleChange}
                  disabled={loading}
                >
                  <MenuItem value={UserRole.STUDENT}>Student</MenuItem>
                  <MenuItem value={UserRole.TEACHER}>Teacher</MenuItem>
                </Select>
              </FormControl>

              <TextField
                margin="normal"
                fullWidth
                id="department"
                label="Department"
                name="department"
                value={userData.department}
                onChange={handleChange}
                disabled={loading}
              />

              {userData.role === UserRole.STUDENT && (
                <TextField
                  margin="normal"
                  fullWidth
                  id="student_id"
                  label="Student ID"
                  name="student_id"
                  value={userData.student_id}
                  onChange={handleChange}
                  disabled={loading}
                />
              )}

              {userData.role === UserRole.TEACHER && (
                <TextField
                  margin="normal"
                  fullWidth
                  id="employee_id"
                  label="Employee ID"
                  name="employee_id"
                  value={userData.employee_id}
                  onChange={handleChange}
                  disabled={loading}
                />
              )}

              <TextField
                margin="normal"
                fullWidth
                id="phone_number"
                label="Phone Number"
                name="phone_number"
                value={userData.phone_number}
                onChange={handleChange}
                disabled={loading}
              />
              
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
                value={userData.password}
                onChange={handleChange}
                disabled={loading}
                helperText="Password must be at least 8 characters long"
              />
              
              <TextField
                margin="normal"
                required
                fullWidth
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={loading}
              />
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Sign Up (Debug)'}
              </Button>
              
              <Box textAlign="center">
                <Link component={RouterLink} to="/login" variant="body2">
                  Already have an account? Sign In
                </Link>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPageDebug;
