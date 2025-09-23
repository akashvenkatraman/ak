import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, Chip, Avatar, LinearProgress } from '@mui/material';
import {
  Pending as PendingIcon,
  Assignment as AssignmentIcon,
  School as SchoolIcon,
  CheckCircle as CheckIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon
} from '@mui/icons-material';

interface PendingReview {
  id: string;
  type: 'student' | 'activity' | 'approval';
  title: string;
  description: string;
  studentName: string;
  studentAvatar?: string;
  status: 'pending' | 'in_review' | 'approved' | 'rejected';
  priority: 'high' | 'medium' | 'low';
  submittedDate: string;
  estimatedTime: string;
  reviewer?: string;
}

interface PendingReviewsBackgroundProps {
  children: React.ReactNode;
  showBackground?: boolean;
}

const PendingReviewsBackground: React.FC<PendingReviewsBackgroundProps> = ({ 
  children, 
  showBackground = true 
}) => {
  // Mock data for pending reviews
  const pendingReviews: PendingReview[] = [
    {
      id: '1',
      type: 'student',
      title: 'New Student Registration',
      description: 'John Doe - Computer Science',
      studentName: 'John Doe',
      status: 'pending',
      priority: 'high',
      submittedDate: '2024-01-15',
      estimatedTime: '5 min',
      reviewer: 'Admin'
    },
    {
      id: '2',
      type: 'activity',
      title: 'Project Submission',
      description: 'Web Development Project - Final Submission',
      studentName: 'Jane Smith',
      status: 'in_review',
      priority: 'medium',
      submittedDate: '2024-01-14',
      estimatedTime: '15 min',
      reviewer: 'Dr. Johnson'
    },
    {
      id: '3',
      type: 'approval',
      title: 'Certificate Request',
      description: 'Course Completion Certificate',
      studentName: 'Mike Wilson',
      status: 'pending',
      priority: 'low',
      submittedDate: '2024-01-13',
      estimatedTime: '3 min',
      reviewer: 'Admin'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return '#ff9800';
      case 'in_review': return '#2196f3';
      case 'approved': return '#4caf50';
      case 'rejected': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#f44336';
      case 'medium': return '#ff9800';
      case 'low': return '#4caf50';
      default: return '#9e9e9e';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'student': return <SchoolIcon />;
      case 'activity': return <AssignmentIcon />;
      case 'approval': return <CheckIcon />;
      default: return <PendingIcon />;
    }
  };

  if (!showBackground) {
    return <>{children}</>;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Animated Background Elements */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%)
          `,
          animation: 'float 20s ease-in-out infinite'
        }}
      />

      {/* Floating Cards Animation */}
      <Box
        sx={{
          position: 'absolute',
          top: '10%',
          right: '5%',
          width: 60,
          height: 60,
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '50%',
          animation: 'float 6s ease-in-out infinite'
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          top: '30%',
          left: '10%',
          width: 40,
          height: 40,
          background: 'rgba(255, 255, 255, 0.08)',
          borderRadius: '50%',
          animation: 'float 8s ease-in-out infinite reverse'
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '20%',
          right: '15%',
          width: 80,
          height: 80,
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '50%',
          animation: 'float 10s ease-in-out infinite'
        }}
      />

      {/* Main Content Container */}
      <Box
        sx={{
          position: 'relative',
          zIndex: 1,
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Header Section */}
        <Box
          sx={{
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(20px)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
            p: 3,
            mb: 4
          }}
        >
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <PendingIcon sx={{ fontSize: 40, color: 'white' }} />
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
              Pending Reviews Dashboard
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            Manage student registrations, activity submissions, and approval requests
          </Typography>
        </Box>

        {/* Pending Reviews Overview */}
        <Box sx={{ px: 3, mb: 4 }}>
          <Box 
            sx={{ 
              display: 'grid', 
              gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' },
              gap: 3 
            }}
          >
            {pendingReviews.map((review) => (
              <Box key={review.id}>
                <Card
                  sx={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: 3,
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-5px)',
                      boxShadow: '0 12px 40px rgba(0, 0, 0, 0.15)'
                    }
                  }}
                >
                  <CardContent>
                    <Box display="flex" alignItems="center" gap={2} mb={2}>
                      <Avatar
                        sx={{
                          bgcolor: getStatusColor(review.status),
                          width: 40,
                          height: 40
                        }}
                      >
                        {getTypeIcon(review.type)}
                      </Avatar>
                      <Box flexGrow={1}>
                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                          {review.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {review.description}
                        </Typography>
                      </Box>
                    </Box>

                    <Box display="flex" alignItems="center" gap={1} mb={2}>
                      <PersonIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                      <Typography variant="body2" color="textSecondary">
                        {review.studentName}
                      </Typography>
                    </Box>

                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                      <Chip
                        label={review.status.replace('_', ' ').toUpperCase()}
                        size="small"
                        sx={{
                          bgcolor: getStatusColor(review.status),
                          color: 'white',
                          fontWeight: 'bold'
                        }}
                      />
                      <Chip
                        label={review.priority.toUpperCase()}
                        size="small"
                        variant="outlined"
                        sx={{
                          borderColor: getPriorityColor(review.priority),
                          color: getPriorityColor(review.priority)
                        }}
                      />
                    </Box>

                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <ScheduleIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                        <Typography variant="body2" color="textSecondary">
                          {review.submittedDate}
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        {review.estimatedTime}
                      </Typography>
                    </Box>

                    {review.reviewer && (
                      <Box display="flex" alignItems="center" gap={1}>
                        <Typography variant="body2" color="textSecondary">
                          Reviewer: {review.reviewer}
                        </Typography>
                      </Box>
                    )}

                    <LinearProgress
                      variant="determinate"
                      value={review.status === 'approved' ? 100 : review.status === 'in_review' ? 50 : 25}
                      sx={{
                        mt: 2,
                        height: 6,
                        borderRadius: 3,
                        bgcolor: 'rgba(0, 0, 0, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          bgcolor: getStatusColor(review.status),
                          borderRadius: 3
                        }
                      }}
                    />
                  </CardContent>
                </Card>
              </Box>
            ))}
          </Box>
        </Box>

        {/* Main Content Area */}
        <Box
          sx={{
            flexGrow: 1,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            borderRadius: '20px 20px 0 0',
            boxShadow: '0 -8px 32px rgba(0, 0, 0, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderBottom: 'none',
            minHeight: '60vh',
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          {/* Content with subtle pattern overlay */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: `
                radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.05) 0%, transparent 50%)
              `,
              pointerEvents: 'none'
            }}
          />
          
          <Box sx={{ position: 'relative', zIndex: 1, p: 3 }}>
            {children}
          </Box>
        </Box>
      </Box>

      {/* CSS Animations */}
      <style>
        {`
          @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
          }
        `}
      </style>
    </Box>
  );
};

export default PendingReviewsBackground;
