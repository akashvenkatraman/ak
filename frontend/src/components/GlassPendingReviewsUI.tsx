import React from 'react';
import { Box, Typography, IconButton, Avatar } from '@mui/material';
import {
  Pending as PendingIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Search as SearchIcon
} from '@mui/icons-material';


interface GlassPendingReviewsUIProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

const GlassPendingReviewsUI: React.FC<GlassPendingReviewsUIProps> = ({ 
  children, 
  title = "Pending Reviews Dashboard",
  subtitle = "Manage student activities, approvals, and submissions"
}) => {

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: '#ffffff',
        position: 'relative',
        overflow: 'hidden'
      }}
    >


      {/* Main Content Container */}
      <Box sx={{ position: 'relative', zIndex: 1, minHeight: '100vh' }}>
        {/* Clean White Header */}
        <Box
          sx={{
            background: '#ffffff',
            borderBottom: '1px solid #e0e0e0',
            p: 4,
            mb: 3,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
          }}
        >
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={2}>
              <Avatar
                sx={{
                  bgcolor: '#1976d2',
                  width: 60,
                  height: 60,
                  boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)'
                }}
              >
                <PendingIcon sx={{ fontSize: 30, color: 'white' }} />
              </Avatar>
              <Box>
                <Typography variant="h4" sx={{ 
                  color: '#1976d2', 
                  fontWeight: 'bold', 
                  mb: 0.5,
                  textShadow: '0 2px 4px rgba(25, 118, 210, 0.3)'
                }}>
                  {title}
                </Typography>
                <Typography variant="body1" sx={{ color: '#666' }}>
                  {subtitle}
                </Typography>
              </Box>
            </Box>
            <Box display="flex" gap={1}>
              <IconButton
                sx={{
                  color: '#1976d2',
                  background: 'rgba(25, 118, 210, 0.1)',
                  border: '1px solid rgba(25, 118, 210, 0.3)',
                  '&:hover': {
                    background: 'rgba(25, 118, 210, 0.2)'
                  }
                }}
              >
                <SearchIcon />
              </IconButton>
              <IconButton
                sx={{
                  color: '#1976d2',
                  background: 'rgba(25, 118, 210, 0.1)',
                  border: '1px solid rgba(25, 118, 210, 0.3)',
                  '&:hover': {
                    background: 'rgba(25, 118, 210, 0.2)'
                  }
                }}
              >
                <FilterIcon />
              </IconButton>
              <IconButton
                sx={{
                  color: '#1976d2',
                  background: 'rgba(25, 118, 210, 0.1)',
                  border: '1px solid rgba(25, 118, 210, 0.3)',
                  '&:hover': {
                    background: 'rgba(25, 118, 210, 0.2)'
                  }
                }}
              >
                <RefreshIcon />
              </IconButton>
            </Box>
          </Box>
        </Box>


        {/* Main Content Area with Clean White Theme */}
        <Box
          sx={{
            background: '#ffffff',
            minHeight: '60vh',
            position: 'relative',
            overflow: 'hidden',
            mx: 2,
            borderRadius: '16px 16px 0 0',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e0e0e0'
          }}
        >
          <Box sx={{ position: 'relative', zIndex: 1, p: 4 }}>
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

export default GlassPendingReviewsUI;
