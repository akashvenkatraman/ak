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
  InputAdornment,
  IconButton,
  Divider,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Person,
  Email,
  Lock,
  Phone,
  School,
  Badge,
  CheckCircle,
  Google as GoogleIcon,
} from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { UserCreate, UserRole } from '../types';
import Logo from '../components/Logo';
import api from '../services/api';

const RegisterPage: React.FC = () => {
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
  const [googleLoading, setGoogleLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  // Validation states
  const [validationErrors, setValidationErrors] = useState<{[key: string]: string}>({});
  const [fieldTouched, setFieldTouched] = useState<{[key: string]: boolean}>({});
  
  const { register } = useAuth();
  const navigate = useNavigate();

  // Validation functions
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string): {isValid: boolean, message: string} => {
    if (password.length < 8) {
      return { isValid: false, message: 'Password must be at least 8 characters long' };
    }
    if (!/(?=.*[a-z])/.test(password)) {
      return { isValid: false, message: 'Password must contain at least one lowercase letter' };
    }
    if (!/(?=.*[A-Z])/.test(password)) {
      return { isValid: false, message: 'Password must contain at least one uppercase letter' };
    }
    if (!/(?=.*\d)/.test(password)) {
      return { isValid: false, message: 'Password must contain at least one number' };
    }
    return { isValid: true, message: '' };
  };

  const validateField = (name: string, value: string): string => {
    switch (name) {
      case 'full_name':
        if (!value.trim()) return 'Full name is required';
        if (value.trim().length < 2) return 'Full name must be at least 2 characters';
        return '';
      case 'email':
        if (!value.trim()) return 'Email is required';
        if (!validateEmail(value)) return 'Please enter a valid email address';
        return '';
      case 'username':
        if (!value.trim()) return 'Username is required';
        if (value.length < 3) return 'Username must be at least 3 characters';
        if (!/^[a-zA-Z0-9_]+$/.test(value)) return 'Username can only contain letters, numbers, and underscores';
        return '';
      case 'password':
        const passwordValidation = validatePassword(value);
        return passwordValidation.isValid ? '' : passwordValidation.message;
      case 'confirmPassword':
        if (!value) return 'Please confirm your password';
        if (value !== userData.password) return 'Passwords do not match';
        return '';
      case 'phone_number':
        if (value && !/^[+]?[1-9][\d]{0,15}$/.test(value.replace(/[\s\-()]/g, ''))) {
          return 'Please enter a valid phone number';
        }
        return '';
      case 'student_id':
        if (userData.role === UserRole.STUDENT && !value.trim()) {
          return 'Student ID is required for students';
        }
        return '';
      case 'employee_id':
        if (userData.role === UserRole.TEACHER && !value.trim()) {
          return 'Employee ID is required for teachers';
        }
        return '';
      default:
        return '';
    }
  };

  const handleFieldBlur = (name: string) => {
    setFieldTouched({ ...fieldTouched, [name]: true });
    const value = name === 'confirmPassword' ? confirmPassword : userData[name as keyof UserCreate] as string;
    const error = validateField(name, value);
    setValidationErrors({ ...validationErrors, [name]: error });
  };

  const handleFieldChange = (name: string, value: string) => {
    if (name === 'confirmPassword') {
      setConfirmPassword(value);
    } else {
      setUserData({ ...userData, [name]: value });
    }
    
    // Clear error when user starts typing
    if (validationErrors[name]) {
      setValidationErrors({ ...validationErrors, [name]: '' });
    }
  };

  // Check if form is valid
  const isFormValid = () => {
    const requiredFields = ['full_name', 'email', 'username', 'password'];
    const roleSpecificFields = userData.role === UserRole.STUDENT ? ['student_id'] : ['employee_id'];
    
    const allFields = [...requiredFields, ...roleSpecificFields];
    
    return allFields.every(field => {
      const value = field === 'confirmPassword' ? confirmPassword : userData[field as keyof UserCreate] as string;
      return value && !validateField(field, value);
    }) && confirmPassword === userData.password;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    // Validate all fields
    const errors: {[key: string]: string} = {};
    const requiredFields = ['full_name', 'email', 'username', 'password'];
    const roleSpecificFields = userData.role === UserRole.STUDENT ? ['student_id'] : ['employee_id'];
    
    [...requiredFields, ...roleSpecificFields].forEach(field => {
      const value = userData[field as keyof UserCreate] as string;
      const error = validateField(field, value);
      if (error) errors[field] = error;
    });
    
    const confirmPasswordError = validateField('confirmPassword', confirmPassword);
    if (confirmPasswordError) errors.confirmPassword = confirmPasswordError;

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      setError('Please fix the errors below');
      setLoading(false);
      return;
    }

    try {
      console.log('🚀 Attempting registration with data:', userData);
      console.log('🌐 API URL:', process.env.REACT_APP_API_URL || 'http://localhost:8000');
      
      await register(userData);
      console.log('✅ Registration successful!');
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
      } else if (err.request) {
        // Request was made but no response received
        errorMessage = 'Network error: Unable to connect to server. Please check if the backend is running.';
      } else {
        // Something else happened
        errorMessage = `Error: ${err.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    setGoogleLoading(true);
    setError('');
    
    try {
      // Get Google OAuth URL from backend
      const response = await api.get('/api/auth/google/url');
      const { url } = response.data;
      
      // Redirect to Google OAuth
      window.location.href = url;
    } catch (err: any) {
      console.error('Google OAuth error:', err);
      if (err.response?.data?.detail?.includes('not configured')) {
        setError('Google OAuth is not configured. Please contact administrator or use regular registration.');
      } else {
        setError('Failed to initiate Google signup. Please try again.');
      }
    } finally {
      setGoogleLoading(false);
    }
  };

  // const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  //   setUserData({
  //     ...userData,
  //     [e.target.name]: e.target.value,
  //   });
  // };

  const handleRoleChange = (e: any) => {
    setUserData({
      ...userData,
      role: e.target.value as UserRole,
    });
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `
          linear-gradient(135deg, 
            #1e3c72 0%, 
            #2a5298 25%, 
            #87ceeb 50%, 
            #98fb98 75%, 
            #f0e68c 100%
          )
        `,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: { xs: 2, sm: 3, md: 4 },
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Jammu Kashmir inspired background elements */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 15% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 85% 80%, rgba(135, 206, 235, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(152, 251, 152, 0.15) 0%, transparent 60%),
            linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.05) 50%, transparent 70%)
          `,
          zIndex: 0
        }}
      />
      
      {/* Mountain silhouette effect */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '200px',
          background: `
            linear-gradient(45deg, 
              rgba(30, 60, 114, 0.3) 0%, 
              rgba(42, 82, 152, 0.2) 30%, 
              rgba(135, 206, 235, 0.1) 70%, 
              transparent 100%
            )
          `,
          clipPath: 'polygon(0 100%, 0 60%, 20% 40%, 40% 50%, 60% 30%, 80% 45%, 100% 35%, 100% 100%)',
          zIndex: 0
        }}
      />

      <Container component="main" maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            minHeight: '100vh',
          }}
        >
        {/* Header with Logo */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            mb: 4,
          }}
        >
          <Logo size="large" showText={true} variant="vertical" />
          <Typography component="h1" variant="h4" gutterBottom sx={{ mt: 2, textAlign: 'center' }}>
            Smart Student Hub
          </Typography>
          <Typography component="h2" variant="h5" gutterBottom color="textSecondary" sx={{ textAlign: 'center' }}>
            Join our educational community
          </Typography>
        </Box>

        <Paper elevation={24} sx={{ 
          padding: { xs: 3, sm: 4, md: 5 }, 
          width: '100%',
          maxWidth: 600,
          borderRadius: 4,
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(25px)',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          boxShadow: `
            0 32px 100px rgba(30, 60, 114, 0.4),
            0 0 80px rgba(135, 206, 235, 0.2),
            0 0 40px rgba(152, 251, 152, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.6)
          `,
          position: 'relative',
          overflow: 'hidden'
        }}>
          {/* Jammu Kashmir inspired pattern */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: `
                linear-gradient(45deg, transparent 30%, rgba(30, 60, 114, 0.02) 50%, transparent 70%),
                linear-gradient(-45deg, transparent 30%, rgba(135, 206, 235, 0.03) 50%, transparent 70%),
                radial-gradient(circle at 20% 80%, rgba(152, 251, 152, 0.02) 0%, transparent 50%)
              `,
              zIndex: 0
            }}
          />

          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              position: 'relative',
              zIndex: 1
            }}
          >
            <Typography component="h2" variant="h4" gutterBottom sx={{ 
              fontWeight: 600,
              background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #87ceeb 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              textAlign: 'center',
              textShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              Create Account
            </Typography>

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

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2, width: '100%' }}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {/* Full Name */}
                <TextField
                  fullWidth
                  required
                  id="full_name"
                  label="Full Name"
                  name="full_name"
                  autoComplete="name"
                  autoFocus
                  value={userData.full_name}
                  onChange={(e) => handleFieldChange('full_name', e.target.value)}
                  onBlur={() => handleFieldBlur('full_name')}
                  disabled={loading}
                  error={fieldTouched.full_name && !!validationErrors.full_name}
                  helperText={fieldTouched.full_name && validationErrors.full_name}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person color={fieldTouched.full_name && !validationErrors.full_name && userData.full_name ? 'success' : 'action'} />
                      </InputAdornment>
                    ),
                  }}
                />

                {/* Email and Username Row */}
                <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                  <TextField
                    fullWidth
                    required
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    type="email"
                    value={userData.email}
                    onChange={(e) => handleFieldChange('email', e.target.value)}
                    onBlur={() => handleFieldBlur('email')}
                    disabled={loading}
                    error={fieldTouched.email && !!validationErrors.email}
                    helperText={fieldTouched.email && validationErrors.email}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Email color={fieldTouched.email && !validationErrors.email && userData.email ? 'success' : 'action'} />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <TextField
                    fullWidth
                    required
                    id="username"
                    label="Username"
                    name="username"
                    autoComplete="username"
                    value={userData.username}
                    onChange={(e) => handleFieldChange('username', e.target.value)}
                    onBlur={() => handleFieldBlur('username')}
                    disabled={loading}
                    error={fieldTouched.username && !!validationErrors.username}
                    helperText={fieldTouched.username && validationErrors.username}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Person color={fieldTouched.username && !validationErrors.username && userData.username ? 'success' : 'action'} />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Box>

                {/* Role and Department Row */}
                <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                  <FormControl fullWidth required>
                    <InputLabel id="role-label">Role</InputLabel>
                    <Select
                      labelId="role-label"
                      id="role"
                      value={userData.role}
                      label="Role"
                      onChange={handleRoleChange}
                      disabled={loading}
                      startAdornment={
                        <InputAdornment position="start">
                          <School color="action" />
                        </InputAdornment>
                      }
                    >
                      <MenuItem value={UserRole.STUDENT}>Student</MenuItem>
                      <MenuItem value={UserRole.TEACHER}>Teacher</MenuItem>
                    </Select>
                  </FormControl>
                  <TextField
                    fullWidth
                    id="department"
                    label="Department"
                    name="department"
                    value={userData.department}
                    onChange={(e) => handleFieldChange('department', e.target.value)}
                    disabled={loading}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <School color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Box>

                {/* Student/Employee ID and Phone Row */}
                <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                  {userData.role === UserRole.STUDENT ? (
                    <TextField
                      fullWidth
                      required
                      id="student_id"
                      label="Student ID"
                      name="student_id"
                      value={userData.student_id}
                      onChange={(e) => handleFieldChange('student_id', e.target.value)}
                      onBlur={() => handleFieldBlur('student_id')}
                      disabled={loading}
                      error={fieldTouched.student_id && !!validationErrors.student_id}
                      helperText={fieldTouched.student_id && validationErrors.student_id}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <Badge color={fieldTouched.student_id && !validationErrors.student_id && userData.student_id ? 'success' : 'action'} />
                          </InputAdornment>
                        ),
                      }}
                    />
                  ) : (
                    <TextField
                      fullWidth
                      required
                      id="employee_id"
                      label="Employee ID"
                      name="employee_id"
                      value={userData.employee_id}
                      onChange={(e) => handleFieldChange('employee_id', e.target.value)}
                      onBlur={() => handleFieldBlur('employee_id')}
                      disabled={loading}
                      error={fieldTouched.employee_id && !!validationErrors.employee_id}
                      helperText={fieldTouched.employee_id && validationErrors.employee_id}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <Badge color={fieldTouched.employee_id && !validationErrors.employee_id && userData.employee_id ? 'success' : 'action'} />
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                  <TextField
                    fullWidth
                    id="phone_number"
                    label="Phone Number"
                    name="phone_number"
                    value={userData.phone_number}
                    onChange={(e) => handleFieldChange('phone_number', e.target.value)}
                    onBlur={() => handleFieldBlur('phone_number')}
                    disabled={loading}
                    error={fieldTouched.phone_number && !!validationErrors.phone_number}
                    helperText={fieldTouched.phone_number && validationErrors.phone_number}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Phone color={fieldTouched.phone_number && !validationErrors.phone_number && userData.phone_number ? 'success' : 'action'} />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Box>

                {/* Password and Confirm Password Row */}
                <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                  <TextField
                    fullWidth
                    required
                    name="password"
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    autoComplete="new-password"
                    value={userData.password}
                    onChange={(e) => handleFieldChange('password', e.target.value)}
                    onBlur={() => handleFieldBlur('password')}
                    disabled={loading}
                    error={fieldTouched.password && !!validationErrors.password}
                    helperText={fieldTouched.password && validationErrors.password}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Lock color={fieldTouched.password && !validationErrors.password && userData.password ? 'success' : 'action'} />
                        </InputAdornment>
                      ),
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowPassword(!showPassword)}
                            edge="end"
                          >
                            {showPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />
                  <TextField
                    fullWidth
                    required
                    name="confirmPassword"
                    label="Confirm Password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => handleFieldChange('confirmPassword', e.target.value)}
                    onBlur={() => handleFieldBlur('confirmPassword')}
                    disabled={loading}
                    error={fieldTouched.confirmPassword && !!validationErrors.confirmPassword}
                    helperText={fieldTouched.confirmPassword && validationErrors.confirmPassword}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Lock color={fieldTouched.confirmPassword && !validationErrors.confirmPassword && confirmPassword ? 'success' : 'action'} />
                        </InputAdornment>
                      ),
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            edge="end"
                          >
                            {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />
                </Box>
              </Box>
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                sx={{ 
                  mt: 4, 
                  mb: 3,
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #87ceeb 100%)',
                  boxShadow: '0 8px 32px rgba(30, 60, 114, 0.4), 0 0 20px rgba(135, 206, 235, 0.2)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #1a3462 0%, #1e3c72 50%, #2a5298 100%)',
                    boxShadow: '0 12px 40px rgba(30, 60, 114, 0.5), 0 0 30px rgba(135, 206, 235, 0.3)',
                    transform: 'translateY(-2px)'
                  },
                  '&:disabled': {
                    background: '#e0e0e0',
                    color: '#9e9e9e',
                    boxShadow: 'none',
                    transform: 'none'
                  },
                  transition: 'all 0.3s ease-in-out'
                }}
                disabled={loading || !isFormValid()}
                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <CheckCircle />}
              >
                {loading ? 'Creating Account...' : 'Create Account'}
              </Button>

              <Divider sx={{ my: 3 }}>
                <Typography variant="body2" color="textSecondary">
                  OR
                </Typography>
              </Divider>

              <Button
                fullWidth
                variant="outlined"
                startIcon={<GoogleIcon />}
                onClick={handleGoogleSignup}
                disabled={googleLoading}
                size="large"
                sx={{ 
                  mb: 3,
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  borderRadius: 2,
                  borderColor: '#1976d2',
                  color: '#1976d2',
                  '&:hover': {
                    borderColor: '#1565c0',
                    backgroundColor: 'rgba(25, 118, 210, 0.04)',
                  },
                  '&:disabled': {
                    borderColor: '#e0e0e0',
                    color: '#9e9e9e',
                  }
                }}
              >
                {googleLoading ? <CircularProgress size={20} /> : 'Continue with Google'}
              </Button>
              
              <Box textAlign="center" sx={{ mt: 2 }}>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                  Already have an account?
                </Typography>
                <Link 
                  component={RouterLink} 
                  to="/login" 
                  variant="body1"
                  sx={{ 
                    fontWeight: 600,
                    textDecoration: 'none',
                    '&:hover': {
                      textDecoration: 'underline',
                    }
                  }}
                >
                  Sign In Here
                </Link>
              </Box>
            </Box>
          </Box>
        </Paper>
        </Box>
      </Container>
    </Box>
  );
};

export default RegisterPage;
