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
  CircularProgress,
  IconButton,
  Tooltip,
  Checkbox,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  People,
  PersonAdd,
  Assignment,
  CheckCircle,
  Cancel,
  School,
  Delete,
  AdminPanelSettings,
  Group,
  TrendingUp,
  Assessment,
  History,
  Security,
  Analytics,
  Settings,
  Dashboard,
  Refresh,
  Download,
  TableChart,
} from '@mui/icons-material';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { adminApi } from '../services/api';
import { User, UserRole, UserStatus, TeacherStudentAllocation } from '../types';
import ActivityLogs from '../components/ActivityLogs';
import MagicBento, { BentoCardProps } from '../components/MagicBento';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import ErrorDialog from '../components/ErrorDialog';
import PendingReviewsBackground from '../components/PendingReviewsBackground';
import GlassPendingReviewsUI from '../components/GlassPendingReviewsUI';
import { getErrorAction } from '../utils/errorHandler';
import './AdminDashboard.css';

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
      <Route path="/analytics" element={<AnalyticsDashboard />} />
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
    lastUpdated: null as Date | null,
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<any>(null);
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const navigate = useNavigate();

  const fetchStats = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      
      console.log('🔄 Fetching dashboard stats...');
      const [allUsers, pendingUsers, teachers, students, pendingActivities, allActivities] = await Promise.all([
        adminApi.getAllUsers(),
        adminApi.getPendingUsers(),
        adminApi.getTeachers(),
        adminApi.getStudents(),
        adminApi.getPendingActivities(),
        adminApi.getAllActivities(),
      ]);

      console.log('📊 Raw API responses:');
      console.log('  - All Users:', allUsers.data.length);
      console.log('  - Pending Users:', pendingUsers.data.length);
      console.log('  - Teachers:', teachers.data.length);
      console.log('  - Students:', students.data.length);
      console.log('  - Pending Activities:', pendingActivities.data.length);
      console.log('  - All Activities:', allActivities.data.length);

      const newStats = {
        totalUsers: allUsers.data.length,
        pendingUsers: pendingUsers.data.length,
        approvedUsers: allUsers.data.filter(u => u.status === UserStatus.APPROVED).length,
        totalTeachers: teachers.data.length,
        totalStudents: students.data.length,
        pendingActivities: pendingActivities.data.length,
        totalActivities: allActivities.data.length,
        lastUpdated: new Date(),
      };

      setStats(newStats);
      setError(null); // Clear any previous errors
      console.log('📊 Dashboard stats updated:', newStats);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setError(error);
      setShowErrorDialog(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
    
    // Refresh data every 30 seconds for real-time updates
    const interval = setInterval(() => fetchStats(true), 30000);
    
    return () => clearInterval(interval);
  }, []);

  // Export handler functions - Updated to use sample data endpoints (no auth required)
  const handleExportTeachers = async () => {
    try {
      const response = await adminApi.exportTeachersSampleData();
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `teachers_performance_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting teachers data:', error);
      alert('Failed to export teachers data. Please try again.');
    }
  };

  const handleExportStudents = async () => {
    try {
      const response = await adminApi.exportStudentsSampleData();
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `students_performance_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting students data:', error);
      alert('Failed to export students data. Please try again.');
    }
  };

  const handleExportComprehensive = async () => {
    try {
      const response = await adminApi.exportOverallSampleData();
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `overall_metrics_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting comprehensive data:', error);
      alert('Failed to export comprehensive data. Please try again.');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  // Magic Bento data for Admin Dashboard
  const bentoData: BentoCardProps[] = [
    {
      color: '#4CAF50',
      gradient: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
      title: 'Total Users',
      description: 'All registered users in the system',
      label: 'Users',
      icon: <People sx={{ fontSize: 40 }} />,
      value: stats.totalUsers,
      size: 'medium',
      onClick: () => navigate('/admin/users')
    },
    {
      color: '#FF9800',
      gradient: 'linear-gradient(135deg, #FF9800 0%, #f57c00 100%)',
      title: 'Pending Approvals',
      description: 'Users waiting for approval',
      label: 'Pending',
      icon: <PersonAdd sx={{ fontSize: 40 }} />,
      value: stats.pendingUsers,
      size: 'medium',
      onClick: () => navigate('/admin/pending')
    },
    {
      color: '#1976d2',
      gradient: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
      title: 'Approved Users',
      description: 'Successfully approved users',
      label: 'Approved',
      icon: <CheckCircle sx={{ fontSize: 40 }} />,
      value: stats.approvedUsers,
      size: 'medium',
      onClick: () => navigate('/admin/users')
    },
    {
      color: '#9C27B0',
      gradient: 'linear-gradient(135deg, #9C27B0 0%, #7b1fa2 100%)',
      title: 'Teachers',
      description: 'Total number of teachers',
      label: 'Teachers',
      icon: <School sx={{ fontSize: 40 }} />,
      value: stats.totalTeachers,
      size: 'medium',
      onClick: () => navigate('/admin/users')
    },
    {
      color: '#00BCD4',
      gradient: 'linear-gradient(135deg, #00BCD4 0%, #0097a7 100%)',
      title: 'Student Allocations',
      description: 'Manage student-teacher assignments',
      label: 'Allocate',
      icon: <Group sx={{ fontSize: 40 }} />,
      size: 'large',
      onClick: () => navigate('/admin/allocations')
    },
    {
      color: '#FF5722',
      gradient: 'linear-gradient(135deg, #FF5722 0%, #d84315 100%)',
      title: 'All Activities',
      description: 'View all student activities',
      label: 'Activities',
      icon: <Assignment sx={{ fontSize: 40 }} />,
      value: stats.totalActivities,
      size: 'medium',
      onClick: () => navigate('/admin/activities')
    },
    {
      color: '#795548',
      gradient: 'linear-gradient(135deg, #795548 0%, #5d4037 100%)',
      title: 'System Logs',
      description: 'Monitor system activity logs',
      label: 'Logs',
      icon: <History sx={{ fontSize: 40 }} />,
      size: 'medium',
      onClick: () => navigate('/admin/logs')
    },
    {
      color: '#607D8B',
      gradient: 'linear-gradient(135deg, #607D8B 0%, #455a64 100%)',
      title: 'System Analytics',
      description: 'Platform performance metrics',
      label: 'Analytics',
      icon: <Analytics sx={{ fontSize: 40 }} />,
      size: 'medium',
      onClick: () => navigate('/admin/users')
    }
  ];

  const handleCardClick = (card: BentoCardProps) => {
    if (card.onClick) {
      card.onClick();
    }
  };

  console.log('Rendering Admin MagicBento with data:', bentoData);

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Admin Dashboard
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          {stats.lastUpdated && (
            <Typography variant="body2" color="textSecondary">
              Last updated: {stats.lastUpdated.toLocaleTimeString()}
            </Typography>
          )}
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={() => fetchStats(true)}
            disabled={refreshing}
            sx={{ minWidth: 120 }}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </Button>
        </Box>
      </Box>
      
      {/* Data Export Section */}
      <Box 
        sx={{ 
          mb: 4, 
          p: 3, 
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(20px)',
          borderRadius: 2,
          border: '1px solid rgba(255, 255, 255, 0.3)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
        }}
      >
        <Typography variant="h6" sx={{ color: '#333', mb: 2, fontWeight: 'bold' }}>
          📊 Data Export
        </Typography>
        <Typography variant="body2" sx={{ color: '#666', mb: 3 }}>
          Download comprehensive data reports for teachers, students, and system activities
        </Typography>
        <Box display="flex" gap={2} flexWrap="wrap">
        <Button
          variant="contained"
          startIcon={<Download />}
          onClick={() => handleExportTeachers()}
          disabled={refreshing}
          sx={{ 
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #1976D2 30%, #1CB5E0 90%)',
            }
          }}
        >
          Export Teachers Performance
        </Button>
        <Button
          variant="contained"
          startIcon={<TableChart />}
          onClick={() => handleExportStudents()}
          disabled={refreshing}
          sx={{ 
            background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #388E3C 30%, #689F38 90%)',
            }
          }}
        >
          Export Students Performance
        </Button>
        <Button
          variant="contained"
          startIcon={<Assessment />}
          onClick={() => handleExportComprehensive()}
          disabled={refreshing}
          sx={{ 
            background: 'linear-gradient(45deg, #FF9800 30%, #FFC107 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #F57C00 30%, #FFA000 90%)',
            }
          }}
        >
          Export NIRF Metrics
        </Button>
        </Box>
      </Box>
      <MagicBento
        data={bentoData}
        enableParticles={true}
        enableGlow={true}
        enableTilt={true}
        glowColor="25, 118, 210"
        onCardClick={handleCardClick}
        title=""
      />
      
      <ErrorDialog
        open={showErrorDialog && error !== null}
        error={error}
        onClose={() => setShowErrorDialog(false)}
        onRetry={() => fetchStats(true)}
      />
    </Box>
  );
};

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<any>(null);
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const [filter, setFilter] = useState<{ role?: UserRole; status?: UserStatus }>({});

  const fetchUsers = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      const response = await adminApi.getAllUsers(filter.role, filter.status);
      setUsers(response.data);
      setError(null); // Clear any previous errors
      console.log('📊 Fetched users:', response.data.length);
    } catch (error) {
      console.error('Error fetching users:', error);
      setError(error);
      setShowErrorDialog(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchUsers();
    
    // Refresh data every 30 seconds for real-time updates
    const interval = setInterval(() => fetchUsers(true), 30000);
    
    return () => clearInterval(interval);
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
    <GlassPendingReviewsUI 
      title="My Students" 
      subtitle="Manage student accounts and profiles"
    >
      <Box>
        <Typography variant="h4" gutterBottom sx={{ color: '#333', mb: 3 }}>
          Student Management
        </Typography>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" gap={2} alignItems="center">
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={() => fetchUsers(true)}
            disabled={refreshing}
            sx={{ minWidth: 120 }}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </Button>
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
      
      <ErrorDialog
        open={showErrorDialog && error !== null}
        error={error}
        onClose={() => setShowErrorDialog(false)}
        onRetry={() => fetchUsers(true)}
      />
      </Box>
    </GlassPendingReviewsUI>
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
    <GlassPendingReviewsUI 
      title="Pending Approvals" 
      subtitle="Review and approve student registrations"
    >
      <Box>
        <Typography variant="h4" gutterBottom sx={{ color: '#333', mb: 3 }}>
          Approval Management
        </Typography>

      <TableContainer 
        component={Paper}
        sx={{
          background: 'rgba(255, 255, 255, 0.2)',
          backdropFilter: 'blur(30px)',
          border: '3px solid rgba(255, 255, 255, 0.4)',
          borderRadius: 3,
          boxShadow: '0 25px 80px rgba(0, 0, 0, 0.6), 0 0 60px rgba(25, 118, 210, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.03) 50%, transparent 70%)',
            animation: 'shimmer 4s ease-in-out infinite',
            pointerEvents: 'none'
          }
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Name</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Email</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Role</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Department</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>ID</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Registered</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold', borderColor: 'rgba(255, 255, 255, 0.2)' }}>Actions</TableCell>
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
    </GlassPendingReviewsUI>
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
    <GlassPendingReviewsUI 
      title="Student Allocations" 
      subtitle="Manage student-teacher assignments and allocations"
    >
      <Box>
        <Typography variant="h4" gutterBottom sx={{ color: '#333', mb: 3 }}>
          Allocation Management
        </Typography>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          variant="contained"
          startIcon={<School />}
          onClick={() => setAllocationDialog(true)}
          sx={{
            background: 'linear-gradient(45deg, #e91e63, #9c27b0)',
            '&:hover': {
              background: 'linear-gradient(45deg, #c2185b, #7b1fa2)',
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 16px rgba(233, 30, 99, 0.3)'
            },
            borderRadius: '25px',
            px: 3,
            py: 1.5,
            fontWeight: 'bold',
            textTransform: 'none',
            fontSize: '1rem',
            boxShadow: '0 4px 12px rgba(233, 30, 99, 0.3)',
            transition: 'all 0.3s ease'
          }}
        >
          Allocate Students
        </Button>
      </Box>

      <TableContainer 
        component={Paper} 
        className="table-container"
        sx={{
          borderRadius: '16px',
          overflow: 'hidden',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}
      >
        <Table>
          <TableHead>
            <TableRow sx={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              '& .MuiTableCell-head': {
                color: 'white',
                fontWeight: 'bold',
                fontSize: '1rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }
            }}>
              <TableCell>Teacher</TableCell>
              <TableCell>Student</TableCell>
              <TableCell>Teacher Department</TableCell>
              <TableCell>Student ID</TableCell>
              <TableCell>Allocated On</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {allocations.map((allocation, index) => (
              <TableRow 
                key={allocation.id}
                sx={{
                  '&:nth-of-type(odd)': {
                    backgroundColor: 'rgba(0, 0, 0, 0.02)',
                  },
                  '&:hover': {
                    backgroundColor: 'rgba(103, 126, 234, 0.08)',
                    transform: 'scale(1.01)',
                    transition: 'all 0.2s ease'
                  },
                  transition: 'all 0.2s ease'
                }}
              >
                <TableCell sx={{ fontWeight: '500', color: '#333' }}>
                  {allocation.teacher_name}
                </TableCell>
                <TableCell sx={{ fontWeight: '500', color: '#333' }}>
                  {allocation.student_name}
                </TableCell>
                <TableCell>
                  <Chip 
                    label={teachers.find(t => t.id === allocation.teacher_id)?.department || '-'} 
                    size="small"
                    sx={{
                      background: 'linear-gradient(45deg, #e91e63, #9c27b0)',
                      color: 'white',
                      fontWeight: 'bold'
                    }}
                  />
                </TableCell>
                <TableCell sx={{ fontWeight: '500', color: '#666' }}>
                  {students.find(s => s.id === allocation.student_id)?.student_id || '-'}
                </TableCell>
                <TableCell sx={{ color: '#666' }}>
                  {new Date(allocation.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Tooltip title="Remove Allocation">
                    <IconButton
                      color="error"
                      onClick={() => handleRemoveAllocation(allocation.id)}
                      sx={{
                        '&:hover': {
                          backgroundColor: 'rgba(244, 67, 54, 0.1)',
                          transform: 'scale(1.1)'
                        },
                        transition: 'all 0.2s ease'
                      }}
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
        <Box 
          textAlign="center" 
          mt={4}
          sx={{
            p: 4,
            borderRadius: '16px',
            background: 'linear-gradient(135deg, rgba(103, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
            border: '2px dashed rgba(103, 126, 234, 0.3)'
          }}
        >
          <School sx={{ fontSize: 64, color: '#667eea', mb: 2 }} />
          <Typography variant="h6" color="textSecondary" sx={{ mb: 1 }}>
            No Student-Teacher Allocations Found
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
            Click "Allocate Students" to create new teacher-student assignments
          </Typography>
          <Button
            variant="contained"
            startIcon={<School />}
            onClick={() => setAllocationDialog(true)}
            sx={{
              background: 'linear-gradient(45deg, #e91e63, #9c27b0)',
              '&:hover': {
                background: 'linear-gradient(45deg, #c2185b, #7b1fa2)',
                transform: 'translateY(-2px)',
                boxShadow: '0 8px 16px rgba(233, 30, 99, 0.3)'
              },
              borderRadius: '25px',
              px: 3,
              py: 1.5,
              fontWeight: 'bold',
              textTransform: 'none'
            }}
          >
            Create First Allocation
          </Button>
        </Box>
      )}

      {/* Allocation Dialog */}
      <Dialog 
        open={allocationDialog} 
        onClose={() => setAllocationDialog(false)} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: '16px',
            background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.9) 100%)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
          }
        }}
      >
        <DialogTitle sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          fontWeight: 'bold',
          textAlign: 'center',
          py: 2
        }}>
          <School sx={{ mr: 1, verticalAlign: 'middle' }} />
          Allocate Students to Teacher
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <FormControl fullWidth margin="normal">
            <InputLabel>Select Teacher</InputLabel>
            <Select
              value={selectedTeacher || ''}
              label="Select Teacher"
              onChange={(e) => setSelectedTeacher(e.target.value as number)}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '12px',
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#667eea'
                  }
                }
              }}
            >
              {teachers.map((teacher) => (
                <MenuItem key={teacher.id} value={teacher.id}>
                  <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                    <School sx={{ mr: 1, color: '#667eea' }} />
                    <Box>
                      <Typography variant="body1" fontWeight="500">
                        {teacher.full_name}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {teacher.department}
                      </Typography>
                    </Box>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Typography variant="h6" sx={{ 
            mt: 3, 
            mb: 2,
            background: 'linear-gradient(45deg, #1976d2, #e91e63)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 'bold'
          }}>
            Select Students:
          </Typography>
          
          <List sx={{ 
            maxHeight: 300, 
            overflow: 'auto',
            border: '1px solid rgba(103, 126, 234, 0.2)',
            borderRadius: '12px',
            p: 1
          }}>
            {students.map((student) => (
              <ListItem 
                key={student.id}
                sx={{
                  borderRadius: '8px',
                  mb: 0.5,
                  '&:hover': {
                    backgroundColor: 'rgba(103, 126, 234, 0.08)'
                  }
                }}
              >
                <Checkbox
                  checked={selectedStudents.includes(student.id)}
                  onChange={() => handleStudentToggle(student.id)}
                  sx={{
                    color: '#667eea',
                    '&.Mui-checked': {
                      color: '#667eea'
                    }
                  }}
                />
                <ListItemText
                  primary={
                    <Typography variant="body1" fontWeight="500">
                      {student.full_name}
                    </Typography>
                  }
                  secondary={
                    <Typography variant="caption" color="textSecondary">
                      ID: {student.student_id} • Department: {student.department}
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions sx={{ p: 3, gap: 2 }}>
          <Button 
            onClick={() => setAllocationDialog(false)} 
            disabled={submitting}
            sx={{
              borderRadius: '25px',
              px: 3,
              py: 1,
              textTransform: 'none',
              fontWeight: 'bold'
            }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleAllocateStudents}
            variant="contained"
            disabled={!selectedTeacher || selectedStudents.length === 0 || submitting}
            sx={{
              background: 'linear-gradient(45deg, #e91e63, #9c27b0)',
              '&:hover': {
                background: 'linear-gradient(45deg, #c2185b, #7b1fa2)',
                transform: 'translateY(-2px)',
                boxShadow: '0 8px 16px rgba(233, 30, 99, 0.3)'
              },
              borderRadius: '25px',
              px: 3,
              py: 1,
              fontWeight: 'bold',
              textTransform: 'none',
              boxShadow: '0 4px 12px rgba(233, 30, 99, 0.3)',
              transition: 'all 0.3s ease'
            }}
          >
            {submitting ? <CircularProgress size={24} color="inherit" /> : 'Allocate Students'}
          </Button>
        </DialogActions>
      </Dialog>
      </Box>
    </GlassPendingReviewsUI>
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
    <GlassPendingReviewsUI 
      title="All Activities" 
      subtitle="Review and manage student activity submissions"
    >
      <Box>
        <Typography variant="h4" gutterBottom sx={{ color: '#333', mb: 3 }}>
          Activity Management
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
    </GlassPendingReviewsUI>
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
