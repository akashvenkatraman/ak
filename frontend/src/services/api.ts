import axios, { AxiosResponse, AxiosError } from 'axios';
import {
  User,
  UserCreate,
  LoginCredentials,
  AuthResponse,
  Activity,
  ActivityApproval,
  DashboardStats,
  TeacherDashboardStats,
  TeacherStudentAllocation,
  TeacherStudentAllocationCreate,
  StudentPerformance,
  UserStatus,
  UserRole
} from '../types';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  console.log('🌐 Request interceptor:', config.method?.toUpperCase(), config.url);
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('🌐 Added auth token to request');
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('🌐 Response interceptor success:', response.status, response.config.url);
    return response;
  },
  (error: AxiosError) => {
    console.error('🌐 Response interceptor error:', error.message);
    console.error('🌐 Error details:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url
    });
    
    // Handle different types of errors with specific messages
    if (error.code === 'ECONNABORTED') {
      const timeoutError = new Error('Request timeout. Please check your connection and try again.');
      timeoutError.name = 'TimeoutError';
      return Promise.reject(timeoutError);
    }
    
    if (error.code === 'ERR_NETWORK' || !error.response) {
      const networkError = new Error('Unable to connect to server. Please check if the backend is running and try again.');
      networkError.name = 'NetworkError';
      return Promise.reject(networkError);
    }
    
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      const authError = new Error('Session expired. Please log in again.');
      authError.name = 'AuthError';
      return Promise.reject(authError);
    }
    
    if (error.response?.status === 403) {
      const forbiddenError = new Error('Access denied. You do not have permission to perform this action.');
      forbiddenError.name = 'ForbiddenError';
      return Promise.reject(forbiddenError);
    }
    
    if (error.response?.status === 404) {
      const notFoundError = new Error('Resource not found. Please check the URL and try again.');
      notFoundError.name = 'NotFoundError';
      return Promise.reject(notFoundError);
    }
    
    if (error.response?.status >= 500) {
      const serverError = new Error('Server error. Please try again later or contact support.');
      serverError.name = 'ServerError';
      return Promise.reject(serverError);
    }
    
    // For other errors, provide the server message if available
    const responseData = error.response?.data as any;
    const serverMessage = responseData?.detail || responseData?.message || error.message;
    const customError = new Error(serverMessage);
    customError.name = 'ApiError';
    return Promise.reject(customError);
  }
);

// Auth API
export const authApi = {
  register: (userData: UserCreate): Promise<AxiosResponse<User>> =>
    api.post('/auth/register', userData),

  login: (credentials: LoginCredentials): Promise<AxiosResponse<AuthResponse>> => {
    console.log('🌐 API: Making login request...');
    console.log('🌐 API: URL:', `${api.defaults.baseURL}/auth/login`);
    console.log('🌐 API: Credentials:', credentials);
    return api.post('/auth/login', credentials);
  },

  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get('/auth/me'),

  createAdmin: (adminData: UserCreate): Promise<AxiosResponse<{ message: string; user_id: number }>> =>
    api.post('/auth/create-admin', adminData),
};

// Admin API
export const adminApi = {
  getPendingUsers: (role?: UserRole): Promise<AxiosResponse<User[]>> =>
    api.get('/admin/pending-users', { params: { role } }),

  approveUser: (approval: { user_id: number; status: UserStatus; comments?: string }): Promise<AxiosResponse<any>> =>
    api.post('/admin/approve-user', approval),

  getAllUsers: (role?: UserRole, status?: UserStatus): Promise<AxiosResponse<User[]>> =>
    api.get('/admin/users', { params: { role, status } }),

  getTeachers: (): Promise<AxiosResponse<User[]>> =>
    api.get('/admin/teachers'),

  getStudents: (): Promise<AxiosResponse<User[]>> =>
    api.get('/admin/students'),

  allocateStudents: (allocation: TeacherStudentAllocationCreate): Promise<AxiosResponse<any>> =>
    api.post('/admin/allocate-students', allocation),

  getAllocations: (teacherId?: number, studentId?: number): Promise<AxiosResponse<TeacherStudentAllocation[]>> =>
    api.get('/admin/allocations', { params: { teacher_id: teacherId, student_id: studentId } }),

  removeAllocation: (allocationId: number): Promise<AxiosResponse<any>> =>
    api.delete(`/admin/allocations/${allocationId}`),

  getPendingActivities: (): Promise<AxiosResponse<any[]>> =>
    api.get('/admin/activities/pending'),

  getAllActivities: (): Promise<AxiosResponse<any[]>> =>
    api.get('/admin/activities/all'),

  // Data Export Functions
  exportTeachersData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/teachers', { responseType: 'blob' }),

  exportStudentsData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/students', { responseType: 'blob' }),

  exportComprehensiveData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/comprehensive', { responseType: 'blob' }),

  // Analytics and Performance Export Functions
  exportTeachersPerformanceData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/teachers-performance', { responseType: 'blob' }),

  exportStudentsPerformanceData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/students-performance', { responseType: 'blob' }),

  exportNirfMetrics: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/nirf-metrics', { responseType: 'blob' }),

  getAnalyticsDashboardData: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/analytics/dashboard-data'),

  // Sample Data Export Functions (No authentication required)
  exportTeachersSampleData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/teachers-sample', { responseType: 'blob' }),

  exportStudentsSampleData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/students-sample', { responseType: 'blob' }),

  exportOverallSampleData: (): Promise<AxiosResponse<Blob>> =>
    api.get('/admin/export/overall-sample', { responseType: 'blob' }),

  getSampleAnalyticsDashboardData: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/analytics/sample-dashboard-data'),
};

// Student API
export const studentApi = {
  getDashboard: (): Promise<AxiosResponse<DashboardStats>> =>
    api.get('/students/dashboard'),

  createActivity: (activityData: FormData): Promise<AxiosResponse<Activity>> => {
    console.log('🔧 API: createActivity called');
    console.log('🔧 API: FormData entries:');
    
    // Use Array.from to convert FormData entries to array for iteration
    const entries = Array.from(activityData.entries());
    entries.forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
    
    console.log('🔧 API: Sending request to /students/activities');
    
    return api.post('/students/activities', activityData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getActivities: (status?: string): Promise<AxiosResponse<Activity[]>> =>
    api.get('/students/activities', { params: { status } }),

  getActivity: (activityId: number): Promise<AxiosResponse<Activity>> =>
    api.get(`/students/activities/${activityId}`),

  updateActivity: (activityId: number, activityData: FormData): Promise<AxiosResponse<Activity>> =>
    api.put(`/students/activities/${activityId}`, activityData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),

  deleteActivity: (activityId: number): Promise<AxiosResponse<any>> =>
    api.delete(`/students/activities/${activityId}`),

  getPerformance: (): Promise<AxiosResponse<StudentPerformance[]>> =>
    api.get('/students/performance'),
};

// Teacher API
export const teacherApi = {
  getDashboard: (): Promise<AxiosResponse<TeacherDashboardStats>> =>
    api.get('/teachers/dashboard'),

  getAssignedStudents: (): Promise<AxiosResponse<User[]>> =>
    api.get('/teachers/students'),

  getPendingActivities: (studentId?: number): Promise<AxiosResponse<Activity[]>> =>
    api.get('/teachers/pending-activities', { params: { student_id: studentId } }),

  getAllActivities: (studentId?: number, status?: string): Promise<AxiosResponse<Activity[]>> =>
    api.get('/teachers/activities', { params: { student_id: studentId, status } }),

  getActivityDetails: (activityId: number): Promise<AxiosResponse<Activity>> =>
    api.get(`/teachers/activities/${activityId}`),

  approveActivity: (approval: ActivityApproval): Promise<AxiosResponse<any>> =>
    api.post('/teachers/approve-activity', approval),

  getApprovalHistory: (): Promise<AxiosResponse<any[]>> =>
    api.get('/teachers/approvals'),
};

// Notifications API
export const notificationApi = {
  getNotifications: (unreadOnly: boolean = false, limit: number = 50): Promise<AxiosResponse<any[]>> =>
    api.get(`/notifications/?unread_only=${unreadOnly}&limit=${limit}`),

  getUnreadCount: (): Promise<AxiosResponse<{ unread_count: number }>> =>
    api.get('/notifications/unread-count'),

  markAsRead: (notificationId: number): Promise<AxiosResponse<any>> =>
    api.put(`/notifications/${notificationId}/read`),

  markAllAsRead: (): Promise<AxiosResponse<any>> =>
    api.put('/notifications/mark-all-read'),
};

// File Management API
export const fileApi = {
  uploadFile: (activityId: number, file: File): Promise<AxiosResponse<any>> => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/files/upload/${activityId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getActivityFiles: (activityId: number): Promise<AxiosResponse<any[]>> =>
    api.get(`/files/activity/${activityId}`),

  downloadFile: (fileId: number): Promise<AxiosResponse<Blob>> =>
    api.get(`/files/download/${fileId}`, { responseType: 'blob' }),

  viewFile: (fileId: number): Promise<AxiosResponse<any>> =>
    api.get(`/files/view/${fileId}`),

  deleteFile: (fileId: number): Promise<AxiosResponse<any>> =>
    api.delete(`/files/${fileId}`),

  getActivityWithFiles: (activityId: number): Promise<AxiosResponse<any>> =>
    api.get(`/files/activity/${activityId}/with-files`),
};

// Activity Logs API
export const activityLogsApi = {
  getActivityLogs: (activityId: number): Promise<AxiosResponse<any[]>> =>
    api.get(`/activity-logs/activity/${activityId}`),

  getMyLogs: (limit?: number, offset?: number): Promise<AxiosResponse<any[]>> =>
    api.get('/activity-logs/my-logs', { params: { limit, offset } }),

  getAdminLogs: (logType?: string, userId?: number, activityId?: number, limit?: number, offset?: number): Promise<AxiosResponse<any[]>> =>
    api.get('/activity-logs/admin/all-logs', { params: { log_type: logType, user_id: userId, activity_id: activityId, limit, offset } }),

  getTeacherLogs: (studentId?: number, activityId?: number, limit?: number, offset?: number): Promise<AxiosResponse<any[]>> =>
    api.get('/activity-logs/teacher/student-logs', { params: { student_id: studentId, activity_id: activityId, limit, offset } }),

  getLogSummary: (days?: number): Promise<AxiosResponse<any>> =>
    api.get('/activity-logs/summary', { params: { days } }),

  getAdminLogSummary: (days?: number): Promise<AxiosResponse<any>> =>
    api.get('/activity-logs/admin/summary', { params: { days } }),
};

// Profile API
export const profileApi = {
  getProfile: (): Promise<AxiosResponse<any>> =>
    api.get('/profile/profile'),

  updateProfile: (profileData: any): Promise<AxiosResponse<any>> =>
    api.put('/profile/profile', profileData),

  changePassword: (passwordData: { current_password: string; new_password: string; confirm_password: string }): Promise<AxiosResponse<any>> =>
    api.post('/profile/profile/password', passwordData),

  uploadProfilePicture: (file: FormData): Promise<AxiosResponse<any>> =>
    api.post('/profile/profile/picture', file, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),

  deleteProfilePicture: (): Promise<AxiosResponse<any>> =>
    api.delete('/profile/profile/picture'),

  getProfilePicture: (userId: number): Promise<AxiosResponse<any>> =>
    api.get(`/profile/profile/picture/${userId}`),
};

// File download utility
export const downloadFile = (filePath: string) => {
  window.open(`${BASE_URL}/${filePath}`, '_blank');
};

export default api;
