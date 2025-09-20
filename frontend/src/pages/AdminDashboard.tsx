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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
  Checkbox,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  People,
  PersonAdd,
  Assignment,
  CheckCircle,
  Cancel,
  School,
  Delete,
} from '@mui/icons-material';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { adminApi, activityLogsApi } from '../services/api';
import { User, UserRole, UserStatus, TeacherStudentAllocation } from '../types';
import ActivityLogs from '../components/ActivityLogs';

// Fix for Grid typing issues
const GridItem = (props: any) => <Grid {...props} />;

const AdminDashboard: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardHome />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/pending" element={<PendingApprovalsPage />} />
      <Route path="/allocations" element={<StudentAllocationPage />} />
      <Route path="/activities" element={<ActivitiesPage />} />
      <Route path="/logs" element={<ActivityLogsPage />} />
    </Routes>
  );
};

const DashboardHome: React.FC = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    pendingUsers: 0,
    approvedUsers: 0,
    totalTeachers: 0,
    totalStudents: 0,
    pendingActivities: 0,
    totalActivities: 0,
  });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [allUsers, pendingUsers, teachers, students, pendingActivities, allActivities] = await Promise.all([
          adminApi.getAllUsers(),
          adminApi.getPendingUsers(),
          adminApi.getTeachers(),
          adminApi.getStudents(),
          adminApi.getPendingActivities(),
          adminApi.getAllActivities(),
        ]);

        setStats({
          totalUsers: allUsers.data.length,
          pendingUsers: pendingUsers.data.length,
          approvedUsers: allUsers.data.filter(u => u.status === UserStatus.APPROVED).length,
          totalTeachers: teachers.data.length,
          totalStudents: students.data.length,
          pendingActivities: pendingActivities.data.length,
          totalActivities: allActivities.data.length,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
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
        Admin Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <People color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Users
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalUsers}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <PersonAdd color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Pending Approval
                  </Typography>
                  <Typography variant="h4">
                    {stats.pendingUsers}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircle color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Approved Users
                  </Typography>
                  <Typography variant="h4">
                    {stats.approvedUsers}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <School color="info" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Teachers
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalTeachers}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Assignment color="secondary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Students
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalStudents}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Assignment color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Pending Activities
                  </Typography>
                  <Typography variant="h4">
                    {stats.pendingActivities}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>

        <GridItem item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircle color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Activities
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalActivities}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </GridItem>
      </Grid>

      {/* System Overview */}
      <Grid container spacing={3}>
        <GridItem item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Overview
            </Typography>
            <Box>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Platform Status: Active
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Total Registrations: {stats.totalUsers}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Active Teachers: {stats.totalTeachers}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Active Students: {stats.totalStudents}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Pending Reviews: {stats.pendingUsers}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Total Activities: {stats.totalActivities}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Pending Activities: {stats.pendingActivities}
              </Typography>
            </Box>
          </Paper>
        </GridItem>
      </Grid>
    </Box>
  );
};

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<{ role?: UserRole; status?: UserStatus }>({});

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await adminApi.getAllUsers(filter.role, filter.status);
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [filter]);

  const getStatusColor = (status: UserStatus) => {
    switch (status) {
      case UserStatus.APPROVED:
        return 'success';
      case UserStatus.PENDING:
        return 'warning';
      case UserStatus.REJECTED:
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
          User Management
        </Typography>
        <Box display="flex" gap={2}>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Role</InputLabel>
            <Select
              value={filter.role || ''}
              label="Role"
              onChange={(e) => setFilter({ ...filter, role: e.target.value as UserRole || undefined })}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value={UserRole.ADMIN}>Admin</MenuItem>
              <MenuItem value={UserRole.TEACHER}>Teacher</MenuItem>
              <MenuItem value={UserRole.STUDENT}>Student</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={filter.status || ''}
              label="Status"
              onChange={(e) => setFilter({ ...filter, status: e.target.value as UserStatus || undefined })}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value={UserStatus.PENDING}>Pending</MenuItem>
              <MenuItem value={UserStatus.APPROVED}>Approved</MenuItem>
              <MenuItem value={UserStatus.REJECTED}>Rejected</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>ID</TableCell>
              <TableCell>Registered</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.full_name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Chip
                    label={user.role.toUpperCase()}
                    variant="outlined"
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={user.status}
                    color={getStatusColor(user.status) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>{user.department || '-'}</TableCell>
                <TableCell>{user.student_id || user.employee_id || '-'}</TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {users.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No users found
          </Typography>
        </Box>
      )}
    </Box>
  );
};

const PendingApprovalsPage: React.FC = () => {
  const [pendingUsers, setPendingUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState<number | null>(null);

  useEffect(() => {
    fetchPendingUsers();
  }, []);

  const fetchPendingUsers = async () => {
    try {
      const response = await adminApi.getPendingUsers();
      setPendingUsers(response.data);
    } catch (error) {
      console.error('Error fetching pending users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApproval = async (userId: number, status: UserStatus) => {
    setProcessing(userId);
    try {
      await adminApi.approveUser({ user_id: userId, status });
      await fetchPendingUsers(); // Refresh the list
    } catch (error) {
      console.error('Error processing approval:', error);
    } finally {
      setProcessing(null);
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
        Pending User Approvals
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>ID</TableCell>
              <TableCell>Registered</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {pendingUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.full_name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Chip
                    label={user.role.toUpperCase()}
                    variant="outlined"
                    size="small"
                  />
                </TableCell>
                <TableCell>{user.department || '-'}</TableCell>
                <TableCell>{user.student_id || user.employee_id || '-'}</TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Box display="flex" gap={1}>
                    <Button
                      variant="contained"
                      color="success"
                      size="small"
                      startIcon={<CheckCircle />}
                      onClick={() => handleApproval(user.id, UserStatus.APPROVED)}
                      disabled={processing === user.id}
                    >
                      Approve
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      size="small"
                      startIcon={<Cancel />}
                      onClick={() => handleApproval(user.id, UserStatus.REJECTED)}
                      disabled={processing === user.id}
                    >
                      Reject
                    </Button>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {pendingUsers.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No pending approvals
          </Typography>
          <Typography variant="body2" color="textSecondary">
            All user registrations have been processed!
          </Typography>
        </Box>
      )}
    </Box>
  );
};

const StudentAllocationPage: React.FC = () => {
  const [teachers, setTeachers] = useState<User[]>([]);
  const [students, setStudents] = useState<User[]>([]);
  const [allocations, setAllocations] = useState<TeacherStudentAllocation[]>([]);
  const [loading, setLoading] = useState(true);
  const [allocationDialog, setAllocationDialog] = useState(false);
  const [selectedTeacher, setSelectedTeacher] = useState<number | null>(null);
  const [selectedStudents, setSelectedStudents] = useState<number[]>([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [teachersRes, studentsRes, allocationsRes] = await Promise.all([
        adminApi.getTeachers(),
        adminApi.getStudents(),
        adminApi.getAllocations(),
      ]);
      
      setTeachers(teachersRes.data);
      setStudents(studentsRes.data);
      setAllocations(allocationsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAllocateStudents = async () => {
    if (!selectedTeacher || selectedStudents.length === 0) return;

    setSubmitting(true);
    try {
      await adminApi.allocateStudents({
        teacher_id: selectedTeacher,
        student_ids: selectedStudents,
      });
      
      setAllocationDialog(false);
      setSelectedTeacher(null);
      setSelectedStudents([]);
      await fetchData(); // Refresh data
    } catch (error) {
      console.error('Error allocating students:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemoveAllocation = async (allocationId: number) => {
    try {
      await adminApi.removeAllocation(allocationId);
      await fetchData(); // Refresh data
    } catch (error) {
      console.error('Error removing allocation:', error);
    }
  };

  const handleStudentToggle = (studentId: number) => {
    setSelectedStudents(prev =>
      prev.includes(studentId)
        ? prev.filter(id => id !== studentId)
        : [...prev, studentId]
    );
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
          Student-Teacher Allocations
        </Typography>
        <Button
          variant="contained"
          startIcon={<School />}
          onClick={() => setAllocationDialog(true)}
        >
          Allocate Students
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Teacher</TableCell>
              <TableCell>Student</TableCell>
              <TableCell>Teacher Department</TableCell>
              <TableCell>Student ID</TableCell>
              <TableCell>Allocated On</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {allocations.map((allocation) => (
              <TableRow key={allocation.id}>
                <TableCell>{allocation.teacher_name}</TableCell>
                <TableCell>{allocation.student_name}</TableCell>
                <TableCell>
                  {teachers.find(t => t.id === allocation.teacher_id)?.department || '-'}
                </TableCell>
                <TableCell>
                  {students.find(s => s.id === allocation.student_id)?.student_id || '-'}
                </TableCell>
                <TableCell>
                  {new Date(allocation.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Tooltip title="Remove Allocation">
                    <IconButton
                      color="error"
                      onClick={() => handleRemoveAllocation(allocation.id)}
                    >
                      <Delete />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {allocations.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="textSecondary">
            No allocations found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Start by allocating students to teachers.
          </Typography>
        </Box>
      )}

      {/* Allocation Dialog */}
      <Dialog open={allocationDialog} onClose={() => setAllocationDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Allocate Students to Teacher</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Select Teacher</InputLabel>
            <Select
              value={selectedTeacher || ''}
              label="Select Teacher"
              onChange={(e) => setSelectedTeacher(e.target.value as number)}
            >
              {teachers.map((teacher) => (
                <MenuItem key={teacher.id} value={teacher.id}>
                  {teacher.full_name} - {teacher.department}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
            Select Students:
          </Typography>
          
          <List sx={{ maxHeight: 300, overflow: 'auto' }}>
            {students.map((student) => (
              <ListItem key={student.id}>
                <Checkbox
                  checked={selectedStudents.includes(student.id)}
                  onChange={() => handleStudentToggle(student.id)}
                />
                <ListItemText
                  primary={student.full_name}
                  secondary={`${student.student_id} - ${student.department}`}
                />
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAllocationDialog(false)} disabled={submitting}>
            Cancel
          </Button>
          <Button
            onClick={handleAllocateStudents}
            variant="contained"
            disabled={!selectedTeacher || selectedStudents.length === 0 || submitting}
          >
            {submitting ? <CircularProgress size={24} /> : 'Allocate Students'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const ActivitiesPage: React.FC = () => {
  const [activities, setActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<{ status?: string }>({});

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await adminApi.getAllActivities();
        setActivities(response.data);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  const filteredActivities = activities.filter(activity => 
    !filter.status || activity.status === filter.status
  );

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
        All Activities
      </Typography>

      {/* Filter */}
      <Box mb={3}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Filter by Status</InputLabel>
          <Select
            value={filter.status || ''}
            label="Filter by Status"
            onChange={(e) => setFilter({ ...filter, status: e.target.value || undefined })}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="approved">Approved</MenuItem>
            <MenuItem value="rejected">Rejected</MenuItem>
            <MenuItem value="under_review">Under Review</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Activities Table */}
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
              <TableCell>Created</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredActivities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">
                      {activity.student_name}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {activity.student_email}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontWeight="bold">
                    {activity.title}
                  </Typography>
                  {activity.description && (
                    <Typography variant="caption" color="textSecondary">
                      {activity.description.substring(0, 100)}...
                    </Typography>
                  )}
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
                    label={activity.status.toUpperCase()}
                    size="small"
                    color={
                      activity.status === 'approved' ? 'success' :
                      activity.status === 'rejected' ? 'error' :
                      activity.status === 'pending' ? 'warning' : 'default'
                    }
                  />
                </TableCell>
                <TableCell>{activity.credits}</TableCell>
                <TableCell>
                  <Chip
                    label={activity.files_count || 0}
                    size="small"
                    color="info"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  {new Date(activity.created_at).toLocaleDateString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {filteredActivities.length === 0 && (
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            No activities found
          </Typography>
        </Box>
      )}
    </Box>
  );
};

const ActivityLogsPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Activity Logs
      </Typography>
      <ActivityLogs isAdmin={true} />
    </Box>
  );
};

export default AdminDashboard;
