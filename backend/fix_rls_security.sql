-- =====================================================
-- COMPREHENSIVE RLS SECURITY FIX FOR SMART STUDENT HUB
-- =====================================================
-- This script fixes all 13 RLS security issues in your Supabase database
-- Run this in your Supabase SQL Editor

-- =====================================================
-- 1. ENABLE RLS ON ALL TABLES
-- =====================================================

-- Enable RLS on all public tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teacher_student_allocations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.file_storage ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.placement_readiness ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skill_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.career_paths ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 2. USERS TABLE POLICIES
-- =====================================================

-- Users can view their own profile
CREATE POLICY "users_view_own_profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "users_update_own_profile" ON public.users
    FOR UPDATE USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Only authenticated users can insert new users (registration)
CREATE POLICY "users_insert_authenticated" ON public.users
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Users can delete their own profile
CREATE POLICY "users_delete_own_profile" ON public.users
    FOR DELETE USING (auth.uid() = id);

-- =====================================================
-- 3. TEACHER_STUDENT_ALLOCATIONS TABLE POLICIES
-- =====================================================

-- Teachers can view their own allocations
CREATE POLICY "allocations_view_teacher" ON public.teacher_student_allocations
    FOR SELECT USING (auth.uid() = teacher_id);

-- Students can view their own allocations
CREATE POLICY "allocations_view_student" ON public.teacher_student_allocations
    FOR SELECT USING (auth.uid() = student_id);

-- Teachers can insert allocations for their students
CREATE POLICY "allocations_insert_teacher" ON public.teacher_student_allocations
    FOR INSERT WITH CHECK (auth.uid() = teacher_id);

-- Teachers can update their own allocations
CREATE POLICY "allocations_update_teacher" ON public.teacher_student_allocations
    FOR UPDATE USING (auth.uid() = teacher_id)
    WITH CHECK (auth.uid() = teacher_id);

-- Teachers can delete their own allocations
CREATE POLICY "allocations_delete_teacher" ON public.teacher_student_allocations
    FOR DELETE USING (auth.uid() = teacher_id);

-- =====================================================
-- 4. ACTIVITY_APPROVALS TABLE POLICIES
-- =====================================================

-- Students can view their own activity approvals
CREATE POLICY "approvals_view_student" ON public.activity_approvals
    FOR SELECT USING (auth.uid() = student_id);

-- Teachers can view approvals for their students
CREATE POLICY "approvals_view_teacher" ON public.activity_approvals
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.activity_approvals.student_id
        )
    );

-- Teachers can insert approvals for their students
CREATE POLICY "approvals_insert_teacher" ON public.activity_approvals
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.activity_approvals.student_id
        )
    );

-- Teachers can update approvals for their students
CREATE POLICY "approvals_update_teacher" ON public.activity_approvals
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.activity_approvals.student_id
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.activity_approvals.student_id
        )
    );

-- =====================================================
-- 5. STUDENT_PERFORMANCE TABLE POLICIES
-- =====================================================

-- Students can view their own performance
CREATE POLICY "performance_view_student" ON public.student_performance
    FOR SELECT USING (auth.uid() = student_id);

-- Teachers can view performance of their students
CREATE POLICY "performance_view_teacher" ON public.student_performance
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.student_performance.student_id
        )
    );

-- Teachers can insert performance records for their students
CREATE POLICY "performance_insert_teacher" ON public.student_performance
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.student_performance.student_id
        )
    );

-- Teachers can update performance records for their students
CREATE POLICY "performance_update_teacher" ON public.student_performance
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.student_performance.student_id
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.student_performance.student_id
        )
    );

-- =====================================================
-- 6. FILE_STORAGE TABLE POLICIES
-- =====================================================

-- Users can view their own files
CREATE POLICY "files_view_own" ON public.file_storage
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own files
CREATE POLICY "files_insert_own" ON public.file_storage
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own files
CREATE POLICY "files_update_own" ON public.file_storage
    FOR UPDATE USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own files
CREATE POLICY "files_delete_own" ON public.file_storage
    FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- 7. PLACEMENT_READINESS TABLE POLICIES
-- =====================================================

-- Students can view their own placement readiness
CREATE POLICY "placement_view_student" ON public.placement_readiness
    FOR SELECT USING (auth.uid() = student_id);

-- Teachers can view placement readiness of their students
CREATE POLICY "placement_view_teacher" ON public.placement_readiness
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.placement_readiness.student_id
        )
    );

-- Teachers can insert placement readiness for their students
CREATE POLICY "placement_insert_teacher" ON public.placement_readiness
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.placement_readiness.student_id
        )
    );

-- Teachers can update placement readiness for their students
CREATE POLICY "placement_update_teacher" ON public.placement_readiness
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.placement_readiness.student_id
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.placement_readiness.student_id
        )
    );

-- =====================================================
-- 8. SKILL_ASSESSMENTS TABLE POLICIES
-- =====================================================

-- Students can view their own skill assessments
CREATE POLICY "skills_view_student" ON public.skill_assessments
    FOR SELECT USING (auth.uid() = student_id);

-- Teachers can view skill assessments of their students
CREATE POLICY "skills_view_teacher" ON public.skill_assessments
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.skill_assessments.student_id
        )
    );

-- Teachers can insert skill assessments for their students
CREATE POLICY "skills_insert_teacher" ON public.skill_assessments
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.skill_assessments.student_id
        )
    );

-- Teachers can update skill assessments for their students
CREATE POLICY "skills_update_teacher" ON public.skill_assessments
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.skill_assessments.student_id
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.skill_assessments.student_id
        )
    );

-- =====================================================
-- 9. ACTIVITY_LOGS TABLE POLICIES
-- =====================================================

-- Users can view their own activity logs
CREATE POLICY "logs_view_own" ON public.activity_logs
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own activity logs
CREATE POLICY "logs_insert_own" ON public.activity_logs
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Teachers can view activity logs of their students
CREATE POLICY "logs_view_teacher" ON public.activity_logs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.teacher_student_allocations 
            WHERE teacher_id = auth.uid() AND student_id = public.activity_logs.user_id
        )
    );

-- =====================================================
-- 10. NOTIFICATIONS TABLE POLICIES
-- =====================================================

-- Users can view their own notifications
CREATE POLICY "notifications_view_own" ON public.notifications
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own notifications
CREATE POLICY "notifications_insert_own" ON public.notifications
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own notifications (mark as read)
CREATE POLICY "notifications_update_own" ON public.notifications
    FOR UPDATE USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own notifications
CREATE POLICY "notifications_delete_own" ON public.notifications
    FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- 11. CAREER_PATHS TABLE POLICIES
-- =====================================================

-- All authenticated users can view career paths (public information)
CREATE POLICY "career_paths_view_all" ON public.career_paths
    FOR SELECT USING (auth.role() = 'authenticated');

-- Only authenticated users can insert career paths
CREATE POLICY "career_paths_insert_authenticated" ON public.career_paths
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Only authenticated users can update career paths
CREATE POLICY "career_paths_update_authenticated" ON public.career_paths
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

-- Only authenticated users can delete career paths
CREATE POLICY "career_paths_delete_authenticated" ON public.career_paths
    FOR DELETE USING (auth.role() = 'authenticated');

-- =====================================================
-- 12. ADMIN POLICIES (Optional - for admin users)
-- =====================================================

-- If you have admin users, you can add these policies
-- Uncomment and modify as needed

-- Admin can view all users
-- CREATE POLICY "admin_view_all_users" ON public.users
--     FOR SELECT USING (
--         EXISTS (
--             SELECT 1 FROM public.users 
--             WHERE id = auth.uid() AND role = 'admin'
--         )
--     );

-- Admin can view all allocations
-- CREATE POLICY "admin_view_all_allocations" ON public.teacher_student_allocations
--     FOR SELECT USING (
--         EXISTS (
--             SELECT 1 FROM public.users 
--             WHERE id = auth.uid() AND role = 'admin'
--         )
--     );

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check if RLS is enabled on all tables
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- Check all policies created
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- =====================================================
-- END OF RLS SECURITY FIX
-- =====================================================

