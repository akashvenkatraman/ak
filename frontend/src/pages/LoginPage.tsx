import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  CircularProgress,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
} from '@mui/material';
import { Google as GoogleIcon, Close as CloseIcon } from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LoginCredentials, UserRole } from '../types';
import Logo from '../components/Logo';
import api from '../services/api';

const LoginPage: React.FC = () => {
  const [credentials, setCredentials] = useState<LoginCredentials>({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [forgotPasswordOpen, setForgotPasswordOpen] = useState(false);
  const [forgotPasswordEmail, setForgotPasswordEmail] = useState('');
  const [forgotPasswordLoading, setForgotPasswordLoading] = useState(false);
  const [forgotPasswordMessage, setForgotPasswordMessage] = useState('');
  
  const { login, isAuthenticated, user, isLoading: authLoading } = useAuth();
  const navigate = useNavigate();
  // const location = useLocation();

  // const from = (location.state as any)?.from?.pathname || '/';

  useEffect(() => {
    if (isAuthenticated && user) {
      // Redirect based on user role
      const redirectPath = user.role === UserRole.ADMIN ? '/admin' :
                          user.role === UserRole.TEACHER ? '/teacher' :
                          '/student';
      navigate(redirectPath, { replace: true });
    }
  }, [isAuthenticated, user, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    console.log('🚀 Starting login process...');
    console.log('📝 Credentials:', credentials);

    // Add a timeout to prevent infinite loading
    const timeoutId = setTimeout(() => {
      if (loading) {
        console.error('⏰ Login timeout - taking too long');
        setError('Login is taking too long. Please try again.');
        setLoading(false);
      }
    }, 5000); // 5 second timeout

    try {
      console.log('📤 Calling login function...');
      const result = await login(credentials);
      console.log('✅ Login successful!', result);
      
      // Clear timeout since login succeeded
      clearTimeout(timeoutId);
      
      // Navigation will be handled by useEffect
    } catch (err: any) {
      console.error('❌ Login error:', err);
      console.error('❌ Error response:', err.response);
      console.error('❌ Error data:', err.response?.data);
      
      // Clear timeout since we got an error
      clearTimeout(timeoutId);
      
      if (err.code === 'ECONNABORTED') {
        setError('Connection timeout. Please check your internet connection and try again.');
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again in a moment.');
      } else if (err.response?.status === 401) {
        setError('Invalid username or password.');
      } else if (err.response?.status === 403) {
        setError('Account is pending approval or inactive.');
      } else if (err.message === 'Network Error') {
        setError('Cannot connect to server. Please check if the backend is running.');
      } else {
        setError(err.response?.data?.detail || err.message || 'Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleGoogleLogin = async () => {
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
        setError('Google OAuth is not configured. Please contact administrator or use regular login.');
      } else {
        setError('Failed to initiate Google login. Please try again.');
      }
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!forgotPasswordEmail) {
      setForgotPasswordMessage('Please enter your email address.');
      return;
    }

    setForgotPasswordLoading(true);
    setForgotPasswordMessage('');

    try {
      await api.post('/api/auth/forgot-password', {
        email: forgotPasswordEmail
      });
      
      setForgotPasswordMessage('If the email exists, a verification code has been sent. Check the backend console for the code if email is not configured.');
    } catch (err: any) {
      console.error('Forgot password error:', err);
      setForgotPasswordMessage('Failed to send reset email. Please try again.');
    } finally {
      setForgotPasswordLoading(false);
    }
  };

  const handleCloseForgotPassword = () => {
    setForgotPasswordOpen(false);
    setForgotPasswordEmail('');
    setForgotPasswordMessage('');
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

      {/* Main Login Container */}
      <Container 
        component="main" 
        maxWidth="sm"
        sx={{ 
          position: 'relative',
          zIndex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          py: 4
        }}
      >
        <Box
          sx={{
            width: '100%',
            maxWidth: { xs: '100%', sm: '450px', md: '500px' },
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}
        >
          <Paper 
            elevation={24} 
            sx={{ 
              padding: { xs: 3, sm: 4, md: 5 }, 
              width: '100%',
              background: 'rgba(255, 255, 255, 0.98)',
              backdropFilter: 'blur(25px)',
              border: '2px solid rgba(255, 255, 255, 0.3)',
              borderRadius: { xs: 3, sm: 4, md: 5 },
              boxShadow: `
                0 32px 100px rgba(30, 60, 114, 0.4),
                0 0 80px rgba(135, 206, 235, 0.2),
                0 0 40px rgba(152, 251, 152, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.6)
              `,
              position: 'relative',
              overflow: 'hidden'
            }}
          >
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
                position: 'relative',
                zIndex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                width: '100%'
              }}
            >
              <Logo size="large" showText={true} variant="vertical" />
              <Typography 
                component="h1" 
                variant="h4" 
                gutterBottom 
                sx={{ 
                  mt: 3, 
                  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #87ceeb 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 'bold',
                  textAlign: 'center',
                  fontSize: { xs: '1.75rem', sm: '2rem', md: '2.25rem' },
                  textShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}
              >
                Welcome Back
              </Typography>
              <Typography 
                variant="body1" 
                textAlign="center" 
                sx={{ 
                  mb: 4, 
                  color: '#2a5298', 
                  fontWeight: '500',
                  fontSize: { xs: '0.9rem', sm: '1rem' },
                  lineHeight: 1.6
                }}
              >
                Sign in to access your Smart Student Hub dashboard
              </Typography>

              {error && (
                <Alert 
                  severity="error" 
                  sx={{ 
                    width: '100%', 
                    mb: 3,
                    borderRadius: 2,
                    fontSize: { xs: '0.875rem', sm: '0.9rem' }
                  }}
                >
                  {error}
                </Alert>
              )}


              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2, width: '100%' }}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  autoComplete="username"
                  autoFocus
                  value={credentials.username}
                  onChange={handleChange}
                  disabled={loading}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                      fontSize: { xs: '0.9rem', sm: '1rem' }
                    }
                  }}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={credentials.password}
                  onChange={handleChange}
                  disabled={loading}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                      fontSize: { xs: '0.9rem', sm: '1rem' }
                    }
                  }}
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ 
                    mt: 4, 
                    mb: 3,
                    py: 1.5,
                    borderRadius: 3,
                    fontSize: { xs: '0.9rem', sm: '1rem' },
                    fontWeight: 'bold',
                    textTransform: 'none',
                    background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #87ceeb 100%)',
                    boxShadow: '0 8px 32px rgba(30, 60, 114, 0.4), 0 0 20px rgba(135, 206, 235, 0.2)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #1a3462 0%, #1e3c72 50%, #2a5298 100%)',
                      boxShadow: '0 12px 40px rgba(30, 60, 114, 0.5), 0 0 30px rgba(135, 206, 235, 0.3)',
                      transform: 'translateY(-2px)'
                    },
                    transition: 'all 0.3s ease-in-out'
                  }}
                  disabled={loading}
                >
                  {loading ? (
                    <Box display="flex" alignItems="center" gap={1}>
                      <CircularProgress size={20} color="inherit" />
                      <span>Signing in...</span>
                    </Box>
                  ) : (
                    'Sign In'
                  )}
                </Button>

                <Box textAlign="center" sx={{ mb: 3 }}>
                  <Link 
                    component="button" 
                    variant="body2" 
                    onClick={() => setForgotPasswordOpen(true)}
                    sx={{ 
                      textDecoration: 'none', 
                      cursor: 'pointer',
                      fontSize: { xs: '0.8rem', sm: '0.875rem' },
                      '&:hover': {
                        textDecoration: 'underline'
                      }
                    }}
                  >
                    Forgot Password?
                  </Link>
                </Box>

                <Divider sx={{ my: 3 }}>
                  <Typography variant="body2" color="textSecondary" sx={{ px: 2 }}>
                    OR
                  </Typography>
                </Divider>

                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<GoogleIcon />}
                  onClick={handleGoogleLogin}
                  disabled={googleLoading}
                  sx={{ 
                    mb: 3,
                    py: 1.5,
                    borderRadius: 2,
                    fontSize: { xs: '0.9rem', sm: '1rem' },
                    textTransform: 'none',
                    borderColor: '#dadce0',
                    color: '#3c4043',
                    '&:hover': {
                      borderColor: '#dadce0',
                      backgroundColor: '#f8f9fa',
                      transform: 'translateY(-1px)'
                    },
                    transition: 'all 0.2s ease-in-out'
                  }}
                >
                  {googleLoading ? <CircularProgress size={24} /> : 'Continue with Google'}
                </Button>

                <Box textAlign="center">
                  <Link 
                    component={RouterLink} 
                    to="/register" 
                    variant="body2"
                    sx={{
                      fontSize: { xs: '0.8rem', sm: '0.875rem' },
                      '&:hover': {
                        textDecoration: 'underline'
                      }
                    }}
                  >
                    {"Don't have an account? Sign Up"}
                  </Link>
                </Box>
              </Box>
            </Box>
          </Paper>
        </Box>
      </Container>

      {/* Forgot Password Dialog */}
      <Dialog open={forgotPasswordOpen} onClose={handleCloseForgotPassword} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">Reset Password</Typography>
            <IconButton onClick={handleCloseForgotPassword} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Enter your email address and we'll send you a verification code to reset your password.
          </Typography>
          
          <TextField
            fullWidth
            label="Email Address"
            type="email"
            value={forgotPasswordEmail}
            onChange={(e) => setForgotPasswordEmail(e.target.value)}
            margin="normal"
            disabled={forgotPasswordLoading}
          />
          
          {forgotPasswordMessage && (
            <Alert 
              severity={forgotPasswordMessage.includes('sent') ? 'success' : 'error'} 
              sx={{ mt: 2 }}
            >
              {forgotPasswordMessage}
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseForgotPassword} disabled={forgotPasswordLoading}>
            Cancel
          </Button>
          <Button 
            onClick={handleForgotPassword} 
            variant="contained" 
            disabled={forgotPasswordLoading}
          >
            {forgotPasswordLoading ? <CircularProgress size={24} /> : 'Send Code'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default LoginPage;
