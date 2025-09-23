import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  Home as HomeIcon,
  Login as LoginIcon
} from '@mui/icons-material';
import { getErrorAction, ErrorAction } from '../utils/errorHandler';

interface ErrorDialogProps {
  open: boolean;
  error: any;
  onClose: () => void;
  onRetry?: () => void;
}

const ErrorDialog: React.FC<ErrorDialogProps> = ({ open, error, onClose, onRetry }) => {
  const errorAction: ErrorAction = getErrorAction(error || null);

  const handleAction = () => {
    if (errorAction.onAction) {
      errorAction.onAction();
    }
    onClose();
  };

  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    }
    onClose();
  };

  const getActionIcon = () => {
    switch (errorAction.action) {
      case 'retry':
        return <RefreshIcon />;
      case 'login':
        return <LoginIcon />;
      case 'home':
        return <HomeIcon />;
      default:
        return <ErrorIcon />;
    }
  };

  const getActionColor = () => {
    switch (errorAction.action) {
      case 'retry':
        return 'primary';
      case 'login':
        return 'secondary';
      case 'home':
        return 'primary';
      default:
        return 'error';
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)'
        }
      }}
    >
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          <ErrorIcon color="error" />
          <Typography variant="h6" component="div">
            Action Required
          </Typography>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        <Alert 
          severity="error" 
          sx={{ 
            mb: 2,
            '& .MuiAlert-message': {
              width: '100%'
            }
          }}
        >
          <Typography variant="body1">
            {errorAction.message}
          </Typography>
        </Alert>
        
        {errorAction.action && (
          <Box mt={2}>
            <Typography variant="body2" color="textSecondary">
              What would you like to do?
            </Typography>
          </Box>
        )}
      </DialogContent>
      
      <DialogActions sx={{ p: 2, gap: 1 }}>
        <Button
          onClick={onClose}
          variant="outlined"
          color="inherit"
        >
          Close
        </Button>
        
        {errorAction.action === 'retry' && onRetry && (
          <Button
            onClick={handleRetry}
            variant="contained"
            color={getActionColor() as any}
            startIcon={getActionIcon()}
          >
            {errorAction.actionText}
          </Button>
        )}
        
        {errorAction.action && errorAction.action !== 'retry' && (
          <Button
            onClick={handleAction}
            variant="contained"
            color={getActionColor() as any}
            startIcon={getActionIcon()}
          >
            {errorAction.actionText}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default ErrorDialog;
