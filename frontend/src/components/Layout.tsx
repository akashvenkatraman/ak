import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Divider,
  Avatar,
  Tooltip,
} from '@mui/material';
import { keyframes } from '@mui/system';
import {
  Menu as MenuIcon,
  Dashboard,
  Assignment,
  People,
  Notifications,
  AccountCircle,
  ExitToApp,
  School,
  CheckCircle,
  PendingActions,
  Person,
  Analytics,
  Storage,
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';
import { notificationApi } from '../services/api';
import { UserRole } from '../types';
import { useNavigate, useLocation } from 'react-router-dom';
import Logo from './Logo';

// Animation keyframes
const slideInLeft = keyframes`
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
`;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [notificationMenuAnchor, setNotificationMenuAnchor] = useState<null | HTMLElement>(null);
  const [profileMenuAnchor, setProfileMenuAnchor] = useState<null | HTMLElement>(null);
  const [notifications, setNotifications] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Fetch notifications
  useEffect(() => {
    if (user) {
      const fetchNotifications = async () => {
        try {
          const [notificationsResponse, unreadResponse] = await Promise.all([
            notificationApi.getNotifications(false, 10), // Get recent 10 notifications
            notificationApi.getUnreadCount()
          ]);
          setNotifications(notificationsResponse.data);
          setUnreadCount(unreadResponse.data.unread_count);
        } catch (error) {
          console.error('Error fetching notifications:', error);
        }
      };

      fetchNotifications();
      // Refresh notifications every 30 seconds
      const interval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationApi.markAsRead(notificationId);
      setNotifications(prev => 
        prev.map(notif => 
          notif.id === notificationId ? { ...notif, is_read: true } : notif
        )
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationApi.markAllAsRead();
      setNotifications(prev => 
        prev.map(notif => ({ ...notif, is_read: true }))
      );
      setUnreadCount(0);
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
    }
  };

  const getMenuItems = () => {
    if (!user) return [];

    const baseItems = [
      {
        text: 'Dashboard',
        icon: <Dashboard />,
        path: `/${user.role}`,
        roles: [UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT],
      },
      {
        text: 'Storage Test',
        icon: <Storage />,
        path: '/storage-test',
        roles: [UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT],
      },
    ];

    const roleSpecificItems = {
      [UserRole.ADMIN]: [
        { text: 'User Management', icon: <People />, path: '/admin/users' },
        { text: 'Pending Approvals', icon: <PendingActions />, path: '/admin/pending' },
        { text: 'Student Allocation', icon: <School />, path: '/admin/allocations' },
        { text: 'All Activities', icon: <Assignment />, path: '/admin/activities' },
        { text: 'Analytics & Reports', icon: <Analytics />, path: '/admin/analytics' },
      ],
      [UserRole.TEACHER]: [
        { text: 'My Students', icon: <People />, path: '/teacher/students' },
        { text: 'Pending Reviews', icon: <PendingActions />, path: '/teacher/pending' },
        { text: 'All Activities', icon: <Assignment />, path: '/teacher/activities' },
        { text: 'Approval History', icon: <CheckCircle />, path: '/teacher/approvals' },
      ],
      [UserRole.STUDENT]: [
        { text: 'My Activities', icon: <Assignment />, path: '/student/activities' },
        { text: 'Add Activity', icon: <Assignment />, path: '/student/add-activity' },
        { text: 'Performance', icon: <Dashboard />, path: '/student/performance' },
      ],
    };

    return [...baseItems, ...(roleSpecificItems[user.role] || [])];
  };

  const menuItems = getMenuItems();

  return (
    <Box sx={{ display: 'flex' }}>
      {/* Professional Header */}
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: (theme) => theme.zIndex.drawer + 1,
          height: 64,
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)'
        }}
      >
        <Toolbar sx={{ position: 'relative', zIndex: 1 }}>
          {/* Professional Menu Button */}
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={() => setDrawerOpen(!drawerOpen)}
            sx={{ 
              mr: 2,
              color: '#1976d2',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              transform: drawerOpen ? 'rotate(90deg)' : 'rotate(0deg)',
              '&:hover': {
                backgroundColor: 'rgba(25, 118, 210, 0.08)',
                transform: drawerOpen ? 'rotate(90deg) scale(1.1)' : 'rotate(0deg) scale(1.1)',
                boxShadow: '0 4px 12px rgba(25, 118, 210, 0.2)'
              }
            }}
          >
            <MenuIcon />
          </IconButton>
          
          {/* Professional Logo Section */}
          <Box 
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              flexGrow: 1
            }}
          >
            <Logo size="small" showText={true} variant="horizontal" />
          </Box>

          {user && (
            <>
              {/* Professional Notification Button */}
              <IconButton
                color="inherit"
                onClick={(e) => setNotificationMenuAnchor(e.currentTarget)}
                sx={{
                  color: '#666',
                  mx: 1,
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    backgroundColor: 'rgba(25, 118, 210, 0.08)',
                    color: '#1976d2',
                    transform: 'scale(1.1)',
                    boxShadow: '0 4px 12px rgba(25, 118, 210, 0.2)'
                  }
                }}
              >
                <Badge 
                  badgeContent={unreadCount}
                  sx={{
                    '& .MuiBadge-badge': {
                      animation: unreadCount > 0 ? `${pulse} 2s infinite` : 'none',
                      transform: 'scale(1)',
                      transition: 'all 0.3s ease'
                    }
                  }}
                >
                  <Notifications />
                </Badge>
              </IconButton>

              {/* Professional Profile Section */}
              <IconButton
                onClick={(e) => setProfileMenuAnchor(e.currentTarget)}
                sx={{
                  color: '#666',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    backgroundColor: 'rgba(25, 118, 210, 0.08)',
                    transform: 'scale(1.1)',
                    boxShadow: '0 4px 12px rgba(25, 118, 210, 0.2)'
                  }
                }}
              >
                <Tooltip title={`${user.full_name} (${user.role})`}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {user.profile_picture ? (
                      <Avatar
                        src={`http://localhost:8000${user.profile_picture}`}
                        alt={user.full_name}
                        sx={{ 
                          width: 32, 
                          height: 32
                        }}
                      />
                    ) : (
                      <Avatar sx={{ 
                        width: 32, 
                        height: 32, 
                        bgcolor: 'primary.main'
                      }}>
                        {user.full_name?.charAt(0) || user.username?.charAt(0) || 'U'}
                      </Avatar>
                    )}
                  </Box>
                </Tooltip>
              </IconButton>
            </>
          )}
        </Toolbar>
      </Box>

      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        sx={{
          width: 280,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 280,
            boxSizing: 'border-box',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            borderRight: '1px solid rgba(0, 0, 0, 0.1)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: drawerOpen ? 'translateX(0)' : 'translateX(-100%)',
          },
        }}
        transitionDuration={300}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto', p: 2 }}>
          <Typography 
            variant="h6" 
            sx={{ 
              color: '#1976d2', 
              mb: 2, 
              textAlign: 'center',
              fontWeight: 600
            }}
          >
            Navigation
          </Typography>
          <List>
            {menuItems.map((item, index) => (
              <ListItem
                key={item.text}
                onClick={() => {
                  navigate(item.path);
                  setDrawerOpen(false);
                }}
                sx={{
                  cursor: 'pointer',
                  borderRadius: 2,
                  mb: 1,
                  background: location.pathname === item.path 
                    ? 'linear-gradient(135deg, rgba(25, 118, 210, 0.1) 0%, rgba(25, 118, 210, 0.05) 100%)' 
                    : 'transparent',
                  border: location.pathname === item.path 
                    ? '1px solid rgba(25, 118, 210, 0.3)' 
                    : '1px solid transparent',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  transform: 'translateX(0)',
                  animation: `${slideInLeft} 0.5s ease-out ${index * 0.1}s both`,
                  '&:hover': {
                    background: location.pathname === item.path 
                      ? 'linear-gradient(135deg, rgba(25, 118, 210, 0.15) 0%, rgba(25, 118, 210, 0.08) 100%)' 
                      : 'linear-gradient(135deg, rgba(0, 0, 0, 0.04) 0%, rgba(0, 0, 0, 0.02) 100%)',
                    transform: 'translateX(8px) scale(1.02)',
                    borderColor: 'rgba(25, 118, 210, 0.4)',
                    boxShadow: '0 4px 12px rgba(25, 118, 210, 0.15)'
                  },
                  '&:active': {
                    transform: 'translateX(4px) scale(0.98)',
                    transition: 'all 0.1s ease'
                  }
                }}
              >
                <ListItemIcon sx={{ 
                  color: location.pathname === item.path ? '#1976d2' : '#666', 
                  minWidth: 40,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'scale(1.1) rotate(5deg)',
                    color: '#1976d2'
                  }
                }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={item.text} 
                  sx={{ 
                    color: '#333',
                    '& .MuiListItemText-primary': {
                      fontWeight: location.pathname === item.path ? 600 : 400,
                    }
                  }} 
                />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Magical Notifications Menu */}
      <Menu
        anchorEl={notificationMenuAnchor}
        open={Boolean(notificationMenuAnchor)}
        onClose={() => setNotificationMenuAnchor(null)}
        PaperProps={{
          style: {
            maxHeight: 400,
            width: '350px',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(0, 0, 0, 0.1)',
            borderRadius: '12px',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
            color: '#333'
          },
        }}
      >
        <MenuItem 
          onClick={handleMarkAllAsRead}
          sx={{
            background: 'rgba(25, 118, 210, 0.1)',
            border: '1px solid rgba(25, 118, 210, 0.3)',
            borderRadius: 1,
            m: 1,
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'rgba(25, 118, 210, 0.2)',
              transform: 'translateY(-1px)'
            }
          }}
        >
          <Typography variant="body2" sx={{ color: '#1976d2', fontWeight: 600 }}>
            Mark All as Read
          </Typography>
        </MenuItem>
        <Divider sx={{ borderColor: 'rgba(0, 0, 0, 0.1)' }} />
        {notifications.length === 0 ? (
          <MenuItem>
            <Typography variant="body2" sx={{ color: '#666' }}>
              No notifications
            </Typography>
          </MenuItem>
        ) : (
          notifications.map((notification) => (
            <MenuItem 
              key={notification.id} 
              onClick={() => {
                if (!notification.is_read) {
                  handleMarkAsRead(notification.id);
                }
                setNotificationMenuAnchor(null);
              }}
              sx={{
                background: notification.is_read 
                  ? 'transparent' 
                  : 'rgba(25, 118, 210, 0.1)',
                border: notification.is_read 
                  ? '1px solid transparent' 
                  : '1px solid rgba(25, 118, 210, 0.3)',
                borderRadius: 1,
                m: 1,
                transition: 'all 0.3s ease',
                '&:hover': {
                  background: notification.is_read 
                    ? 'rgba(0, 0, 0, 0.04)' 
                    : 'rgba(25, 118, 210, 0.15)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 4px 12px rgba(25, 118, 210, 0.2)'
                }
              }}
            >
              <Box>
                <Typography variant="body2" fontWeight="bold" sx={{ color: 'white' }}>
                  {notification.title}
                </Typography>
                <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  {notification.message}
                </Typography>
                <Typography variant="caption" display="block" sx={{ color: 'rgba(255, 255, 255, 0.5)' }}>
                  {new Date(notification.created_at).toLocaleString()}
                </Typography>
              </Box>
            </MenuItem>
          ))
        )}
      </Menu>

      {/* Clean Profile Menu */}
      <Menu
        anchorEl={profileMenuAnchor}
        open={Boolean(profileMenuAnchor)}
        onClose={() => setProfileMenuAnchor(null)}
        PaperProps={{
          style: {
            background: '#ffffff',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            color: '#333',
            minWidth: '200px',
            marginTop: '8px'
          },
        }}
      >
        <MenuItem 
          onClick={() => {
            navigate('/profile');
            setProfileMenuAnchor(null);
          }}
          sx={{
            borderRadius: 2,
            m: 0.5,
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'rgba(25, 118, 210, 0.1)',
              transform: 'translateY(-1px)'
            }
          }}
        >
          <ListItemIcon sx={{ color: '#1976d2', minWidth: 36 }}>
            <Person fontSize="small" />
          </ListItemIcon>
          <Typography sx={{ color: '#333', fontWeight: 500 }}>Profile</Typography>
        </MenuItem>
        <Divider sx={{ borderColor: 'rgba(0, 0, 0, 0.1)', mx: 1 }} />
        <MenuItem 
          onClick={handleLogout}
          sx={{
            borderRadius: 2,
            m: 0.5,
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'rgba(244, 67, 54, 0.1)',
              transform: 'translateY(-1px)'
            }
          }}
        >
          <ListItemIcon sx={{ color: '#f44336', minWidth: 36 }}>
            <ExitToApp fontSize="small" />
          </ListItemIcon>
          <Typography sx={{ color: '#f44336', fontWeight: 500 }}>Logout</Typography>
        </MenuItem>
      </Menu>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          background: 'transparent',
          minHeight: '100vh',
          p: 3,
          mt: 8, // Account for AppBar height
          animation: `${slideInLeft} 0.6s ease-out`,
          transition: 'all 0.3s ease'
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;

