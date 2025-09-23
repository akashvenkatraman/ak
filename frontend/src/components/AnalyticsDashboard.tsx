import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Button,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  Assessment,
  School,
  Group,
  Assignment,
  Download,
  Refresh,
} from '@mui/icons-material';
import { adminApi } from '../services/api';

interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string;
    fill?: boolean;
  }>;
}

interface AnalyticsData {
  activity_types: ChartData;
  departments: ChartData;
  monthly_trends: ChartData;
}

const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await adminApi.getSampleAnalyticsDashboardData();
      setAnalyticsData(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const handleExportPerformance = async (type: 'teachers' | 'students' | 'overall') => {
    try {
      let response;
      switch (type) {
        case 'teachers':
          response = await adminApi.exportTeachersSampleData();
          break;
        case 'students':
          response = await adminApi.exportStudentsSampleData();
          break;
        case 'overall':
          response = await adminApi.exportOverallSampleData();
          break;
      }
      
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${type}_performance_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(`Error exporting ${type} data:`, error);
      alert(`Failed to export ${type} data. Please try again.`);
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
        <Button onClick={fetchAnalyticsData} sx={{ ml: 2 }}>
          Retry
        </Button>
      </Alert>
    );
  }

  if (!analyticsData) {
    return (
      <Alert severity="info">
        No analytics data available.
      </Alert>
    );
  }

  // Transform data for charts
  const activityTypesData = analyticsData.activity_types.labels.map((label, index) => ({
    name: label,
    total: analyticsData.activity_types.datasets[0].data[index],
    approved: analyticsData.activity_types.datasets[1].data[index],
  }));

  const departmentsData = analyticsData.departments.labels.map((label, index) => ({
    name: label,
    students: analyticsData.departments.datasets[0].data[index],
    teachers: analyticsData.departments.datasets[1].data[index],
    activities: analyticsData.departments.datasets[2].data[index],
  }));

  const monthlyData = analyticsData.monthly_trends.labels.map((label, index) => ({
    month: label,
    total: analyticsData.monthly_trends.datasets[0].data[index],
    approved: analyticsData.monthly_trends.datasets[1].data[index],
    credits: analyticsData.monthly_trends.datasets[2].data[index],
  }));

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" sx={{ color: '#333', fontWeight: 'bold' }}>
          📊 Analytics Dashboard
        </Typography>
        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchAnalyticsData}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={() => handleExportPerformance('overall')}
            sx={{ 
              background: 'linear-gradient(45deg, #FF9800 30%, #FFC107 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #F57C00 30%, #FFA000 90%)',
              }
            }}
          >
            Export Overall Report
          </Button>
        </Box>
      </Box>

      {/* Export Buttons */}
      <Paper sx={{ p: 3, mb: 3, background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(20px)' }}>
        <Typography variant="h6" sx={{ color: '#333', mb: 2 }}>
          📈 Performance Reports for NIRF/AICTE
        </Typography>
        <Box display="flex" gap={2} flexWrap="wrap">
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={() => handleExportPerformance('teachers')}
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
            startIcon={<Download />}
            onClick={() => handleExportPerformance('students')}
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
            onClick={() => handleExportPerformance('overall')}
            sx={{ 
              background: 'linear-gradient(45deg, #FF9800 30%, #FFC107 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #F57C00 30%, #FFA000 90%)',
              }
            }}
          >
            Export Overall Metrics
          </Button>
        </Box>
      </Paper>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Activity Analysis" />
          <Tab label="Department Performance" />
          <Tab label="Monthly Trends" />
          <Tab label="NIRF Metrics" />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
          <Box flex={2}>
            <Paper sx={{ p: 3, height: 400 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
                Activity Types Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={activityTypesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="total" fill="#8884d8" name="Total Activities" />
                  <Bar dataKey="approved" fill="#82ca9d" name="Approved Activities" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Box>
          <Box flex={1}>
            <Paper sx={{ p: 3, height: 400 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
                Activity Status
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={activityTypesData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }: any) => `${name} ${((percent as number) * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="total"
                  >
                    {activityTypesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Box>
        </Box>
      )}

      {activeTab === 1 && (
        <Box>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
              Department Performance Comparison
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={departmentsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="students" fill="#8884d8" name="Students" />
                <Bar dataKey="teachers" fill="#82ca9d" name="Teachers" />
                <Bar dataKey="activities" fill="#ffc658" name="Activities" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Box>
      )}

      {activeTab === 2 && (
        <Box>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
              Monthly Activity Trends
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="total" stackId="1" stroke="#8884d8" fill="#8884d8" name="Total Activities" />
                <Area type="monotone" dataKey="approved" stackId="1" stroke="#82ca9d" fill="#82ca9d" name="Approved Activities" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Box>
      )}

      {activeTab === 3 && (
        <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
          <Box flex={1}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
                  Key Performance Indicators
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="textSecondary">
                    Student-Teacher Ratio
                  </Typography>
                  <LinearProgress variant="determinate" value={75} sx={{ mb: 1 }} />
                  <Typography variant="body2">75% (Target: 80%)</Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="textSecondary">
                    Activity Approval Rate
                  </Typography>
                  <LinearProgress variant="determinate" value={85} sx={{ mb: 1 }} />
                  <Typography variant="body2">85% (Target: 90%)</Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="textSecondary">
                    Research Activities
                  </Typography>
                  <LinearProgress variant="determinate" value={60} sx={{ mb: 1 }} />
                  <Typography variant="body2">60% (Target: 70%)</Typography>
                </Box>
              </CardContent>
            </Card>
          </Box>
          <Box flex={1}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, color: '#333' }}>
                  NIRF Ranking Factors
                </Typography>
                <Box display="flex" flexDirection="column" gap={2}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Teaching, Learning & Resources</Typography>
                    <Chip label="Good" color="success" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Research and Professional Practice</Typography>
                    <Chip label="Excellent" color="primary" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Graduation Outcomes</Typography>
                    <Chip label="Good" color="success" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Outreach and Inclusivity</Typography>
                    <Chip label="Excellent" color="primary" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Perception</Typography>
                    <Chip label="Good" color="success" size="small" />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default AnalyticsDashboard;
