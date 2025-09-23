import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import { UserRole, UserStatus } from '../types';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: UserRole[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  console.log('🛡️ ProtectedRoute: Checking access...', {
    isLoading,
    isAuthenticated,
    user: user ? { username: user.username, role: user.role, status: user.status } : null,
    allowedRoles
  });

  if (isLoading) {
    console.log('🛡️ ProtectedRoute: Still loading...');
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    console.log('🛡️ ProtectedRoute: Not authenticated, redirecting to login');
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!user) {
    console.log('🛡️ ProtectedRoute: No user data, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  // Check if user status is approved (case-insensitive)
  const userStatus = user.status?.toLowerCase();
  const isApproved = userStatus === 'approved' || userStatus === UserStatus.APPROVED.toLowerCase();
  
  if (!isApproved) {
    console.log('🛡️ ProtectedRoute: User not approved, status:', user.status);
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
      >
        <h2>Account Pending Approval</h2>
        <p>Your account is pending approval from an administrator.</p>
        <p>Status: {user.status}</p>
        <p>Please contact your institution for assistance.</p>
      </Box>
    );
  }

  if (!allowedRoles.includes(user.role)) {
    console.log('🛡️ ProtectedRoute: Role not allowed, user role:', user.role, 'allowed:', allowedRoles);
    return <Navigate to="/login" replace />;
  }

  console.log('🛡️ ProtectedRoute: Access granted');
  return <>{children}</>;
};

export default ProtectedRoute;

