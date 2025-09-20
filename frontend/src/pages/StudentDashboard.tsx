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
} from '@mui/icons-material';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { studentApi, fileApi } from '../services/api';
import { DashboardStats, Activity, ActivityType, ActivityStatus, ActivityWithFiles } from '../types';
import FileManager from '../components/FileManager';
import ActivityLogs from '../components/ActivityLogs';

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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Student Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Assignment color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Activities
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_activities || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircle color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Approved
                  </Typography>
                  <Typography variant="h4">
                    {stats?.approved_activities || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Pending color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Pending Review
                  </Typography>
                  <Typography variant="h4">
                    {stats?.pending_activities || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Assignment color="secondary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Credits
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_credits || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Star color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Performance Score
                  </Typography>
                  <Typography variant="h4">
                    {stats?.performance_score || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <EmojiEvents color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Credits Earned
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_credits_earned || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>
      </Grid>

      <Grid container spacing={3}>
        {/* Activity Status Chart */}
        <GridItem item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Activity Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </GridItem>

        {/* Recent Activities */}
        <GridItem item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">
                Recent Activities
              </Typography>
              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={() => navigate('/student/add-activity')}
              >
                Add Activity
              </Button>
            </Box>
            
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Credits</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recentActivities.map((activity) => (
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
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            
            {recentActivities.length === 0 && (
              <Typography variant="body2" color="textSecondary" textAlign="center" sx={{ mt: 2 }}>
                No activities yet. Start by adding your first activity!
              </Typography>
            )}
          </Paper>
        </GridItem>

        {/* Performance Summary */}
        {(stats?.gpa || stats?.attendance_percentage) && (
          <GridItem item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Academic Performance
              </Typography>
              <Grid container spacing={3}>
                {stats.gpa && (
                  <GridItem item xs={12} sm={6}>
                    <Box textAlign="center">
                      <Typography variant="h3" color="primary">
                        {stats.gpa.toFixed(2)}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Current GPA
                      </Typography>
                    </Box>
                  </GridItem>
                )}
                {stats.attendance_percentage && (
                  <GridItem item xs={12} sm={6}>
                    <Box textAlign="center">
                      <Typography variant="h3" color="primary">
                        {stats.attendance_percentage.toFixed(1)}%
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Attendance
                      </Typography>
                    </Box>
                  </GridItem>
                )}
              </Grid>
            </Paper>
          </GridItem>
        )}
      </Grid>
    </Box>
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
      const formDataToSend = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        formDataToSend.append(key, value.toString());
      });
      
      if (file) {
        formDataToSend.append('certificate_file', file);
      }

      await studentApi.createActivity(formDataToSend);
      setSuccess('Activity submitted successfully!');
      setTimeout(() => navigate('/student/activities'), 2000);
    } catch (err: any) {
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
