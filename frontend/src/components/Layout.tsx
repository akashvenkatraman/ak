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
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';
import { notificationApi } from '../services/api';
import { UserRole } from '../types';
import { useNavigate, useLocation } from 'react-router-dom';
import Logo from './Logo';

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
    ];

    const roleSpecificItems = {
      [UserRole.ADMIN]: [
        { text: 'User Management', icon: <People />, path: '/admin/users' },
        { text: 'Pending Approvals', icon: <PendingActions />, path: '/admin/pending' },
        { text: 'Student Allocation', icon: <School />, path: '/admin/allocations' },
        { text: 'All Activities', icon: <Assignment />, path: '/admin/activities' },
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
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={() => setDrawerOpen(!drawerOpen)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Logo size="small" showText={true} variant="horizontal" />
          </Box>

          {user && (
            <>
              <IconButton
                color="inherit"
                onClick={(e) => setNotificationMenuAnchor(e.currentTarget)}
              >
                <Badge badgeContent={unreadCount} color="error">
                  <Notifications />
                </Badge>
              </IconButton>

              <Tooltip title={`${user.full_name} (${user.role})`}>
                <IconButton
                  color="inherit"
                  onClick={(e) => setProfileMenuAnchor(e.currentTarget)}
                  sx={{ ml: 1 }}
                >
                  {user.profile_picture ? (
                    <Avatar
                      src={`http://localhost:8000${user.profile_picture}`}
                      alt={user.full_name}
                      sx={{ width: 32, height: 32 }}
                    />
                  ) : (
                    <AccountCircle />
                  )}
                </IconButton>
              </Tooltip>

              <Typography variant="body2" sx={{ ml: 1 }}>
                {user.full_name} ({user.role})
              </Typography>
            </>
          )}
        </Toolbar>
      </AppBar>

      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem
                key={item.text}
                onClick={() => {
                  navigate(item.path);
                  setDrawerOpen(false);
                }}
                sx={{
                  cursor: 'pointer',
                  backgroundColor: location.pathname === item.path ? 'rgba(0, 0, 0, 0.08)' : 'transparent',
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Notifications Menu */}
      <Menu
        anchorEl={notificationMenuAnchor}
        open={Boolean(notificationMenuAnchor)}
        onClose={() => setNotificationMenuAnchor(null)}
        PaperProps={{
          style: {
            maxHeight: 400,
            width: '350px',
          },
        }}
      >
        <MenuItem onClick={handleMarkAllAsRead}>
          <Typography variant="body2" color="primary">
            Mark All as Read
          </Typography>
        </MenuItem>
        <Divider />
        {notifications.length === 0 ? (
          <MenuItem>
            <Typography variant="body2" color="textSecondary">
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
                backgroundColor: notification.is_read ? 'transparent' : '#f5f5f5',
              }}
            >
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  {notification.title}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {notification.message}
                </Typography>
                <Typography variant="caption" display="block" color="textSecondary">
                  {new Date(notification.created_at).toLocaleString()}
                </Typography>
              </Box>
            </MenuItem>
          ))
        )}
      </Menu>

      {/* Profile Menu */}
      <Menu
        anchorEl={profileMenuAnchor}
        open={Boolean(profileMenuAnchor)}
        onClose={() => setProfileMenuAnchor(null)}
      >
        <MenuItem onClick={() => {
          navigate('/profile');
          setProfileMenuAnchor(null);
        }}>
          <ListItemIcon>
            <Person fontSize="small" />
          </ListItemIcon>
          Profile
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <ExitToApp fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
          mt: 8, // Account for AppBar height
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;

