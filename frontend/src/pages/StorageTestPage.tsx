import React, { useState } from 'react';
import {
  Box,
  Typography,
  Container,
  Paper,
  Tabs,
  Tab,
  Alert
} from '@mui/material';
import {
  CloudUpload,
  Storage,
  Image,
  Description
} from '@mui/icons-material';
import FileUpload from '../components/FileUpload';
import StorageManager from '../components/StorageManager';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`storage-tabpanel-${index}`}
      aria-labelledby={`storage-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const StorageTestPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [uploadSuccess, setUploadSuccess] = useState<any>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleUploadSuccess = (fileData: any) => {
    setUploadSuccess(fileData);
    // Switch to storage manager tab to see the uploaded file
    setTabValue(3);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Storage System Test
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        Test the Supabase storage integration with file uploads and management.
      </Typography>

      {uploadSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          File uploaded successfully! Check the Storage Manager tab to see your files.
        </Alert>
      )}

      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="storage tabs">
            <Tab 
              icon={<Image />} 
              label="Upload User Image" 
              id="storage-tab-0"
              aria-controls="storage-tabpanel-0"
            />
            <Tab 
              icon={<Image />} 
              label="Upload Profile Picture" 
              id="storage-tab-1"
              aria-controls="storage-tabpanel-1"
            />
            <Tab 
              icon={<Description />} 
              label="Upload Activity Document" 
              id="storage-tab-2"
              aria-controls="storage-tabpanel-2"
            />
            <Tab 
              icon={<Storage />} 
              label="Storage Manager" 
              id="storage-tab-3"
              aria-controls="storage-tabpanel-3"
            />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Typography variant="h6" gutterBottom>
            Upload User Image
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Upload images for your activities. Maximum file size: 10MB
          </Typography>
          <FileUpload 
            type="user-image" 
            onUploadSuccess={handleUploadSuccess}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Typography variant="h6" gutterBottom>
            Upload Profile Picture
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Upload your profile picture. Maximum file size: 5MB
          </Typography>
          <FileUpload 
            type="profile-picture" 
            onUploadSuccess={handleUploadSuccess}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Typography variant="h6" gutterBottom>
            Upload Activity Document
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Upload documents related to your activities. Maximum file size: 15MB
          </Typography>
          <FileUpload 
            type="activity-document" 
            activityId={1} // Example activity ID
            onUploadSuccess={handleUploadSuccess}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <StorageManager />
        </TabPanel>
      </Paper>

      {/* Storage Information */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Storage Information
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          <Box>
            <Typography variant="subtitle1" gutterBottom>
              User Images
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Maximum size: 10MB
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Supported formats: JPEG, PNG, GIF, WebP
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Use for: Activity images, general uploads
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Profile Pictures
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Maximum size: 5MB
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Supported formats: JPEG, PNG, GIF
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Use for: User profile photos
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Activity Documents
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Maximum size: 15MB
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Supported formats: PDF, DOC, DOCX, Images
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • Use for: Certificates, reports, documents
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default StorageTestPage;