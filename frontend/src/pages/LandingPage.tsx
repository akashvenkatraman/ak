import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Paper,
  IconButton,
  useTheme,
  useMediaQuery,
  Fade,
  Slide,
  Zoom,
  Grow
} from '@mui/material';
import {
  School,
  People,
  Assignment,
  Analytics,
  Security,
  Speed,
  CloudUpload,
  Dashboard,
  TrendingUp,
  CheckCircle,
  ArrowForward,
  Menu as MenuIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { keyframes } from '@mui/system';

// Animation keyframes
const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
`;

const pulse = keyframes`
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
`;

const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
`;

const slideInRight = keyframes`
  from { opacity: 0; transform: translateX(50px); }
  to { opacity: 1; transform: translateX(0); }
`;

const fadeInUp = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

const gradientShift = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const LandingPage: React.FC = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleGetStarted = () => {
    navigate('/login');
  };

  const features = [
    {
      icon: <School sx={{ fontSize: 40 }} />,
      title: "Student Management",
      description: "Comprehensive student profiles, activity tracking, and performance analytics."
    },
    {
      icon: <People sx={{ fontSize: 40 }} />,
      title: "Teacher Dashboard",
      description: "Review student activities, approve submissions, and manage allocations."
    },
    {
      icon: <Assignment sx={{ fontSize: 40 }} />,
      title: "Activity Tracking",
      description: "Students can submit activities with documents and images for review."
    },
    {
      icon: <Analytics sx={{ fontSize: 40 }} />,
      title: "Analytics & Reports",
      description: "Detailed insights into student performance and activity trends."
    },
    {
      icon: <Security sx={{ fontSize: 40 }} />,
      title: "Secure Storage",
      description: "User-specific file storage with advanced security and privacy."
    },
    {
      icon: <Speed sx={{ fontSize: 40 }} />,
      title: "Real-time Updates",
      description: "Instant notifications and live updates for all activities."
    }
  ];

  const stats = [
    { number: "1000+", label: "Students" },
    { number: "50+", label: "Teachers" },
    { number: "5000+", label: "Activities" },
    { number: "99.9%", label: "Uptime" }
  ];

  const renderHomeSection = () => (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          minHeight: '100vh',
          background: `
            linear-gradient(135deg, 
              #1e3c72 0%, 
              #2a5298 25%, 
              #87ceeb 50%, 
              #98fb98 75%, 
              #f0e68c 100%
            )
          `,
          backgroundSize: '400% 400%',
          animation: `${gradientShift} 15s ease infinite`,
          display: 'flex',
          alignItems: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {/* Background Elements */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `
              radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(135, 206, 235, 0.2) 0%, transparent 50%),
              radial-gradient(circle at 40% 40%, rgba(152, 251, 152, 0.15) 0%, transparent 60%)
            `,
            zIndex: 0
          }}
        />

        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 4, alignItems: 'center' }}>
            <Box sx={{ flex: 1 }}>
              <Fade in={isVisible} timeout={1000}>
                <Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2, animation: `${slideInLeft} 1s ease-out` }}>
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: { xs: 80, md: 120 },
                        height: { xs: 80, md: 120 },
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%)',
                        boxShadow: '0 8px 32px rgba(255, 255, 255, 0.3)',
                        mr: 3,
                        position: 'relative',
                        overflow: 'hidden',
                        '&::before': {
                          content: '""',
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          bottom: 0,
                          background: 'linear-gradient(135deg, rgba(30, 60, 114, 0.1) 0%, rgba(42, 82, 152, 0.1) 100%)',
                          borderRadius: '50%'
                        }
                      }}
                    >
                      <School 
                        sx={{ 
                          fontSize: { xs: 40, md: 60 }, 
                          color: '#1e3c72',
                          zIndex: 1,
                          filter: 'drop-shadow(0 4px 8px rgba(30, 60, 114, 0.3))'
                        }} 
                      />
                    </Box>
                    <Typography
                      variant="h1"
                      sx={{
                        fontSize: { xs: '2.5rem', md: '4rem' },
                        fontWeight: 800,
                        background: 'linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%)',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        textShadow: '0 4px 8px rgba(0,0,0,0.3)',
                        lineHeight: 1.1
                      }}
                    >
                      Smart Student Hub
                    </Typography>
                  </Box>
                  <Typography
                    variant="h5"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.9)',
                      mb: 3,
                      fontWeight: 500,
                      animation: `${slideInLeft} 1s ease-out 0.2s both`
                    }}
                  >
                    Revolutionizing Education Management
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.8)',
                      mb: 4,
                      fontSize: '1.1rem',
                      lineHeight: 1.6,
                      animation: `${slideInLeft} 1s ease-out 0.4s both`
                    }}
                  >
                    A comprehensive platform for students, teachers, and administrators to manage 
                    educational activities, track progress, and collaborate effectively.
                  </Typography>
                  <Box sx={{ animation: `${slideInLeft} 1s ease-out 0.6s both` }}>
                    <Button
                      variant="contained"
                      size="large"
                      onClick={handleGetStarted}
                      endIcon={<ArrowForward />}
                      sx={{
                        background: 'linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%)',
                        color: '#1e3c72',
                        px: 4,
                        py: 1.5,
                        fontSize: '1.1rem',
                        fontWeight: 600,
                        borderRadius: 3,
                        boxShadow: '0 8px 32px rgba(255, 255, 255, 0.3)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%)',
                          transform: 'translateY(-2px)',
                          boxShadow: '0 12px 40px rgba(255, 255, 255, 0.4)'
                        },
                        transition: 'all 0.3s ease-in-out'
                      }}
                    >
                      Get Started
                    </Button>
                  </Box>
                </Box>
              </Fade>
            </Box>
            <Box sx={{ flex: 1 }}>
              <Fade in={isVisible} timeout={1000} style={{ transitionDelay: '0.3s' }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    animation: `${float} 6s ease-in-out infinite`
                  }}
                >
                  <Paper
                    elevation={24}
                    sx={{
                      p: 4,
                      borderRadius: 4,
                      background: 'rgba(255, 255, 255, 0.95)',
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                      maxWidth: 400,
                      width: '100%'
                    }}
                  >
                    <Box sx={{ textAlign: 'center' }}>
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: 120,
                          height: 120,
                          borderRadius: '50%',
                          background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                          mx: 'auto',
                          mb: 3,
                          boxShadow: '0 12px 40px rgba(30, 60, 114, 0.4)',
                          position: 'relative',
                          overflow: 'hidden',
                          '&::before': {
                            content: '""',
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(240, 248, 255, 0.1) 100%)',
                            borderRadius: '50%'
                          }
                        }}
                      >
                        <School 
                          sx={{ 
                            fontSize: 60, 
                            color: 'white',
                            zIndex: 1,
                            filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3))'
                          }} 
                        />
                      </Box>
                      <Typography variant="h4" sx={{ color: '#1e3c72', fontWeight: 700, mb: 1 }}>
                        Education Hub
                      </Typography>
                      <Typography variant="body1" sx={{ color: '#666' }}>
                        Your gateway to smart education management
                      </Typography>
                    </Box>
                  </Paper>
                </Box>
              </Fade>
            </Box>
          </Box>
        </Container>
      </Box>

      {/* Stats Section */}
      <Box sx={{ py: 8, background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)' }}>
        <Container maxWidth="lg">
          <Fade in={isVisible} timeout={1000}>
            <Box sx={{ textAlign: 'center', mb: 6 }}>
              <Typography variant="h3" sx={{ color: '#1e3c72', fontWeight: 700, mb: 2 }}>
                Trusted by Thousands
              </Typography>
              <Typography variant="h6" sx={{ color: '#666' }}>
                Join the growing community of educational institutions
              </Typography>
            </Box>
          </Fade>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4, justifyContent: 'center' }}>
            {stats.map((stat, index) => (
              <Box key={index} sx={{ flex: '1 1 200px', minWidth: '200px', maxWidth: '250px' }}>
                <Grow in={isVisible} timeout={1000} style={{ transitionDelay: `${index * 0.1}s` }}>
                  <Card
                    sx={{
                      textAlign: 'center',
                      p: 3,
                      borderRadius: 3,
                      background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
                      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: '0 16px 48px rgba(0, 0, 0, 0.15)'
                      },
                      transition: 'all 0.3s ease-in-out'
                    }}
                  >
                    <Typography variant="h3" sx={{ color: '#1e3c72', fontWeight: 800, mb: 1 }}>
                      {stat.number}
                    </Typography>
                    <Typography variant="h6" sx={{ color: '#666' }}>
                      {stat.label}
                    </Typography>
                  </Card>
                </Grow>
              </Box>
            ))}
          </Box>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 8, background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)' }}>
        <Container maxWidth="lg">
          <Fade in={isVisible} timeout={1000}>
            <Box sx={{ textAlign: 'center', mb: 6 }}>
              <Typography variant="h3" sx={{ color: 'white', fontWeight: 700, mb: 2 }}>
                Powerful Features
              </Typography>
              <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                Everything you need for modern education management
              </Typography>
            </Box>
          </Fade>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4, justifyContent: 'center' }}>
            {features.map((feature, index) => (
              <Box key={index} sx={{ flex: '1 1 300px', minWidth: '300px', maxWidth: '400px' }}>
                <Slide direction="up" in={isVisible} timeout={1000} style={{ transitionDelay: `${index * 0.1}s` }}>
                  <Card
                    sx={{
                      p: 3,
                      height: '100%',
                      borderRadius: 3,
                      background: 'rgba(255, 255, 255, 0.95)',
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: '0 16px 48px rgba(0, 0, 0, 0.2)'
                      },
                      transition: 'all 0.3s ease-in-out'
                    }}
                  >
                    <Box sx={{ textAlign: 'center', mb: 2 }}>
                      <Box
                        sx={{
                          display: 'inline-flex',
                          p: 2,
                          borderRadius: '50%',
                          background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                          color: 'white',
                          mb: 2,
                          animation: `${pulse} 2s ease-in-out infinite`
                        }}
                      >
                        {feature.icon}
                      </Box>
                    </Box>
                    <Typography variant="h5" sx={{ color: '#1e3c72', fontWeight: 600, mb: 2, textAlign: 'center' }}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#666', textAlign: 'center' }}>
                      {feature.description}
                    </Typography>
                  </Card>
                </Slide>
              </Box>
            ))}
          </Box>
        </Container>
      </Box>
    </Box>
  );

  const renderMoreInfoSection = () => (
    <Box sx={{ minHeight: '100vh', py: 8, background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)' }}>
      <Container maxWidth="lg">
        <Fade in={isVisible} timeout={1000}>
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h3" sx={{ color: '#1e3c72', fontWeight: 700, mb: 2 }}>
              More Information
            </Typography>
            <Typography variant="h6" sx={{ color: '#666' }}>
              Learn more about our platform and capabilities
            </Typography>
          </Box>
        </Fade>

        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 6 }}>
          <Box sx={{ flex: 1 }}>
            <Zoom in={isVisible} timeout={1000}>
              <Card
                sx={{
                  p: 4,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                  height: '100%'
                }}
              >
                <Dashboard sx={{ fontSize: 60, color: '#1e3c72', mb: 2 }} />
                <Typography variant="h5" sx={{ color: '#1e3c72', fontWeight: 600, mb: 2 }}>
                  Student Dashboard
                </Typography>
                <Typography variant="body1" sx={{ color: '#666', mb: 3 }}>
                  Students can view their activities, track progress, upload documents, 
                  and monitor their performance with detailed analytics and insights.
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {['Activity Tracking', 'Document Upload', 'Progress Analytics', 'Performance Reports'].map((item, index) => (
                    <Box
                      key={index}
                      sx={{
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                        color: 'white',
                        fontSize: '0.8rem',
                        fontWeight: 500
                      }}
                    >
                      {item}
                    </Box>
                  ))}
                </Box>
              </Card>
            </Zoom>
          </Box>

          <Box sx={{ flex: 1 }}>
            <Zoom in={isVisible} timeout={1000} style={{ transitionDelay: '0.2s' }}>
              <Card
                sx={{
                  p: 4,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                  height: '100%'
                }}
              >
                <People sx={{ fontSize: 60, color: '#1e3c72', mb: 2 }} />
                <Typography variant="h5" sx={{ color: '#1e3c72', fontWeight: 600, mb: 2 }}>
                  Teacher Management
                </Typography>
                <Typography variant="body1" sx={{ color: '#666', mb: 3 }}>
                  Teachers can review student submissions, approve activities, 
                  manage student allocations, and provide feedback efficiently.
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {['Activity Review', 'Student Allocation', 'Approval System', 'Feedback Tools'].map((item, index) => (
                    <Box
                      key={index}
                      sx={{
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                        color: 'white',
                        fontSize: '0.8rem',
                        fontWeight: 500
                      }}
                    >
                      {item}
                    </Box>
                  ))}
                </Box>
              </Card>
            </Zoom>
          </Box>

          <Box sx={{ flex: 1 }}>
            <Zoom in={isVisible} timeout={1000} style={{ transitionDelay: '0.4s' }}>
              <Card
                sx={{
                  p: 4,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                  height: '100%'
                }}
              >
                <Analytics sx={{ fontSize: 60, color: '#1e3c72', mb: 2 }} />
                <Typography variant="h5" sx={{ color: '#1e3c72', fontWeight: 600, mb: 2 }}>
                  Admin Analytics
                </Typography>
                <Typography variant="body1" sx={{ color: '#666', mb: 3 }}>
                  Administrators get comprehensive insights, user management tools, 
                  and system-wide analytics to make informed decisions.
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {['User Management', 'System Analytics', 'Performance Reports', 'Data Insights'].map((item, index) => (
                    <Box
                      key={index}
                      sx={{
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                        color: 'white',
                        fontSize: '0.8rem',
                        fontWeight: 500
                      }}
                    >
                      {item}
                    </Box>
                  ))}
                </Box>
              </Card>
            </Zoom>
          </Box>

          <Box sx={{ flex: 1 }}>
            <Zoom in={isVisible} timeout={1000} style={{ transitionDelay: '0.6s' }}>
              <Card
                sx={{
                  p: 4,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                  height: '100%'
                }}
              >
                <CloudUpload sx={{ fontSize: 60, color: '#1e3c72', mb: 2 }} />
                <Typography variant="h5" sx={{ color: '#1e3c72', fontWeight: 600, mb: 2 }}>
                  Secure Storage
                </Typography>
                <Typography variant="body1" sx={{ color: '#666', mb: 3 }}>
                  Advanced file storage system with user-specific buckets, 
                  secure uploads, and organized document management.
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {['User Buckets', 'Secure Upload', 'File Management', 'Privacy Control'].map((item, index) => (
                    <Box
                      key={index}
                      sx={{
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                        color: 'white',
                        fontSize: '0.8rem',
                        fontWeight: 500
                      }}
                    >
                      {item}
                    </Box>
                  ))}
                </Box>
              </Card>
            </Zoom>
          </Box>
        </Box>
      </Container>
    </Box>
  );

  const renderGetStartedSection = () => (
    <Box sx={{ minHeight: '100vh', py: 8, background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)' }}>
      <Container maxWidth="lg">
        <Fade in={isVisible} timeout={1000}>
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h3" sx={{ color: 'white', fontWeight: 700, mb: 2 }}>
              Ready to Get Started?
            </Typography>
            <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
              Join thousands of students and teachers already using our platform
            </Typography>
          </Box>
        </Fade>

        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 6, alignItems: 'center' }}>
          <Box sx={{ flex: 1 }}>
            <Slide direction="right" in={isVisible} timeout={1000}>
              <Box>
                <Typography variant="h4" sx={{ color: 'white', fontWeight: 600, mb: 3 }}>
                  Why Choose Smart Student Hub?
                </Typography>
                {[
                  "Comprehensive activity tracking and management",
                  "Secure file storage with user-specific buckets",
                  "Real-time notifications and updates",
                  "Advanced analytics and reporting",
                  "User-friendly interface with modern design",
                  "Scalable architecture for growing institutions"
                ].map((item, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CheckCircle sx={{ color: '#98fb98', mr: 2 }} />
                    <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                      {item}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Slide>
          </Box>

          <Box sx={{ flex: 1 }}>
            <Slide direction="left" in={isVisible} timeout={1000}>
              <Box sx={{ textAlign: 'center' }}>
                <Paper
                  elevation={24}
                  sx={{
                    p: 6,
                    borderRadius: 4,
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.3)'
                  }}
                >
                  <TrendingUp sx={{ fontSize: 80, color: '#1e3c72', mb: 3 }} />
                  <Typography variant="h4" sx={{ color: '#1e3c72', fontWeight: 700, mb: 2 }}>
                    Start Your Journey
                  </Typography>
                  <Typography variant="body1" sx={{ color: '#666', mb: 4 }}>
                    Create your account and experience the future of education management
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={handleGetStarted}
                    endIcon={<ArrowForward />}
                    sx={{
                      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                      px: 6,
                      py: 2,
                      fontSize: '1.2rem',
                      fontWeight: 600,
                      borderRadius: 3,
                      boxShadow: '0 8px 32px rgba(30, 60, 114, 0.4)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #1a3462 0%, #1e3c72 100%)',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 12px 40px rgba(30, 60, 114, 0.5)'
                      },
                      transition: 'all 0.3s ease-in-out'
                    }}
                  >
                    Get Started Now
                  </Button>
                </Paper>
              </Box>
            </Slide>
          </Box>
        </Box>
      </Container>
    </Box>
  );

  return (
    <Box>
      {/* Navigation */}
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 1000,
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', py: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                  mr: 2,
                  boxShadow: '0 4px 12px rgba(30, 60, 114, 0.3)'
                }}
              >
                <School 
                  sx={{ 
                    fontSize: 24, 
                    color: 'white',
                    filter: 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2))'
                  }} 
                />
              </Box>
              <Typography
                variant="h5"
                sx={{
                  fontWeight: 700,
                  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent'
                }}
              >
                Smart Student Hub
              </Typography>
            </Box>
            
            {isMobile ? (
              <IconButton onClick={() => setIsMenuOpen(!isMenuOpen)}>
                {isMenuOpen ? <CloseIcon /> : <MenuIcon />}
              </IconButton>
            ) : (
              <Box sx={{ display: 'flex', gap: 2 }}>
                {['home', 'moreinfo', 'getstarted'].map((section) => (
                  <Button
                    key={section}
                    onClick={() => setActiveSection(section)}
                    sx={{
                      color: activeSection === section ? '#1e3c72' : '#666',
                      fontWeight: activeSection === section ? 600 : 400,
                      textTransform: 'capitalize',
                      '&:hover': {
                        color: '#1e3c72',
                        background: 'rgba(30, 60, 114, 0.1)'
                      }
                    }}
                  >
                    {section === 'moreinfo' ? 'More Info' : section === 'getstarted' ? 'Get Started' : 'Home'}
                  </Button>
                ))}
              </Box>
            )}
          </Box>
        </Container>
      </Box>

      {/* Mobile Menu */}
      {isMobile && isMenuOpen && (
        <Box
          sx={{
            position: 'fixed',
            top: 70,
            left: 0,
            right: 0,
            background: 'rgba(255, 255, 255, 0.98)',
            backdropFilter: 'blur(20px)',
            zIndex: 999,
            p: 2,
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
          }}
        >
          {['home', 'moreinfo', 'getstarted'].map((section) => (
            <Button
              key={section}
              fullWidth
              onClick={() => {
                setActiveSection(section);
                setIsMenuOpen(false);
              }}
              sx={{
                color: activeSection === section ? '#1e3c72' : '#666',
                fontWeight: activeSection === section ? 600 : 400,
                textTransform: 'capitalize',
                justifyContent: 'flex-start',
                py: 2
              }}
            >
              {section === 'moreinfo' ? 'More Info' : section === 'getstarted' ? 'Get Started' : 'Home'}
            </Button>
          ))}
        </Box>
      )}

      {/* Content */}
      <Box sx={{ pt: 8 }}>
        {activeSection === 'home' && renderHomeSection()}
        {activeSection === 'moreinfo' && renderMoreInfoSection()}
        {activeSection === 'getstarted' && renderGetStartedSection()}
      </Box>
    </Box>
  );
};

export default LandingPage;
