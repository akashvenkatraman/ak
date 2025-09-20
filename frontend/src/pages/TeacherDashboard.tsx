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
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  People,
  Assignment,
  CheckCircle,
  Pending,
  Visibility,
  Download,
  Comment,
  Cancel,
} from '@mui/icons-material';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { teacherApi, downloadFile, fileApi, activityLogsApi } from '../services/api';
import { TeacherDashboardStats, Activity, ActivityStatus, User, ActivityApproval, ActivityWithFiles } from '../types';
import FileManager from '../components/FileManager';
import ActivityLogs from '../components/ActivityLogs';

// Fix for Grid typing issues
const GridItem = (props: any) => <Grid {...props} />;

const TeacherDashboard: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardHome />} />
      <Route path="/students" element={<StudentsPage />} />
      <Route path="/pending" element={<PendingActivitiesPage />} />
      <Route path="/activities" element={<AllActivitiesPage />} />
      <Route path="/approvals" element={<ApprovalsPage />} />
    </Routes>
  );
};

const DashboardHome: React.FC = () => {
  const [stats, setStats] = useState<TeacherDashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const dashboardResponse = await teacherApi.getDashboard();
        setStats(dashboardResponse.data);
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

  return (
    <Box>
        <Typography variant="h4" gutterBottom>
          Teacher Dashboard
        </Typography>


      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <GridItem item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <People color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Assigned Students
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_students || 0}
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
                    Pending Approvals
                  </Typography>
                  <Typography variant="h4">
                    {stats?.pending_approvals || 0}
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
                    Activities Reviewed
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_activities_reviewed || 0}
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
                    Recent Submissions
                  </Typography>
                  <Typography variant="h4">
                    {stats?.recent_submissions?.length || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>
      </Grid>

      {/* Recent Submissions */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <GridItem item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Submissions
            </Typography>
            
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Student</TableCell>
                    <TableCell>Activity</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Submitted</TableCell>
                    <TableCell>Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {stats?.recent_submissions?.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell>
                        <Typography variant="body2" fontWeight="bold">
                          {activity.student_name}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {activity.title}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={activity.activity_type.replace('_', ' ').toUpperCase()}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={activity.status?.toUpperCase() || 'PENDING'}
                          size="small"
                          color={
                            activity.status === 'approved' ? 'success' :
                            activity.status === 'rejected' ? 'error' :
                            'warning'
                          }
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="caption" color="textSecondary">
                          {new Date(activity.created_at).toLocaleDateString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<Visibility />}
                          onClick={() => navigate('/teacher/pending')}
                        >
                          Review
                        </Button>
                      </TableCell>
                    </TableRow>
                  )) || []}
                </TableBody>
              </Table>
            </TableContainer>
            
            {(!stats?.recent_submissions || stats.recent_submissions.length === 0) && (
              <Box textAlign="center" py={4}>
                <Typography variant="body2" color="textSecondary">
                  No recent submissions
                </Typography>
              </Box>
            )}
          </Paper>
        </GridItem>
      </Grid>
    </Box>
  );
};

const StudentsPage: React.FC = () => {
  const [students, setStudents] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await teacherApi.getAssignedStudents();
        setStudents(response.data);
      } catch (error) {
        console.error('Error fetching students:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Students
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Student ID</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>Phone</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {students.map((student) => (
              <TableRow key={student.id}>
                <TableCell>{student.full_name}</TableCell>
                <TableCell>{student.email}</TableCell>
                <TableCell>{student.student_id || '-'}</TableCell>
                <TableCell>{student.department || '-'}</TableCell>
                <TableCell>{student.phone_number || '-'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {students.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No students assigned
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Contact your administrator to get students assigned to you.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

const PendingActivitiesPage: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [reviewDialog, setReviewDialog] = useState(false);
  const [filesDialog, setFilesDialog] = useState(false);
  const [reviewData, setReviewData] = useState({
    status: ActivityStatus.APPROVED,
    comments: '',
    credits_awarded: 0,
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchPendingActivities();
  }, []);

  const fetchPendingActivities = async () => {
    try {
      const response = await teacherApi.getPendingActivities();
      setActivities(response.data);
    } catch (error) {
      console.error('Error fetching pending activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReview = (activity: Activity) => {
    console.log('Reviewing activity:', activity);
    setSelectedActivity(activity);
    setReviewData({
      status: ActivityStatus.APPROVED,
      comments: '',
      credits_awarded: activity.credits,
    });
    setReviewDialog(true);
  };

  const handleViewFiles = (activity: Activity) => {
    setSelectedActivity(activity);
    setFilesDialog(true);
  };

  const handleSubmitReview = async () => {
    if (!selectedActivity) return;

    console.log('Submitting review for activity:', selectedActivity.id);
    console.log('Review data:', reviewData);
    
    // Validate form data
    if (!reviewData.status) {
      alert('Please select a decision (Approve or Reject)');
      return;
    }
    
    if (reviewData.status === ActivityStatus.APPROVED && (!reviewData.credits_awarded || reviewData.credits_awarded <= 0)) {
      alert('Please enter a valid credits amount for approval');
      return;
    }
    
    setSubmitting(true);
    try {
      // Teachers can now approve or reject activities directly
      const response = await teacherApi.approveActivity({
        activity_id: selectedActivity.id,
        status: reviewData.status,
        comments: reviewData.comments,
        credits_awarded: reviewData.credits_awarded,
      });
      
      console.log('Review submitted successfully:', response.data);
      
      // Show success message
      alert(`Activity ${reviewData.status === ActivityStatus.APPROVED ? 'approved' : 'rejected'} successfully!`);
      
      setReviewDialog(false);
      setSelectedActivity(null);
      setReviewData({
        status: ActivityStatus.PENDING,
        comments: '',
        credits_awarded: 0
      });
      await fetchPendingActivities(); // Refresh the list
    } catch (error: any) {
      console.error('Error submitting review:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to submit review';
      alert(`Error: ${errorMessage}`);
    } finally {
      setSubmitting(false);
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
      <Typography variant="h4" gutterBottom>
        Pending Activities for Review
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Student</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Credits</TableCell>
              <TableCell>Files</TableCell>
              <TableCell>Submitted</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {activities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>{activity.student_name}</TableCell>
                <TableCell>{activity.title}</TableCell>
                <TableCell>
                  {activity.activity_type.replace('_', ' ').toUpperCase()}
                </TableCell>
                <TableCell>{activity.credits}</TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Chip
                      label={activity.files_count || 0}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                    {(activity.files_count || 0) > 0 && (
                      <Tooltip title="View Files">
                        <IconButton
                          size="small"
                          onClick={() => handleViewFiles(activity)}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                </TableCell>
                <TableCell>
                  {new Date(activity.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Box display="flex" gap={1}>
                    <Button
                      variant="contained"
                      size="small"
                      startIcon={<Visibility />}
                      onClick={() => handleReview(activity)}
                    >
                      Review
                    </Button>
                    {(activity.files_count || 0) > 0 && (
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<Download />}
                        onClick={() => handleViewFiles(activity)}
                      >
                        Files
                      </Button>
                    )}
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {activities.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No pending activities
          </Typography>
          <Typography variant="body2" color="textSecondary">
            All activities have been reviewed!
          </Typography>
        </Box>
      )}

      {/* Review Dialog */}
      <Dialog open={reviewDialog} onClose={() => setReviewDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Review Activity: {selectedActivity?.title}
        </DialogTitle>
        <DialogContent>
          {selectedActivity && (
            <Box>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Student: {selectedActivity.student_name}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Type: {selectedActivity.activity_type.replace('_', ' ').toUpperCase()}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Requested Credits: {selectedActivity.credits}
              </Typography>
              {selectedActivity.description && (
                <Box mt={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Description:
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    {selectedActivity.description}
                  </Typography>
                </Box>
              )}
              
              {/* File Management */}
              <Box mt={3}>
                <Typography variant="subtitle2" gutterBottom>
                  Uploaded Files:
                </Typography>
                <FileManager
                  activityId={selectedActivity.id}
                  canUpload={false}
                  canDelete={false}
                />
              </Box>

              <Box mt={3}>
                <Typography variant="h6" gutterBottom color="primary">
                  Review Decision
                </Typography>
                
                <FormControl fullWidth margin="normal" required>
                  <InputLabel>Decision *</InputLabel>
                  <Select
                    value={reviewData.status}
                    label="Decision *"
                    onChange={(e) => setReviewData({ ...reviewData, status: e.target.value as ActivityStatus })}
                  >
                    <MenuItem value={ActivityStatus.APPROVED}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <CheckCircle color="success" />
                        <Typography>Approve Activity</Typography>
                      </Box>
                    </MenuItem>
                    <MenuItem value={ActivityStatus.REJECTED}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <Cancel color="error" />
                        <Typography>Reject Activity</Typography>
                      </Box>
                    </MenuItem>
                  </Select>
                </FormControl>

                {reviewData.status === ActivityStatus.APPROVED && (
                  <Box>
                    <Typography variant="subtitle2" gutterBottom color="success.main">
                      Performance Scoring
                    </Typography>
                    <TextField
                      fullWidth
                      margin="normal"
                      type="number"
                      label="Credits to Award *"
                      value={reviewData.credits_awarded}
                      onChange={(e) => setReviewData({ ...reviewData, credits_awarded: parseFloat(e.target.value) || 0 })}
                      inputProps={{ min: 0, step: 0.5, max: 10 }}
                      helperText="Enter performance score (0-10 credits) based on quality and effort"
                      required
                    />
                  </Box>
                )}

                {reviewData.status === ActivityStatus.REJECTED && (
                  <Alert severity="warning" sx={{ mt: 2 }}>
                    <Typography variant="body2">
                      Please provide clear feedback on why this activity was rejected so the student can improve.
                    </Typography>
                  </Alert>
                )}

                <TextField
                  fullWidth
                  margin="normal"
                  multiline
                  rows={4}
                  label="Review Comments & Feedback"
                  value={reviewData.comments}
                  onChange={(e) => setReviewData({ ...reviewData, comments: e.target.value })}
                  placeholder={
                    reviewData.status === ActivityStatus.APPROVED 
                      ? "Provide constructive feedback on the student's work. Highlight strengths and areas for improvement..."
                      : "Explain why this activity was rejected. Provide specific guidance on how the student can improve..."
                  }
                  required
                />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReviewDialog(false)} disabled={submitting}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmitReview}
            variant="contained"
            color={reviewData.status === ActivityStatus.APPROVED ? "success" : reviewData.status === ActivityStatus.REJECTED ? "error" : "primary"}
            disabled={submitting || !reviewData.status || (reviewData.status === ActivityStatus.APPROVED && (!reviewData.credits_awarded || reviewData.credits_awarded <= 0))}
            startIcon={reviewData.status === ActivityStatus.APPROVED ? <CheckCircle /> : reviewData.status === ActivityStatus.REJECTED ? <Cancel /> : <Assignment />}
          >
            {submitting 
              ? <CircularProgress size={24} />
              : reviewData.status === ActivityStatus.APPROVED 
                ? 'Approve Activity' 
                : reviewData.status === ActivityStatus.REJECTED 
                  ? 'Reject Activity' 
                  : 'Submit Review'
            }
          </Button>
        </DialogActions>
      </Dialog>

      {/* Files Dialog */}
      <Dialog
        open={filesDialog}
        onClose={() => setFilesDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Files for: {selectedActivity?.title}
        </DialogTitle>
        <DialogContent>
          {selectedActivity && (
            <Box>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Student: {selectedActivity.student_name}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Activity Type: {selectedActivity.activity_type.replace('_', ' ').toUpperCase()}
              </Typography>
              
              <Box mt={2}>
                <FileManager
                  activityId={selectedActivity.id}
                  canUpload={false}
                  canDelete={false}
                />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFilesDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const AllActivitiesPage: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [filesDialog, setFilesDialog] = useState(false);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await teacherApi.getAllActivities(
          undefined,
          filter === 'all' ? undefined : filter
        );
        setActivities(response.data);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, [filter]);

  const handleViewFiles = (activity: Activity) => {
    setSelectedActivity(activity);
    setFilesDialog(true);
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
          All Activities
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
              <TableCell>Student</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Credits</TableCell>
              <TableCell>Files</TableCell>
              <TableCell>Submitted</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {activities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>{activity.student_name}</TableCell>
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
                  <Box display="flex" alignItems="center" gap={1}>
                    <Chip
                      label={activity.files_count || 0}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                    {(activity.files_count || 0) > 0 && (
                      <Tooltip title="View Files">
                        <IconButton
                          size="small"
                          onClick={() => handleViewFiles(activity)}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                </TableCell>
                <TableCell>
                  {new Date(activity.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {(activity.files_count || 0) > 0 && (
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Download />}
                      onClick={() => handleViewFiles(activity)}
                    >
                      View Files
                    </Button>
                  )}
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
            {filter === 'all' ? 'No activities have been submitted yet.' : `No ${filter} activities found.`}
          </Typography>
        </Box>
      )}

      {/* Files Dialog */}
      <Dialog
        open={filesDialog}
        onClose={() => setFilesDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Files for: {selectedActivity?.title}
        </DialogTitle>
        <DialogContent>
          {selectedActivity && (
            <Box>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Student: {selectedActivity.student_name}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Activity Type: {selectedActivity.activity_type.replace('_', ' ').toUpperCase()}
              </Typography>
              
              <Box mt={2}>
                <FileManager
                  activityId={selectedActivity.id}
                  canUpload={false}
                  canDelete={false}
                />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFilesDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const ApprovalsPage: React.FC = () => {
  const [approvals, setApprovals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<{ status?: string; dateRange?: string }>({});

  useEffect(() => {
    const fetchApprovals = async () => {
      try {
        const response = await teacherApi.getApprovalHistory();
        setApprovals(response.data);
      } catch (error) {
        console.error('Error fetching approval history:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchApprovals();
  }, []);

  const filteredApprovals = approvals.filter(approval => {
    if (filter.status && approval.status !== filter.status) return false;
    if (filter.dateRange) {
      const approvalDate = new Date(approval.created_at);
      const now = new Date();
      const daysDiff = Math.floor((now.getTime() - approvalDate.getTime()) / (1000 * 60 * 60 * 24));
      
      switch (filter.dateRange) {
        case 'today':
          return daysDiff === 0;
        case 'week':
          return daysDiff <= 7;
        case 'month':
          return daysDiff <= 30;
        default:
          return true;
      }
    }
    return true;
  });

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Approval History
      </Typography>

      {/* Filters */}
      <Box mb={3} display="flex" gap={2} flexWrap="wrap">
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Filter by Status</InputLabel>
          <Select
            value={filter.status || ''}
            label="Filter by Status"
            onChange={(e) => setFilter({ ...filter, status: e.target.value || undefined })}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="approved">Approved</MenuItem>
            <MenuItem value="rejected">Rejected</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Date Range</InputLabel>
          <Select
            value={filter.dateRange || ''}
            label="Date Range"
            onChange={(e) => setFilter({ ...filter, dateRange: e.target.value || undefined })}
          >
            <MenuItem value="">All Time</MenuItem>
            <MenuItem value="today">Today</MenuItem>
            <MenuItem value="week">Last 7 Days</MenuItem>
            <MenuItem value="month">Last 30 Days</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Approval History Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Student</TableCell>
              <TableCell>Activity</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Decision</TableCell>
              <TableCell>Credits Awarded</TableCell>
              <TableCell>Comments</TableCell>
              <TableCell>Approved Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredApprovals.map((approval) => (
              <TableRow key={approval.id}>
                <TableCell>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">
                      {approval.student_name || 'Unknown Student'}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      ID: {approval.student_id}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">
                      {approval.activity_title || 'Unknown Activity'}
                    </Typography>
                    {approval.activity_description && (
                      <Typography variant="caption" color="textSecondary" display="block">
                        {approval.activity_description.substring(0, 50)}...
                      </Typography>
                    )}
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    label={approval.activity_type?.replace('_', ' ').toUpperCase() || 'UNKNOWN'}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={approval.status?.toUpperCase() || 'UNKNOWN'}
                    size="small"
                    color={
                      approval.status === 'approved' ? 'success' :
                      approval.status === 'rejected' ? 'error' : 'default'
                    }
                    icon={
                      approval.status === 'approved' ? <CheckCircle /> :
                      approval.status === 'rejected' ? <Cancel /> : undefined
                    }
                  />
                </TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body2" fontWeight="bold">
                      {approval.credits_awarded || 0}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      credits
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      maxWidth: 200, 
                      overflow: 'hidden', 
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}
                    title={approval.comments || 'No comments'}
                  >
                    {approval.comments || 'No comments'}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box>
                    <Typography variant="body2">
                      {new Date(approval.approved_at || approval.created_at).toLocaleDateString()}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(approval.approved_at || approval.created_at).toLocaleTimeString()}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Box display="flex" gap={1}>
                    <Tooltip title="View Details">
                      <IconButton size="small" color="primary">
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Download Files">
                      <IconButton size="small" color="secondary">
                        <Download />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {filteredApprovals.length === 0 && (
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            No approval history found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {filter.status || filter.dateRange 
              ? 'Try adjusting your filters' 
              : 'You haven\'t reviewed any activities yet'
            }
          </Typography>
        </Box>
      )}

      {/* Summary Stats */}
      {filteredApprovals.length > 0 && (
        <Box mt={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Summary Statistics
            </Typography>
            <Grid container spacing={2}>
              <GridItem item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="primary">
                    {filteredApprovals.length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Reviews
                  </Typography>
                </Box>
              </GridItem>
              <GridItem item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="success.main">
                    {filteredApprovals.filter(a => a.status === 'approved').length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Approved
                  </Typography>
                </Box>
              </GridItem>
              <GridItem item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="error.main">
                    {filteredApprovals.filter(a => a.status === 'rejected').length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Rejected
                  </Typography>
                </Box>
              </GridItem>
              <GridItem item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="warning.main">
                    {filteredApprovals.reduce((sum, a) => sum + (a.credits_awarded || 0), 0)}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Credits Awarded
                  </Typography>
                </Box>
              </GridItem>
            </Grid>
          </Paper>
        </Box>
      )}
    </Box>
  );
};

export default TeacherDashboard;
