import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Paper,
} from '@mui/material';
import {
  ExpandMore,
  Timeline,
  Person,
  Schedule,
  Description,
  CheckCircle,
  Cancel,
  Visibility,
  Download,
  Edit,
  Add,
} from '@mui/icons-material';
import { activityLogsApi } from '../services/api';
import { ActivityLog, ActivityLogType } from '../types';

interface ActivityLogsProps {
  activityId?: number;
  userId?: number;
  isAdmin?: boolean;
  isTeacher?: boolean;
  limit?: number;
}

const ActivityLogs: React.FC<ActivityLogsProps> = ({
  activityId,
  userId,
  isAdmin = false,
  isTeacher = false,
  limit = 50,
}) => {
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLogs();
  }, [activityId, userId, isAdmin, isTeacher, limit]);

  const loadLogs = async () => {
    try {
      setLoading(true);
      let response;
      
      if (activityId) {
        response = await activityLogsApi.getActivityLogs(activityId);
      } else if (isAdmin) {
        response = await activityLogsApi.getAdminLogs(undefined, userId, undefined, limit);
      } else if (isTeacher) {
        response = await activityLogsApi.getTeacherLogs(userId, undefined, limit);
      } else {
        response = await activityLogsApi.getMyLogs(limit);
      }
      
      setLogs(response.data);
    } catch (err: any) {
      setError('Failed to load activity logs');
      console.error('Error loading logs:', err);
    } finally {
      setLoading(false);
    }
  };

  const getLogIcon = (logType: ActivityLogType) => {
    switch (logType) {
      case ActivityLogType.ACTIVITY_CREATED:
        return <Add color="primary" />;
      case ActivityLogType.ACTIVITY_UPDATED:
        return <Edit color="info" />;
      case ActivityLogType.ACTIVITY_APPROVED:
        return <CheckCircle color="success" />;
      case ActivityLogType.ACTIVITY_REJECTED:
        return <Cancel color="error" />;
      case ActivityLogType.ACTIVITY_UNDER_REVIEW:
        return <Schedule color="warning" />;
      case ActivityLogType.CERTIFICATE_UPLOADED:
        return <Description color="primary" />;
      case ActivityLogType.CERTIFICATE_VIEWED:
        return <Visibility color="info" />;
      case ActivityLogType.CERTIFICATE_DOWNLOADED:
        return <Download color="success" />;
      default:
        return <Timeline color="inherit" />;
    }
  };

  const getLogColor = (logType: ActivityLogType) => {
    switch (logType) {
      case ActivityLogType.ACTIVITY_APPROVED:
      case ActivityLogType.CERTIFICATE_DOWNLOADED:
        return 'success';
      case ActivityLogType.ACTIVITY_REJECTED:
        return 'error';
      case ActivityLogType.ACTIVITY_UNDER_REVIEW:
        return 'warning';
      case ActivityLogType.ACTIVITY_CREATED:
      case ActivityLogType.CERTIFICATE_UPLOADED:
        return 'primary';
      default:
        return 'inherit';
    }
  };

  const formatLogType = (logType: ActivityLogType) => {
    return logType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={2}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" onClose={() => setError(null)}>
        {error}
      </Alert>
    );
  }

  if (logs.length === 0) {
    return (
      <Card>
        <CardContent>
          <Box textAlign="center" py={4}>
            <Timeline sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              No activity logs found
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Activity logs will appear here as actions are performed
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Activity Logs ({logs.length})
      </Typography>
      
      <List>
        {logs.map((log, index) => (
          <React.Fragment key={log.id}>
            <ListItem>
              <Box display="flex" alignItems="flex-start" width="100%">
                <Box mr={2} mt={0.5}>
                  {getLogIcon(log.log_type)}
                </Box>
                <Box flex={1}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <Chip
                      label={formatLogType(log.log_type)}
                      color={getLogColor(log.log_type) as any}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      {formatDateTime(log.created_at)}
                    </Typography>
                  </Box>
                  
                  <Typography variant="body2" gutterBottom>
                    {log.action}
                  </Typography>
                  
                  {log.user_name && (
                    <Typography variant="caption" color="text.secondary">
                      by {log.user_name}
                    </Typography>
                  )}
                  
                  {log.details && Object.keys(log.details).length > 0 && (
                    <Accordion sx={{ mt: 1 }}>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography variant="caption">Details</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Box component="pre" sx={{ fontSize: '0.75rem', overflow: 'auto' }}>
                          {JSON.stringify(log.details, null, 2)}
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </Box>
              </Box>
            </ListItem>
            {index < logs.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default ActivityLogs;
