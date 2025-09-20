import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Avatar,
  Button,
  TextField,
  Divider,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Snackbar,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  InputAdornment,
  Tooltip,
  Fade
} from '@mui/material';
import {
  Edit,
  Save,
  Cancel,
  PhotoCamera,
  Delete,
  Person,
  Email,
  Phone,
  LocationOn,
  Work,
  School,
  CalendarToday,
  LinkedIn,
  Twitter,
  Web,
  Lock,
  Visibility,
  VisibilityOff,
  Info
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';
import { profileApi } from '../services/api';

interface ProfileData {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: string;
  status: string;
  phone_number?: string;
  department?: string;
  student_id?: string;
  employee_id?: string;
  performance_score?: number;
  total_credits_earned?: number;
  profile_picture?: string;
  bio?: string;
  date_of_birth?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  linkedin_url?: string;
  twitter_url?: string;
  website_url?: string;
  created_at: string;
  updated_at?: string;
}

interface PasswordData {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

const ProfilePage: React.FC = () => {
  const { updateUser } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editing, setEditing] = useState(false);
  const [passwordDialogOpen, setPasswordDialogOpen] = useState(false);
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  
  const [formData, setFormData] = useState<Partial<ProfileData>>({});
  const [passwordData, setPasswordData] = useState<PasswordData>({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  const fetchProfile = useCallback(async () => {
    try {
      const response = await profileApi.getProfile();
      setProfile(response.data);
      setFormData(response.data);
      
      // Update auth context with the latest profile data
      updateUser({
        full_name: response.data.full_name,
        email: response.data.email,
        phone_number: response.data.phone_number,
        department: response.data.department,
        student_id: response.data.student_id,
        employee_id: response.data.employee_id,
        performance_score: response.data.performance_score,
        total_credits_earned: response.data.total_credits_earned,
        profile_picture: response.data.profile_picture,
        bio: response.data.bio,
        date_of_birth: response.data.date_of_birth,
        address: response.data.address,
        city: response.data.city,
        state: response.data.state,
        country: response.data.country,
        postal_code: response.data.postal_code,
        linkedin_url: response.data.linkedin_url,
        twitter_url: response.data.twitter_url,
        website_url: response.data.website_url,
        updated_at: response.data.updated_at
      });
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setSnackbar({ open: true, message: 'Failed to load profile', severity: 'error' });
      setLoading(false);
    }
  }, [updateUser]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const handleEdit = () => {
    setEditing(true);
    // Ensure formData includes all current profile data, especially profile_picture
    setFormData(profile ? { ...profile } : {});
  };

  const handleCancel = () => {
    setEditing(false);
    setFormData(profile || {});
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      
      const response = await profileApi.updateProfile(formData);
      
      // Update profile state with the response
      setProfile(response.data);
      
      // Update auth context with the new profile data
      updateUser({
        full_name: response.data.full_name,
        email: response.data.email,
        phone_number: response.data.phone_number,
        department: response.data.department,
        student_id: response.data.student_id,
        employee_id: response.data.employee_id,
        performance_score: response.data.performance_score,
        total_credits_earned: response.data.total_credits_earned,
        profile_picture: response.data.profile_picture,
        bio: response.data.bio,
        date_of_birth: response.data.date_of_birth,
        address: response.data.address,
        city: response.data.city,
        state: response.data.state,
        country: response.data.country,
        postal_code: response.data.postal_code,
        linkedin_url: response.data.linkedin_url,
        twitter_url: response.data.twitter_url,
        website_url: response.data.website_url,
        updated_at: response.data.updated_at
      });
      
      setEditing(false);
      setSnackbar({ open: true, message: 'Profile updated successfully', severity: 'success' });
    } catch (error: any) {
      console.error('Error updating profile:', error);
      setSnackbar({ 
        open: true, 
        message: error.response?.data?.detail || 'Failed to update profile', 
        severity: 'error' 
      });
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async () => {
    try {
      setSaving(true);
      await profileApi.changePassword(passwordData);
      setPasswordDialogOpen(false);
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
      setSnackbar({ open: true, message: 'Password changed successfully', severity: 'success' });
    } catch (error: any) {
      console.error('Error changing password:', error);
      setSnackbar({ 
        open: true, 
        message: error.response?.data?.detail || 'Failed to change password', 
        severity: 'error' 
      });
    } finally {
      setSaving(false);
    }
  };

  const handleProfilePictureUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setSaving(true);
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await profileApi.uploadProfilePicture(formData);
      const newProfilePictureUrl = response.data.profile_picture;
      
      // Update both profile and formData states to keep them in sync
      setProfile(prev => prev ? { ...prev, profile_picture: newProfilePictureUrl } : null);
      setFormData(prev => ({ ...prev, profile_picture: newProfilePictureUrl }));
      
      // Update auth context with the new profile picture
      updateUser({ profile_picture: newProfilePictureUrl });
      
      setSnackbar({ open: true, message: 'Profile picture updated successfully', severity: 'success' });
    } catch (error: any) {
      console.error('Error uploading profile picture:', error);
      setSnackbar({ 
        open: true, 
        message: error.response?.data?.detail || 'Failed to upload profile picture', 
        severity: 'error' 
      });
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteProfilePicture = async () => {
    try {
      setSaving(true);
      await profileApi.deleteProfilePicture();
      
      // Update both profile and formData states to keep them in sync
      setProfile(prev => prev ? { ...prev, profile_picture: undefined } : null);
      setFormData(prev => ({ ...prev, profile_picture: undefined }));
      
      // Update auth context to remove the profile picture
      updateUser({ profile_picture: undefined });
      
      setSnackbar({ open: true, message: 'Profile picture deleted successfully', severity: 'success' });
    } catch (error: any) {
      console.error('Error deleting profile picture:', error);
      setSnackbar({ 
        open: true, 
        message: error.response?.data?.detail || 'Failed to delete profile picture', 
        severity: 'error' 
      });
    } finally {
      setSaving(false);
    }
  };

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handlePasswordInputChange = (field: keyof PasswordData, value: string) => {
    setPasswordData(prev => ({ ...prev, [field]: value }));
  };

  const togglePasswordVisibility = (field: 'current' | 'new' | 'confirm') => {
    setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }));
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin': return 'error';
      case 'teacher': return 'primary';
      case 'student': return 'success';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'success';
      case 'pending': return 'warning';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!profile) {
    return (
      <Container maxWidth="md">
        <Alert severity="error">Failed to load profile data</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              Profile Management
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage your personal information and account settings
            </Typography>
          </Box>
          <Box>
            {!editing ? (
              <Button
                variant="contained"
                startIcon={<Edit />}
                onClick={handleEdit}
                disabled={saving}
                size="large"
                sx={{ minWidth: 140 }}
              >
                Edit Profile
              </Button>
            ) : (
              <Box display="flex" gap={2}>
                <Button
                  variant="contained"
                  startIcon={saving ? <CircularProgress size={20} /> : <Save />}
                  onClick={handleSave}
                  disabled={saving}
                  size="large"
                  sx={{ minWidth: 140 }}
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Cancel />}
                  onClick={handleCancel}
                  disabled={saving}
                  size="large"
                  sx={{ minWidth: 100 }}
                >
                  Cancel
                </Button>
              </Box>
            )}
          </Box>
        </Box>

        <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={4}>
          {/* Profile Picture Section */}
          <Box flex={{ xs: '1', md: '0 0 33.333%' }}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box position="relative" display="inline-block">
                  <Box position="relative">
                    <Avatar
                      src={profile.profile_picture ? `http://localhost:8000${profile.profile_picture}` : undefined}
                      sx={{ 
                        width: 120, 
                        height: 120, 
                        mx: 'auto', 
                        mb: 2,
                        opacity: saving ? 0.7 : 1,
                        transition: 'opacity 0.3s ease'
                      }}
                    >
                      {!profile.profile_picture && <Person sx={{ fontSize: 60 }} />}
                    </Avatar>
                    {saving && (
                      <Box
                        sx={{
                          position: 'absolute',
                          top: '50%',
                          left: '50%',
                          transform: 'translate(-50%, -50%)',
                          zIndex: 1
                        }}
                      >
                        <CircularProgress size={30} />
                      </Box>
                    )}
                  </Box>
                  <Box sx={{ position: 'absolute', bottom: 0, right: 0 }}>
                    <input
                      accept="image/*"
                      style={{ display: 'none' }}
                      id="profile-picture-upload"
                      type="file"
                      onChange={handleProfilePictureUpload}
                    />
                    <Tooltip title="Upload Profile Picture" arrow>
                      <label htmlFor="profile-picture-upload">
                        <IconButton
                          color="primary"
                          component="span"
                          disabled={saving}
                          sx={{ 
                            bgcolor: 'primary.main', 
                            color: 'white',
                            '&:hover': { bgcolor: 'primary.dark' },
                            boxShadow: 2,
                            transition: 'all 0.2s ease-in-out'
                          }}
                          size="small"
                        >
                          <PhotoCamera />
                        </IconButton>
                      </label>
                    </Tooltip>
                  </Box>
                  {profile.profile_picture && (
                    <Box sx={{ position: 'absolute', bottom: 0, left: 0 }}>
                      <Tooltip title="Delete Profile Picture" arrow>
                        <IconButton
                          color="error"
                          onClick={handleDeleteProfilePicture}
                          disabled={saving}
                          sx={{ 
                            bgcolor: 'error.main', 
                            color: 'white',
                            '&:hover': { bgcolor: 'error.dark' },
                            boxShadow: 2,
                            transition: 'all 0.2s ease-in-out'
                          }}
                          size="small"
                        >
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  )}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {profile.full_name}
                </Typography>
                <Box mb={2}>
                  <Chip
                    label={profile.role.toUpperCase()}
                    color={getRoleColor(profile.role)}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  <Chip
                    label={profile.status.toUpperCase()}
                    color={getStatusColor(profile.status)}
                    size="small"
                  />
                </Box>
                {profile.bio && (
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {profile.bio}
                  </Typography>
                )}
                <Box sx={{ 
                  bgcolor: 'info.light', 
                  p: 2, 
                  borderRadius: 1, 
                  border: '1px solid', 
                  borderColor: 'info.main',
                  mb: 2
                }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <Info color="info" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="subtitle2" color="info.dark">
                      Profile Picture Tips
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="info.dark" display="block">
                    • Supported formats: JPEG, PNG, GIF, WebP
                  </Typography>
                  <Typography variant="caption" color="info.dark" display="block">
                    • Maximum file size: 5MB
                  </Typography>
                  <Typography variant="caption" color="info.dark" display="block">
                    • Recommended size: 400x400 pixels
                  </Typography>
                </Box>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center' }}>
                <Button
                  variant="outlined"
                  startIcon={<Lock />}
                  onClick={() => setPasswordDialogOpen(true)}
                  disabled={saving}
                >
                  Change Password
                </Button>
              </CardActions>
            </Card>
          </Box>

          {/* Profile Details Section */}
          <Box flex={{ xs: '1', md: '0 0 66.666%' }}>
            <Box display="flex" flexDirection="column" gap={3}>
              {/* Basic Information */}
              <Box sx={{ 
                bgcolor: editing ? 'action.hover' : 'transparent', 
                p: editing ? 2 : 0, 
                borderRadius: 1,
                transition: 'all 0.3s ease-in-out'
              }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Basic Information
                  </Typography>
                  {editing && (
                    <Fade in={editing}>
                      <Chip 
                        icon={<Edit />} 
                        label="Editing" 
                        color="primary" 
                        size="small" 
                        variant="outlined"
                      />
                    </Fade>
                  )}
                </Box>
                <Divider sx={{ mb: 2 }} />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="Full Name"
                  value={editing ? formData.full_name || '' : profile.full_name}
                  onChange={(e) => handleInputChange('full_name', e.target.value)}
                  disabled={!editing}
                  variant={editing ? "outlined" : "filled"}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person color={editing ? "primary" : "action"} />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={editing ? formData.email || '' : profile.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  disabled={!editing}
                  variant={editing ? "outlined" : "filled"}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Email color={editing ? "primary" : "action"} />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="Username"
                  value={profile.username}
                  disabled
                  variant="filled"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person color="action" />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Phone Number"
                  value={editing ? formData.phone_number || '' : profile.phone_number || ''}
                  onChange={(e) => handleInputChange('phone_number', e.target.value)}
                  disabled={!editing}
                  variant={editing ? "outlined" : "filled"}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Phone color={editing ? "primary" : "action"} />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="Department"
                  value={editing ? formData.department || '' : profile.department || ''}
                  onChange={(e) => handleInputChange('department', e.target.value)}
                  disabled={!editing}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Work />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label={profile.role === 'student' ? 'Student ID' : 'Employee ID'}
                  value={editing ? (formData.student_id || formData.employee_id || '') : (profile.student_id || profile.employee_id || '')}
                  onChange={(e) => handleInputChange(profile.role === 'student' ? 'student_id' : 'employee_id', e.target.value)}
                  disabled={!editing}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <School />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              {/* Personal Information */}
              <Box sx={{ 
                bgcolor: editing ? 'action.hover' : 'transparent', 
                p: editing ? 2 : 0, 
                borderRadius: 1,
                transition: 'all 0.3s ease-in-out'
              }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Personal Information
                  </Typography>
                  {editing && (
                    <Fade in={editing}>
                      <Chip 
                        icon={<Edit />} 
                        label="Editing" 
                        color="primary" 
                        size="small" 
                        variant="outlined"
                      />
                    </Fade>
                  )}
                </Box>
                <Divider sx={{ mb: 2 }} />
              </Box>

              <Box>
                <TextField
                  fullWidth
                  label="Bio"
                  multiline
                  rows={3}
                  value={editing ? formData.bio || '' : profile.bio || ''}
                  onChange={(e) => handleInputChange('bio', e.target.value)}
                  disabled={!editing}
                  placeholder="Tell us about yourself..."
                />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="Date of Birth"
                  type="date"
                  value={editing ? (formData.date_of_birth ? formData.date_of_birth.split('T')[0] : '') : (profile.date_of_birth ? profile.date_of_birth.split('T')[0] : '')}
                  onChange={(e) => handleInputChange('date_of_birth', e.target.value ? new Date(e.target.value).toISOString() : '')}
                  disabled={!editing}
                  InputLabelProps={{ shrink: true }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <CalendarToday />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              {/* Address Information */}
              <Box sx={{ 
                bgcolor: editing ? 'action.hover' : 'transparent', 
                p: editing ? 2 : 0, 
                borderRadius: 1,
                transition: 'all 0.3s ease-in-out'
              }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Address Information
                  </Typography>
                  {editing && (
                    <Fade in={editing}>
                      <Chip 
                        icon={<Edit />} 
                        label="Editing" 
                        color="primary" 
                        size="small" 
                        variant="outlined"
                      />
                    </Fade>
                  )}
                </Box>
                <Divider sx={{ mb: 2 }} />
              </Box>

              <Box>
                <TextField
                  fullWidth
                  label="Address"
                  multiline
                  rows={2}
                  value={editing ? formData.address || '' : profile.address || ''}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  disabled={!editing}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LocationOn />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="City"
                  value={editing ? formData.city || '' : profile.city || ''}
                  onChange={(e) => handleInputChange('city', e.target.value)}
                  disabled={!editing}
                />
                <TextField
                  fullWidth
                  label="State"
                  value={editing ? formData.state || '' : profile.state || ''}
                  onChange={(e) => handleInputChange('state', e.target.value)}
                  disabled={!editing}
                />
                <TextField
                  fullWidth
                  label="Country"
                  value={editing ? formData.country || '' : profile.country || ''}
                  onChange={(e) => handleInputChange('country', e.target.value)}
                  disabled={!editing}
                />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="Postal Code"
                  value={editing ? formData.postal_code || '' : profile.postal_code || ''}
                  onChange={(e) => handleInputChange('postal_code', e.target.value)}
                  disabled={!editing}
                />
              </Box>

              {/* Social Links */}
              <Box sx={{ 
                bgcolor: editing ? 'action.hover' : 'transparent', 
                p: editing ? 2 : 0, 
                borderRadius: 1,
                transition: 'all 0.3s ease-in-out'
              }}>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Social Links
                  </Typography>
                  {editing && (
                    <Fade in={editing}>
                      <Chip 
                        icon={<Edit />} 
                        label="Editing" 
                        color="primary" 
                        size="small" 
                        variant="outlined"
                      />
                    </Fade>
                  )}
                </Box>
                <Divider sx={{ mb: 2 }} />
              </Box>

              <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2}>
                <TextField
                  fullWidth
                  label="LinkedIn"
                  value={editing ? formData.linkedin_url || '' : profile.linkedin_url || ''}
                  onChange={(e) => handleInputChange('linkedin_url', e.target.value)}
                  disabled={!editing}
                  placeholder="https://linkedin.com/in/username"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LinkedIn />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Twitter"
                  value={editing ? formData.twitter_url || '' : profile.twitter_url || ''}
                  onChange={(e) => handleInputChange('twitter_url', e.target.value)}
                  disabled={!editing}
                  placeholder="https://twitter.com/username"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Twitter />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Website"
                  value={editing ? formData.website_url || '' : profile.website_url || ''}
                  onChange={(e) => handleInputChange('website_url', e.target.value)}
                  disabled={!editing}
                  placeholder="https://yourwebsite.com"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Web />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>
            </Box>
          </Box>
        </Box>
      </Paper>

      {/* Password Change Dialog */}
      <Dialog open={passwordDialogOpen} onClose={() => setPasswordDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Change Password</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} sx={{ mt: 1 }}>
            <TextField
              fullWidth
              label="Current Password"
              type={showPasswords.current ? 'text' : 'password'}
              value={passwordData.current_password}
              onChange={(e) => handlePasswordInputChange('current_password', e.target.value)}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => togglePasswordVisibility('current')}>
                      {showPasswords.current ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <TextField
              fullWidth
              label="New Password"
              type={showPasswords.new ? 'text' : 'password'}
              value={passwordData.new_password}
              onChange={(e) => handlePasswordInputChange('new_password', e.target.value)}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => togglePasswordVisibility('new')}>
                      {showPasswords.new ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <TextField
              fullWidth
              label="Confirm New Password"
              type={showPasswords.confirm ? 'text' : 'password'}
              value={passwordData.confirm_password}
              onChange={(e) => handlePasswordInputChange('confirm_password', e.target.value)}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => togglePasswordVisibility('confirm')}>
                      {showPasswords.confirm ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPasswordDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handlePasswordChange}
            variant="contained"
            disabled={saving || !passwordData.current_password || !passwordData.new_password || passwordData.new_password !== passwordData.confirm_password}
          >
            {saving ? <CircularProgress size={20} /> : 'Change Password'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ProfilePage;
