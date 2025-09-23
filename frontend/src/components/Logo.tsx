import React from 'react';
import { Box, Typography } from '@mui/material';
import { School, Group, MenuBook, Psychology, AutoStories, Star, Rocket, Lightbulb } from '@mui/icons-material';

interface LogoProps {
  size?: 'small' | 'medium' | 'large';
  showText?: boolean;
  variant?: 'horizontal' | 'vertical';
}

const Logo: React.FC<LogoProps> = ({ 
  size = 'medium', 
  showText = true, 
  variant = 'horizontal' 
}) => {
  const getSize = () => {
    switch (size) {
      case 'small':
        return { icon: 24, text: 'h6' };
      case 'large':
        return { icon: 48, text: 'h3' };
      default:
        return { icon: 32, text: 'h5' };
    }
  };

  const { icon: iconSize, text: textVariant } = getSize();

  const logoContent = (
    <Box
      display="flex"
      alignItems="center"
      gap={1.5}
      sx={{
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-1px)',
        },
      }}
    >
      {/* Main Icon - Modern School with trending design */}
      <Box
        sx={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2,
        }}
      >
        <School 
          sx={{ 
            color: '#1976d2', 
            fontSize: iconSize,
          }} 
        />
      </Box>

      {showText && (
        <Box
          display="flex"
          flexDirection={variant === 'vertical' ? 'column' : 'row'}
          alignItems={variant === 'vertical' ? 'center' : 'flex-start'}
          gap={0.5}
          sx={{ zIndex: 2, position: 'relative' }}
        >
          <Typography
            variant={textVariant as any}
            sx={{
              color: '#1976d2',
              fontWeight: '700',
              letterSpacing: '0.5px',
              fontSize: size === 'small' ? '1.1rem' : size === 'large' ? '1.8rem' : '1.4rem',
              fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
              textTransform: 'uppercase',
            }}
          >
            Smart Student
          </Typography>
          <Typography
            variant={textVariant as any}
            sx={{
              color: '#1976d2',
              fontWeight: '700',
              letterSpacing: '0.5px',
              fontSize: size === 'small' ? '1.2rem' : size === 'large' ? '2rem' : '1.6rem',
              fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
              textTransform: 'uppercase',
            }}
          >
            Hub
          </Typography>
        </Box>
      )}
    </Box>
  );

  return logoContent;
};

export default Logo;
