import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add,
  Assignment,
  CheckCircle,
  Pending,
  Upload,
  Star,
  EmojiEvents,
  TrendingUp,
  School,
  Group,
} from '@mui/icons-material';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { studentApi, fileApi } from '../services/api';
import { DashboardStats, Activity, ActivityType, ActivityStatus, ActivityWithFiles } from '../types';
import FileManager from '../components/FileManager';
import ActivityLogs from '../components/ActivityLogs';
import MagicBento, { BentoCardProps } from '../components/MagicBento';

// Fix for Grid typing issues
const GridItem = (props: any) => <Grid {...props} />;

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const StudentDashboard: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardHome />} />
      <Route path="/activities" element={<ActivitiesPage />} />
      <Route path="/add-activity" element={<AddActivityPage />} />
      <Route path="/performance" element={<PerformancePage />} />
    </Routes>
  );
};

const DashboardHome: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentActivities, setRecentActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsResponse, activitiesResponse] = await Promise.all([
          studentApi.getDashboard(),
          studentApi.getActivities(),
        ]);
        
        setStats(statsResponse.data);
        setRecentActivities(activitiesResponse.data.slice(0, 5)); // Show only recent 5
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  const pieData = stats ? [
    { name: 'Approved', value: stats.approved_activities, color: '#4CAF50' },
    { name: 'Pending', value: stats.pending_activities, color: '#FF9800' },
    { name: 'Rejected', value: stats.rejected_activities, color: '#F44336' },
  ] : [];

  const getStatusColor = (status: ActivityStatus) => {
    switch (status) {
      case ActivityStatus.APPROVED:
        return 'success';
      case ActivityStatus.PENDING:
        return 'warning';
      case ActivityStatus.REJECTED:
        return 'error';
      default:
        return 'default';
    }
  };

  // Magic Bento data
  const bentoData: BentoCardProps[] = [
    {
      color: '#4CAF50',
      gradient: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
      title: 'Approved Activities',
      description: 'Your successfully approved activities',
      label: 'Success',
      icon: <CheckCircle sx={{ fontSize: 40 }} />,
      value: stats?.approved_activities || 0,
      size: 'medium',
      onClick: () => navigate('/student/activities?status=approved')
    },
    {
      color: '#FF9800',
      gradient: 'linear-gradient(135deg, #FF9800 0%, #f57c00 100%)',
      title: 'Pending Activities',
      description: 'Activities waiting for approval',
      label: 'Pending',
      icon: <Pending sx={{ fontSize: 40 }} />,
      value: stats?.pending_activities || 0,
      size: 'medium',
      onClick: () => navigate('/student/activities?status=pending')
    },
    {
      color: '#1976d2',
      gradient: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
      title: 'Total Credits',
      description: 'Credits earned from activities',
      label: 'Achievement',
      icon: <Star sx={{ fontSize: 40 }} />,
      value: stats?.total_credits || 0,
      size: 'medium',
      onClick: () => navigate('/student/performance')
    },
    {
      color: '#9C27B0',
      gradient: 'linear-gradient(135deg, #9C27B0 0%, #7b1fa2 100%)',
      title: 'Performance Score',
      description: 'Your overall performance rating',
      label: 'Excellence',
      icon: <EmojiEvents sx={{ fontSize: 40 }} />,
      value: stats?.performance_score || 0,
      size: 'medium',
      onClick: () => navigate('/student/performance')
    },
    {
      color: '#00BCD4',
      gradient: 'linear-gradient(135deg, #00BCD4 0%, #0097a7 100%)',
      title: 'Add New Activity',
      description: 'Submit a new activity for approval',
      label: 'Action',
      icon: <Add sx={{ fontSize: 40 }} />,
      size: 'large',
      onClick: () => navigate('/student/add-activity')
    },
    {
      color: '#FF5722',
      gradient: 'linear-gradient(135deg, #FF5722 0%, #d84315 100%)',
      title: 'View All Activities',
      description: 'Browse through all your activities',
      label: 'Overview',
      icon: <Assignment sx={{ fontSize: 40 }} />,
      size: 'medium',
      onClick: () => navigate('/student/activities')
    },
    {
      color: '#795548',
      gradient: 'linear-gradient(135deg, #795548 0%, #5d4037 100%)',
      title: 'Recent Activities',
      description: `Latest ${recentActivities.length} activities`,
      label: 'Recent',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      size: 'medium',
      onClick: () => navigate('/student/activities')
    },
    {
      color: '#607D8B',
      gradient: 'linear-gradient(135deg, #607D8B 0%, #455a64 100%)',
      title: 'Academic Progress',
      description: 'Track your academic journey',
      label: 'Progress',
      icon: <School sx={{ fontSize: 40 }} />,
      size: 'medium',
      onClick: () => navigate('/student/performance')
    }
  ];

  const handleCardClick = (card: BentoCardProps) => {
    if (card.onClick) {
      card.onClick();
    }
  };

  console.log('Rendering MagicBento with data:', bentoData);
  
      return (
        <MagicBento
          data={bentoData}
          enableParticles={true}
          enableGlow={true}
          enableTilt={true}
          glowColor="25, 118, 210"
          onCardClick={handleCardClick}
          title="Student Dashboard"
        />
  );
};

const ActivitiesPage: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [selectedActivity, setSelectedActivity] = useState<ActivityWithFiles | null>(null);
  const [detailsDialog, setDetailsDialog] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await studentApi.getActivities(filter === 'all' ? undefined : filter);
        setActivities(response.data);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, [filter]);

  const handleViewDetails = async (activity: Activity) => {
    setLoadingDetails(true);
    try {
      const response = await fileApi.getActivityWithFiles(activity.id);
      setSelectedActivity(response.data);
      setDetailsDialog(true);
    } catch (error) {
      console.error('Error fetching activity details:', error);
    } finally {
      setLoadingDetails(false);
    }
  };

  const getStatusColor = (status: ActivityStatus) => {
    switch (status) {
      case ActivityStatus.APPROVED:
        return 'success';
      case ActivityStatus.PENDING:
        return 'warning';
      case ActivityStatus.REJECTED:
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          My Activities
        </Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Filter</InputLabel>
          <Select
            value={filter}
            label="Filter"
            onChange={(e) => setFilter(e.target.value)}
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="approved">Approved</MenuItem>
            <MenuItem value="rejected">Rejected</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Credits</TableCell>
              <TableCell>Files</TableCell>
              <TableCell>Start Date</TableCell>
              <TableCell>End Date</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {activities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>{activity.title}</TableCell>
                <TableCell>
                  {activity.activity_type.replace('_', ' ').toUpperCase()}
                </TableCell>
                <TableCell>
                  <Chip
                    label={activity.status}
                    color={getStatusColor(activity.status) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>{activity.credits}</TableCell>
                <TableCell>
                  <Chip
                    label={activity.files_count || 0}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  {activity.start_date ? new Date(activity.start_date).toLocaleDateString() : '-'}
                </TableCell>
                <TableCell>
                  {activity.end_date ? new Date(activity.end_date).toLocaleDateString() : '-'}
                </TableCell>
                <TableCell>
                  {new Date(activity.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => handleViewDetails(activity)}
                    disabled={loadingDetails}
                  >
                    {loadingDetails ? <CircularProgress size={16} /> : 'View Details'}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {activities.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No activities found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {filter === 'all' ? 'Start by adding your first activity!' : `No ${filter} activities found.`}
          </Typography>
        </Box>
      )}

      {/* Activity Details Dialog */}
      <Dialog
        open={detailsDialog}
        onClose={() => setDetailsDialog(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          Activity Details: {selectedActivity?.title}
        </DialogTitle>
        <DialogContent>
          {selectedActivity && (
            <Box>
              <Grid container spacing={3}>
                <GridItem item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Activity Information
                  </Typography>
                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary">
                      Type: {selectedActivity.activity_type.replace('_', ' ').toUpperCase()}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Status: {selectedActivity.status}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Credits: {selectedActivity.credits}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Created: {new Date(selectedActivity.created_at).toLocaleString()}
                    </Typography>
                  </Box>
                  
                  {selectedActivity.description && (
                    <Box>
                      <Typography variant="subtitle2" gutterBottom>
                        Description:
                      </Typography>
                      <Typography variant="body2">
                        {selectedActivity.description}
                      </Typography>
                    </Box>
                  )}
                </GridItem>
                
                <GridItem item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Uploaded Files
                  </Typography>
                  <FileManager
                    activityId={selectedActivity.id}
                    canUpload={true}
                    canDelete={true}
                    onFileUploaded={() => {
                      // Refresh activity details
                      handleViewDetails(selectedActivity);
                    }}
                    onFileDeleted={() => {
                      // Refresh activity details
                      handleViewDetails(selectedActivity);
                    }}
                  />
                </GridItem>
              </Grid>
              
              <Box mt={3}>
                <Typography variant="h6" gutterBottom>
                  Activity History & Logs
                </Typography>
                <ActivityLogs activityId={selectedActivity.id} />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const AddActivityPage: React.FC = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    activity_type: ActivityType.SEMINAR,
    credits: 0,
    start_date: '',
    end_date: '',
  });
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      console.log('🚀 Starting activity submission...');
      console.log('📝 Form data:', formData);
      
      const formDataToSend = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        let processedValue = value;
        
        // Convert date fields to ISO format for backend compatibility
        if ((key === 'start_date' || key === 'end_date') && value) {
          // Convert YYYY-MM-DD to ISO format (YYYY-MM-DDTHH:MM:SSZ)
          processedValue = new Date(value + 'T00:00:00Z').toISOString();
          console.log(`📅 Converted ${key}: ${value} -> ${processedValue}`);
        }
        
        formDataToSend.append(key, processedValue.toString());
        console.log(`📋 Added to FormData: ${key} = ${processedValue}`);
      });
      
      if (file) {
        formDataToSend.append('certificate_file', file);
        console.log('📎 Added file to FormData:', file.name);
      }

      console.log('🔐 Checking authentication...');
      const token = localStorage.getItem('access_token');
      console.log('🔑 Token exists:', !!token);
      
      console.log('📤 Sending request to API...');
      const response = await studentApi.createActivity(formDataToSend);
      console.log('✅ API response:', response.data);
      
      setSuccess('Activity submitted successfully!');
      setTimeout(() => navigate('/student/activities'), 2000);
    } catch (err: any) {
      console.error('❌ Activity submission error:', err);
      console.error('❌ Error response:', err.response);
      console.error('❌ Error data:', err.response?.data);
      setError(err.response?.data?.detail || 'Failed to submit activity');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Add New Activity
      </Typography>

      <Paper sx={{ p: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <GridItem item xs={12}>
              <TextField
                required
                fullWidth
                label="Activity Title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                disabled={loading}
              />
            </GridItem>

            <GridItem item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                disabled={loading}
              />
            </GridItem>

            <GridItem item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Activity Type</InputLabel>
                <Select
                  name="activity_type"
                  value={formData.activity_type}
                  label="Activity Type"
                  onChange={(e) => setFormData({ ...formData, activity_type: e.target.value as ActivityType })}
                  disabled={loading}
                >
                  {Object.values(ActivityType).map((type) => (
                    <MenuItem key={type} value={type}>
                      {type.replace('_', ' ').toUpperCase()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </GridItem>

            <GridItem item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Credits"
                name="credits"
                value={formData.credits}
                onChange={handleChange}
                disabled={loading}
                inputProps={{ min: 0, step: 0.5 }}
              />
            </GridItem>

            <GridItem item xs={12} md={6}>
              <TextField
                fullWidth
                type="date"
                label="Start Date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                disabled={loading}
                InputLabelProps={{ shrink: true }}
              />
            </GridItem>

            <GridItem item xs={12} md={6}>
              <TextField
                fullWidth
                type="date"
                label="End Date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                disabled={loading}
                InputLabelProps={{ shrink: true }}
              />
            </GridItem>

            <GridItem item xs={12}>
              <Box>
                <Typography variant="body2" gutterBottom>
                  Upload Certificate/Document
                </Typography>
                <Button
                  variant="outlined"
                  component="label"
                  startIcon={<Upload />}
                  disabled={loading}
                >
                  Choose File
                  <input
                    type="file"
                    hidden
                    accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                  />
                </Button>
                {file && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    Selected: {file.name}
                  </Typography>
                )}
              </Box>
            </GridItem>

            <GridItem item xs={12}>
              <Box display="flex" gap={2}>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Submit Activity'}
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => navigate('/student/activities')}
                  disabled={loading}
                >
                  Cancel
                </Button>
              </Box>
            </GridItem>
          </Grid>
        </Box>
      </Paper>
    </Box>
  );
};

const PerformancePage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Academic Performance
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Performance tracking will be implemented here based on your institution's requirements.
        </Typography>
      </Paper>
    </Box>
  );
};

export default StudentDashboard;
