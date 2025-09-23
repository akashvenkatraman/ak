/**
 * Error handling utility for better user experience
 */

export interface ErrorAction {
  message: string;
  action?: string;
  actionText?: string;
  onAction?: () => void;
}

export const getErrorAction = (error: any): ErrorAction => {
  // Handle null/undefined error
  if (!error) {
    return {
      message: 'An unknown error occurred.',
      action: 'retry',
      actionText: 'Try Again',
      onAction: () => window.location.reload()
    };
  }

  // Handle different error types
  if (error.name === 'NetworkError') {
    return {
      message: 'Unable to connect to server. Please check your internet connection.',
      action: 'retry',
      actionText: 'Retry Connection',
      onAction: () => window.location.reload()
    };
  }

  if (error.name === 'TimeoutError') {
    return {
      message: 'Request is taking too long. Please check your connection.',
      action: 'retry',
      actionText: 'Try Again',
      onAction: () => window.location.reload()
    };
  }

  if (error.name === 'AuthError') {
    return {
      message: 'Your session has expired. Please log in again.',
      action: 'login',
      actionText: 'Go to Login',
      onAction: () => window.location.href = '/login'
    };
  }

  if (error.name === 'ForbiddenError') {
    return {
      message: 'You do not have permission to perform this action.',
      action: 'home',
      actionText: 'Go to Dashboard',
      onAction: () => window.location.href = '/admin'
    };
  }

  if (error.name === 'NotFoundError') {
    return {
      message: 'The requested resource was not found.',
      action: 'home',
      actionText: 'Go to Dashboard',
      onAction: () => window.location.href = '/admin'
    };
  }

  if (error.name === 'ServerError') {
    return {
      message: 'Server is experiencing issues. Please try again later.',
      action: 'retry',
      actionText: 'Try Again',
      onAction: () => window.location.reload()
    };
  }

  // Default error handling
  const message = error?.message || 'An unexpected error occurred.';
  
  if (message.includes('Network Error') || message.includes('ERR_NETWORK')) {
    return {
      message: 'Unable to connect to server. Please check if the backend is running.',
      action: 'retry',
      actionText: 'Retry Connection',
      onAction: () => window.location.reload()
    };
  }

  if (message.includes('timeout')) {
    return {
      message: 'Request timed out. Please check your connection and try again.',
      action: 'retry',
      actionText: 'Try Again',
      onAction: () => window.location.reload()
    };
  }

  // Generic error with retry option
  return {
    message: message,
    action: 'retry',
    actionText: 'Try Again',
    onAction: () => window.location.reload()
  };
};

export const showErrorToast = (error: any, showToast: (message: string, severity: 'error' | 'warning' | 'info' | 'success') => void) => {
  const errorAction = getErrorAction(error);
  showToast(errorAction.message, 'error');
};

export const getErrorMessage = (error: any): string => {
  return getErrorAction(error).message;
};
