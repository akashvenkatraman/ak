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
  
  const { login, isAuthenticated, user } = useAuth();
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

    try {
      await login(credentials);
      // Navigation will be handled by useEffect
    } catch (err: any) {
      console.error('Login error:', err);
      if (err.code === 'ECONNABORTED') {
        setError('Connection timeout. Please check your internet connection and try again.');
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again in a moment.');
      } else if (err.response?.status === 401) {
        setError('Invalid username or password.');
      } else if (err.response?.status === 403) {
        setError('Account is pending approval or inactive.');
      } else {
        setError(err.response?.data?.detail || 'Login failed. Please try again.');
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
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
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
            <Logo size="large" showText={true} variant="vertical" />
            <Typography component="h2" variant="h5" gutterBottom sx={{ mt: 2 }}>
              Welcome Back
            </Typography>
            <Typography variant="body2" color="textSecondary" textAlign="center" sx={{ mb: 3 }}>
              Sign in to access your Smart Student Hub dashboard
            </Typography>

            {error && (
              <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
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
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Sign In'}
              </Button>

              <Box textAlign="center" sx={{ mb: 2 }}>
                <Link 
                  component="button" 
                  variant="body2" 
                  onClick={() => setForgotPasswordOpen(true)}
                  sx={{ textDecoration: 'none', cursor: 'pointer' }}
                >
                  Forgot Password?
                </Link>
              </Box>

              <Divider sx={{ my: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  OR
                </Typography>
              </Divider>

              <Button
                fullWidth
                variant="outlined"
                startIcon={<GoogleIcon />}
                onClick={handleGoogleLogin}
                disabled={googleLoading}
                sx={{ mb: 2 }}
              >
                {googleLoading ? <CircularProgress size={24} /> : 'Continue with Google'}
              </Button>

              <Box textAlign="center">
                <Link component={RouterLink} to="/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Box>

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
    </Container>
  );
};

export default LoginPage;
