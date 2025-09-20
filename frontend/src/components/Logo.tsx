import React from 'react';
import { Box, Typography } from '@mui/material';
import { School, Group, MenuBook, Psychology, AutoStories } from '@mui/icons-material';

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
      gap={1}
      sx={{
        background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%)',
        borderRadius: 2,
        p: 1.5,
        boxShadow: '0 4px 12px rgba(30, 58, 138, 0.4)',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%)',
          animation: 'shimmer 2s infinite',
        },
        '@keyframes shimmer': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      }}
    >
      {/* Main Icon - School building with educational elements */}
      <Box
        sx={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <School 
          sx={{ 
            color: 'white', 
            fontSize: iconSize,
            filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))',
          }} 
        />
        {/* Book icon accent */}
        <Box
          sx={{
            position: 'absolute',
            top: -3,
            right: -3,
            width: iconSize * 0.35,
            height: iconSize * 0.35,
            background: 'linear-gradient(45deg, #ffd700, #ffed4e)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
          }}
        >
          <MenuBook 
            sx={{ 
              color: '#1976d2', 
              fontSize: iconSize * 0.2,
            }} 
          />
        </Box>
        {/* Brain/learning icon */}
        <Box
          sx={{
            position: 'absolute',
            top: -2,
            left: -2,
            width: iconSize * 0.3,
            height: iconSize * 0.3,
            background: 'rgba(255,255,255,0.9)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
          }}
        >
          <Psychology 
            sx={{ 
              color: '#1976d2', 
              fontSize: iconSize * 0.15,
            }} 
          />
        </Box>
      </Box>

      {/* Students/learning icon */}
      <Box
        sx={{
          position: 'absolute',
          bottom: -2,
          right: -2,
          width: iconSize * 0.35,
          height: iconSize * 0.35,
          background: 'rgba(255,255,255,0.9)',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        }}
      >
        <Group 
          sx={{ 
            color: '#1976d2', 
            fontSize: iconSize * 0.2,
          }} 
        />
      </Box>
      
      {/* Story/learning journey icon */}
      <Box
        sx={{
          position: 'absolute',
          bottom: -2,
          left: -2,
          width: iconSize * 0.3,
          height: iconSize * 0.3,
          background: 'linear-gradient(45deg, #4caf50, #8bc34a)',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        }}
      >
        <AutoStories 
          sx={{ 
            color: 'white', 
            fontSize: iconSize * 0.15,
          }} 
        />
      </Box>

      {showText && (
        <Box
          display="flex"
          flexDirection={variant === 'vertical' ? 'column' : 'row'}
          alignItems={variant === 'vertical' ? 'center' : 'flex-start'}
          gap={0.5}
        >
          <Typography
            variant={textVariant as any}
            sx={{
              color: 'white',
              fontWeight: 'bold',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)',
              letterSpacing: '0.5px',
            }}
          >
            Smart Student
          </Typography>
          <Typography
            variant={textVariant as any}
            sx={{
              color: 'rgba(255,255,255,0.9)',
              fontWeight: '600',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)',
              letterSpacing: '0.5px',
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
