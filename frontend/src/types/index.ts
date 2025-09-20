// User types
export enum UserRole {
  ADMIN = 'admin',
  TEACHER = 'teacher',
  STUDENT = 'student'
}

export enum UserStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected'
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  status: UserStatus;
  is_active: boolean;
  phone_number?: string;
  department?: string;
  student_id?: string;
  employee_id?: string;
  performance_score?: number;
  total_credits_earned?: number;
  
  // Profile fields
  profile_picture?: string;
  bio?: string;
  date_of_birth?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  linkedin_url?: string;
  twitter_url?: string;
  website_url?: string;
  
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  email: string;
  username: string;
  full_name: string;
  password: string;
  role: UserRole;
  phone_number?: string;
  department?: string;
  student_id?: string;
  employee_id?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Activity types
export enum ActivityType {
  SEMINAR = 'seminar',
  CONFERENCE = 'conference',
  ONLINE_COURSE = 'online_course',
  MOOC = 'mooc',
  INTERNSHIP = 'internship',
  EXTRACURRICULAR = 'extracurricular',
  WORKSHOP = 'workshop',
  CERTIFICATION = 'certification'
}

export enum ActivityStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  UNDER_REVIEW = 'under_review'
}

export interface Activity {
  id: number;
  student_id: number;
  student_name?: string;
  title: string;
  description?: string;
  activity_type: ActivityType;
  credits: number;
  start_date?: string;
  end_date?: string;
  certificate_file_path?: string;
  additional_documents?: string;
  status: ActivityStatus;
  files_count?: number;
  created_at: string;
  updated_at?: string;
}

export interface ActivityCreate {
  title: string;
  description?: string;
  activity_type: ActivityType;
  credits?: number;
  start_date?: string;
  end_date?: string;
}

export interface ActivityApproval {
  activity_id: number;
  status: ActivityStatus;
  comments?: string;
  credits_awarded?: number;
}

export interface ActivityApprovalResponse {
  id: number;
  activity_id: number;
  teacher_id: number;
  teacher_name?: string;
  status: ActivityStatus;
  comments?: string;
  credits_awarded: number;
  approved_at?: string;
  created_at: string;
}

// Dashboard types
export interface DashboardStats {
  total_activities: number;
  pending_activities: number;
  approved_activities: number;
  rejected_activities: number;
  total_credits: number;
  performance_score: number;
  total_credits_earned: number;
  attendance_percentage?: number;
  gpa?: number;
}

export interface TeacherDashboardStats {
  total_students: number;
  pending_approvals: number;
  total_activities_reviewed: number;
  recent_submissions: Activity[];
}

// Student allocation types
export interface TeacherStudentAllocation {
  id: number;
  teacher_id: number;
  student_id: number;
  teacher_name: string;
  student_name: string;
  created_at: string;
}

export interface TeacherStudentAllocationCreate {
  teacher_id: number;
  student_ids: number[];
}

// Performance types
export interface StudentPerformance {
  id: number;
  student_id: number;
  semester: string;
  academic_year: string;
  gpa?: number;
  attendance_percentage?: number;
  total_credits: number;
  extracurricular_credits: number;
  created_at: string;
  updated_at?: string;
}

// Notification types
export interface Notification {
  type: string;
  title: string;
  message: string;
  timestamp: string;
  activity_id?: number;
  student_name?: string;
  activity_title?: string;
  status?: string;
  teacher_name?: string;
  comments?: string;
}

// File storage types
export interface FileStorage {
  id: number;
  activity_id: number;
  file_name: string;
  original_name: string;
  file_path: string;
  file_size: number;
  file_type: string;
  file_extension: string;
  uploaded_by: number;
  uploader_name?: string;
  is_certificate: boolean;
  download_count: number;
  view_count: number;
  created_at: string;
  updated_at?: string;
}

export interface ActivityWithFiles extends Activity {
  files_count: number;
  files: FileStorage[];
}

// Activity log types
export enum ActivityLogType {
  ACTIVITY_CREATED = 'activity_created',
  ACTIVITY_UPDATED = 'activity_updated',
  ACTIVITY_DELETED = 'activity_deleted',
  ACTIVITY_SUBMITTED = 'activity_submitted',
  ACTIVITY_APPROVED = 'activity_approved',
  ACTIVITY_REJECTED = 'activity_rejected',
  ACTIVITY_UNDER_REVIEW = 'activity_under_review',
  CERTIFICATE_UPLOADED = 'certificate_uploaded',
  CERTIFICATE_VIEWED = 'certificate_viewed',
  CERTIFICATE_DOWNLOADED = 'certificate_downloaded',
  COMMENT_ADDED = 'comment_added',
  CREDITS_AWARDED = 'credits_awarded',
  STATUS_CHANGED = 'status_changed'
}

export interface ActivityLog {
  id: number;
  activity_id: number;
  user_id: number;
  user_name?: string;
  target_user_id?: number;
  target_user_name?: string;
  log_type: ActivityLogType;
  action: string;
  details?: Record<string, any>;
  created_at: string;
}

export interface ActivityLogSummary {
  total_logs: number;
  logs_by_type: Record<string, number>;
  recent_logs: ActivityLog[];
  activity_stats: Record<string, number>;
}

// API response types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

