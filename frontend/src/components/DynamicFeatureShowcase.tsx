import React, { useState, useEffect } from 'react';
import { Box, Typography, IconButton } from '@mui/material';
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
  Psychology,
  TrendingUp,
  Lightbulb,
  CheckCircle,
  PlayArrow,
  Pause
} from '@mui/icons-material';
import './DynamicFeatureShowcase.css';

interface Feature {
  id: number;
  icon: React.ReactNode;
  title: string;
  description: string;
  gradient: string;
  glowColor: string;
  particles: number;
  accentIcon: React.ReactNode;
  stats?: string;
  highlight?: string;
}

const DynamicFeatureShowcase: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isHovered, setIsHovered] = useState(false);

  const features: Feature[] = [
    {
      id: 1,
      icon: <School sx={{ fontSize: 80, color: '#4CAF50', filter: 'drop-shadow(0 6px 12px rgba(76, 175, 80, 0.6))' }} />,
      accentIcon: <AutoAwesome sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Smart Learning',
      description: 'AI-powered educational platform with personalized learning paths and adaptive content delivery',
      gradient: 'linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%)',
      glowColor: '76, 175, 80',
      particles: 12,
      stats: '95% Success Rate',
      highlight: 'Revolutionary AI'
    },
    {
      id: 2,
      icon: <People sx={{ fontSize: 80, color: '#2196F3', filter: 'drop-shadow(0 6px 12px rgba(33, 150, 243, 0.6))' }} />,
      accentIcon: <Star sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Student Management',
      description: 'Comprehensive student tracking with real-time analytics and performance insights',
      gradient: 'linear-gradient(135deg, #2196F3 0%, #1976d2 50%, #0D47A1 100%)',
      glowColor: '33, 150, 243',
      particles: 10,
      stats: '10K+ Students',
      highlight: 'Real-time Analytics'
    },
    {
      id: 3,
      icon: <Assignment sx={{ fontSize: 80, color: '#FF9800', filter: 'drop-shadow(0 6px 12px rgba(255, 152, 0, 0.6))' }} />,
      accentIcon: <Rocket sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Activity Tracking',
      description: 'Advanced activity monitoring with progress tracking and automated reporting',
      gradient: 'linear-gradient(135deg, #FF9800 0%, #f57c00 50%, #E65100 100%)',
      glowColor: '255, 152, 0',
      particles: 14,
      stats: '99.9% Uptime',
      highlight: 'Live Monitoring'
    },
    {
      id: 4,
      icon: <Analytics sx={{ fontSize: 80, color: '#9C27B0', filter: 'drop-shadow(0 6px 12px rgba(156, 39, 176, 0.6))' }} />,
      accentIcon: <Psychology sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Advanced Analytics',
      description: 'Deep insights into student performance with predictive analytics and recommendations',
      gradient: 'linear-gradient(135deg, #9C27B0 0%, #7b1fa2 50%, #4A148C 100%)',
      glowColor: '156, 39, 176',
      particles: 16,
      stats: '50+ Metrics',
      highlight: 'Predictive AI'
    },
    {
      id: 5,
      icon: <Security sx={{ fontSize: 80, color: '#F44336', filter: 'drop-shadow(0 6px 12px rgba(244, 67, 54, 0.6))' }} />,
      accentIcon: <CheckCircle sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Secure Platform',
      description: 'Enterprise-grade security with end-to-end encryption and compliance standards',
      gradient: 'linear-gradient(135deg, #F44336 0%, #d32f2f 50%, #B71C1C 100%)',
      glowColor: '244, 67, 54',
      particles: 8,
      stats: 'SOC 2 Certified',
      highlight: 'Bank-level Security'
    },
    {
      id: 6,
      icon: <Speed sx={{ fontSize: 80, color: '#00BCD4', filter: 'drop-shadow(0 6px 12px rgba(0, 188, 212, 0.6))' }} />,
      accentIcon: <Rocket sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Lightning Fast',
      description: 'Optimized performance with CDN delivery and instant loading times',
      gradient: 'linear-gradient(135deg, #00BCD4 0%, #0097a7 50%, #006064 100%)',
      glowColor: '0, 188, 212',
      particles: 20,
      stats: '< 100ms Load',
      highlight: 'Ultra Fast'
    },
    {
      id: 7,
      icon: <CloudUpload sx={{ fontSize: 80, color: '#795548', filter: 'drop-shadow(0 6px 12px rgba(121, 85, 72, 0.6))' }} />,
      accentIcon: <Star sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Cloud Storage',
      description: 'Seamless file management with unlimited cloud storage and smart organization',
      gradient: 'linear-gradient(135deg, #795548 0%, #5d4037 50%, #3E2723 100%)',
      glowColor: '121, 85, 72',
      particles: 6,
      stats: 'Unlimited Space',
      highlight: 'Smart Organization'
    },
    {
      id: 8,
      icon: <Notifications sx={{ fontSize: 80, color: '#607D8B', filter: 'drop-shadow(0 6px 12px rgba(96, 125, 139, 0.6))' }} />,
      accentIcon: <Lightbulb sx={{ fontSize: 24, color: '#FFD700' }} />,
      title: 'Smart Notifications',
      description: 'Intelligent alerts with personalized timing and context-aware messaging',
      gradient: 'linear-gradient(135deg, #607D8B 0%, #455a64 50%, #263238 100%)',
      glowColor: '96, 125, 139',
      particles: 9,
      stats: 'Smart Timing',
      highlight: 'Context Aware'
    }
  ];

  // Auto-advance feature
  useEffect(() => {
    if (!isPlaying || isHovered) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % features.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [isPlaying, isHovered, features.length]);

  const currentFeature = features[currentIndex];

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % features.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + features.length) % features.length);
  };

  const togglePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <Box
      className="dynamic-showcase-container"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Control Panel */}
      <Box className="control-panel">
        <IconButton 
          onClick={handlePrev}
          className="control-btn prev-btn"
          size="small"
        >
          ←
        </IconButton>
        
        <IconButton 
          onClick={togglePlayPause}
          className="control-btn play-pause-btn"
          size="small"
        >
          {isPlaying ? <Pause /> : <PlayArrow />}
        </IconButton>
        
        <IconButton 
          onClick={handleNext}
          className="control-btn next-btn"
          size="small"
        >
          →
        </IconButton>
      </Box>

      {/* Progress Indicator */}
      <Box className="progress-indicator">
        {features.map((_, index) => (
          <Box
            key={index}
            className={`progress-dot ${index === currentIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </Box>

      {/* Main Feature Card */}
      <Box
        className="feature-card-main"
        style={{
          background: currentFeature.gradient,
          '--glow-color': currentFeature.glowColor
        } as React.CSSProperties}
      >
        {/* Magical Particles */}
        {Array.from({ length: currentFeature.particles }).map((_, particleIndex) => (
          <div
            key={particleIndex}
            className="magical-particle"
            style={{
              '--delay': `${Math.random() * 2}s`,
              '--duration': `${3 + Math.random() * 3}s`,
              '--glow-color': currentFeature.glowColor
            } as React.CSSProperties}
          />
        ))}

        {/* Animated Background */}
        <div className="animated-background" />

        {/* Floating Accent Icon */}
        <div className="floating-accent">
          {currentFeature.accentIcon}
        </div>

        {/* Corner Decorations */}
        <div className="corner-decoration top-left" />
        <div className="corner-decoration top-right" />
        <div className="corner-decoration bottom-left" />
        <div className="corner-decoration bottom-right" />

        {/* Content */}
        <Box className="feature-content">
          <Box className="icon-container">
            {currentFeature.icon}
            <div className="icon-glow-ring" />
          </Box>

          <Typography className="feature-title">
            {currentFeature.title}
          </Typography>

          <Typography className="feature-description">
            {currentFeature.description}
          </Typography>

          <Box className="feature-stats">
            <Box className="stat-item">
              <Typography className="stat-value">
                {currentFeature.stats}
              </Typography>
            </Box>
            <Box className="highlight-badge">
              {currentFeature.highlight}
            </Box>
          </Box>
        </Box>

        {/* Shimmer Effect */}
        <div className="shimmer-effect" />
      </Box>

      {/* Feature Counter */}
      <Box className="feature-counter">
        <Typography variant="body2">
          {currentIndex + 1} / {features.length}
        </Typography>
      </Box>
    </Box>
  );
};

export default DynamicFeatureShowcase;
