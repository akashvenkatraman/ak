import React from 'react';
import { Card } from './CardSwap';
import { 
  School, 
  People, 
  Assignment, 
  Analytics, 
  Security, 
  Speed,
  CloudUpload,
  Notifications,
  AutoAwesome,
  Star,
  Rocket,
  Psychology
} from '@mui/icons-material';

const FeatureCards: React.FC = () => {
  console.log('FeatureCards component rendering');
  
  const features = [
    {
      icon: <School sx={{ fontSize: 60, color: '#4CAF50', filter: 'drop-shadow(0 4px 8px rgba(76, 175, 80, 0.4))' }} />,
      accentIcon: <AutoAwesome sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Smart Learning',
      description: 'AI-powered educational platform with personalized learning paths',
      gradient: 'linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%)',
      glowColor: '76, 175, 80',
      particles: 8
    },
    {
      icon: <People sx={{ fontSize: 60, color: '#2196F3', filter: 'drop-shadow(0 4px 8px rgba(33, 150, 243, 0.4))' }} />,
      accentIcon: <Star sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Student Management',
      description: 'Comprehensive student tracking and performance analytics',
      gradient: 'linear-gradient(135deg, #2196F3 0%, #1976d2 50%, #0D47A1 100%)',
      glowColor: '33, 150, 243',
      particles: 6
    },
    {
      icon: <Assignment sx={{ fontSize: 60, color: '#FF9800', filter: 'drop-shadow(0 4px 8px rgba(255, 152, 0, 0.4))' }} />,
      accentIcon: <Rocket sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Activity Tracking',
      description: 'Real-time activity monitoring and progress tracking',
      gradient: 'linear-gradient(135deg, #FF9800 0%, #f57c00 50%, #E65100 100%)',
      glowColor: '255, 152, 0',
      particles: 7
    },
    {
      icon: <Analytics sx={{ fontSize: 60, color: '#9C27B0', filter: 'drop-shadow(0 4px 8px rgba(156, 39, 176, 0.4))' }} />,
      accentIcon: <Psychology sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Advanced Analytics',
      description: 'Deep insights into student performance and engagement',
      gradient: 'linear-gradient(135deg, #9C27B0 0%, #7b1fa2 50%, #4A148C 100%)',
      glowColor: '156, 39, 176',
      particles: 9
    },
    {
      icon: <Security sx={{ fontSize: 60, color: '#F44336', filter: 'drop-shadow(0 4px 8px rgba(244, 67, 54, 0.4))' }} />,
      accentIcon: <AutoAwesome sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Secure Platform',
      description: 'Enterprise-grade security with end-to-end encryption',
      gradient: 'linear-gradient(135deg, #F44336 0%, #d32f2f 50%, #B71C1C 100%)',
      glowColor: '244, 67, 54',
      particles: 5
    },
    {
      icon: <Speed sx={{ fontSize: 60, color: '#00BCD4', filter: 'drop-shadow(0 4px 8px rgba(0, 188, 212, 0.4))' }} />,
      accentIcon: <Rocket sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Lightning Fast',
      description: 'Optimized performance with instant loading times',
      gradient: 'linear-gradient(135deg, #00BCD4 0%, #0097a7 50%, #006064 100%)',
      glowColor: '0, 188, 212',
      particles: 12
    },
    {
      icon: <CloudUpload sx={{ fontSize: 60, color: '#795548', filter: 'drop-shadow(0 4px 8px rgba(121, 85, 72, 0.4))' }} />,
      accentIcon: <Star sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Cloud Storage',
      description: 'Seamless file management with unlimited cloud storage',
      gradient: 'linear-gradient(135deg, #795548 0%, #5d4037 50%, #3E2723 100%)',
      glowColor: '121, 85, 72',
      particles: 4
    },
    {
      icon: <Notifications sx={{ fontSize: 60, color: '#607D8B', filter: 'drop-shadow(0 4px 8px rgba(96, 125, 139, 0.4))' }} />,
      accentIcon: <Psychology sx={{ fontSize: 20, color: '#FFD700' }} />,
      title: 'Smart Notifications',
      description: 'Intelligent alerts and real-time updates',
      gradient: 'linear-gradient(135deg, #607D8B 0%, #455a64 50%, #263238 100%)',
      glowColor: '96, 125, 139',
      particles: 6
    }
  ];

  return (
    <>
      {features.map((feature, index) => (
        <Card
          key={index}
          customClass="feature-card"
           style={{
             background: feature.gradient,
             display: 'flex',
             flexDirection: 'column',
             alignItems: 'center',
             justifyContent: 'center',
             padding: '1.5rem',
             textAlign: 'center',
             color: 'white',
             boxShadow: `0 25px 50px rgba(0,0,0,0.4), 0 0 60px rgba(${feature.glowColor}, 0.3)`,
             border: `2px solid rgba(255,255,255,0.3)`,
             backdropFilter: 'blur(15px)',
             position: 'relative',
             overflow: 'hidden',
             cursor: 'pointer',
             transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
             transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg)',
             '--glow-color': feature.glowColor,
             minWidth: '300px',
             minHeight: '200px',
             opacity: 0.7
           } as React.CSSProperties}
        >
           {/* Magical Particles */}
           {Array.from({ length: feature.particles }).map((_, particleIndex) => (
             <div
               key={particleIndex}
               style={{
                 position: 'absolute',
                 width: '3px',
                 height: '3px',
                 background: `rgba(${feature.glowColor}, 0.5)`,
                 borderRadius: '50%',
                 top: `${Math.random() * 100}%`,
                 left: `${Math.random() * 100}%`,
                 animation: `float ${3 + Math.random() * 4}s ease-in-out infinite`,
                 animationDelay: `${Math.random() * 2}s`,
                 boxShadow: `0 0 6px rgba(${feature.glowColor}, 0.4)`,
                 pointerEvents: 'none'
               }}
             />
           ))}

           {/* Animated background pattern */}
           <div
             style={{
               position: 'absolute',
               top: 0,
               left: 0,
               right: 0,
               bottom: 0,
               background: `
                 radial-gradient(circle at 20% 20%, rgba(255,255,255,0.08) 0%, transparent 50%),
                 radial-gradient(circle at 80% 80%, rgba(255,255,255,0.08) 0%, transparent 50%),
                 radial-gradient(circle at 50% 50%, rgba(255,255,255,0.04) 0%, transparent 50%),
                 linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.03) 50%, transparent 70%)
               `,
               animation: 'shimmer 4s ease-in-out infinite, float 8s ease-in-out infinite'
             }}
           />

          {/* Floating accent icon */}
          <div
            style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              animation: 'orbit 6s linear infinite',
              zIndex: 3
            }}
          >
            {feature.accentIcon}
          </div>

          {/* Corner decorations */}
          <div
            style={{
              position: 'absolute',
              top: '8px',
              left: '8px',
              width: '20px',
              height: '20px',
              border: `2px solid rgba(${feature.glowColor}, 0.6)`,
              borderRight: 'none',
              borderBottom: 'none',
              borderRadius: '4px 0 0 0',
              animation: 'pulse 2s ease-in-out infinite'
            }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: '8px',
              right: '8px',
              width: '20px',
              height: '20px',
              border: `2px solid rgba(${feature.glowColor}, 0.6)`,
              borderLeft: 'none',
              borderTop: 'none',
              borderRadius: '0 0 4px 0',
              animation: 'pulse 2s ease-in-out infinite 1s'
            }}
          />
          
          {/* Content */}
          <div style={{ position: 'relative', zIndex: 2 }}>
            <div style={{ 
              marginBottom: '1.5rem',
              position: 'relative',
              animation: 'float 3s ease-in-out infinite'
            }}>
              {feature.icon}
              {/* Icon glow ring */}
              <div
                style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  width: '80px',
                  height: '80px',
                  border: `2px solid rgba(${feature.glowColor}, 0.3)`,
                  borderRadius: '50%',
                  transform: 'translate(-50%, -50%)',
                  animation: 'pulse 3s ease-in-out infinite',
                  pointerEvents: 'none'
                }}
              />
            </div>
             <h3 style={{ 
               fontSize: '1.6rem', 
               fontWeight: '800', 
               marginBottom: '1rem',
               textShadow: '0 2px 4px rgba(0,0,0,0.5), 0 0 20px rgba(255,255,255,0.3)',
               background: 'linear-gradient(45deg, rgba(255,255,255,0.9) 0%, rgba(240,240,240,0.8) 50%, rgba(255,255,255,0.9) 100%)',
               backgroundClip: 'text',
               WebkitBackgroundClip: 'text',
               WebkitTextFillColor: 'transparent',
               animation: 'textGlow 2s ease-in-out infinite alternate',
               letterSpacing: '1px'
             }}>
               {feature.title}
             </h3>
             <p style={{ 
               fontSize: '0.9rem', 
               opacity: 0.8,
               lineHeight: '1.4',
               textShadow: '0 1px 3px rgba(0,0,0,0.4)',
               fontWeight: '500',
               maxWidth: '250px'
             }}>
               {feature.description}
             </p>
          </div>

          {/* Enhanced glow effect */}
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              borderRadius: '12px',
              boxShadow: `inset 0 0 30px rgba(255,255,255,0.1), inset 0 0 60px rgba(${feature.glowColor}, 0.1)`,
              pointerEvents: 'none'
            }}
          />

          {/* Hover effect overlay */}
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: `linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%)`,
              opacity: 0,
              transition: 'opacity 0.3s ease',
              pointerEvents: 'none',
              borderRadius: '12px'
            }}
            className="hover-overlay"
          />
        </Card>
      ))}
    </>
  );
};

export default FeatureCards;
