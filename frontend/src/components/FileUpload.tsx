import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Alert,
  Paper,
  IconButton,
  Chip
} from '@mui/material';
import {
  CloudUpload,
  Image,
  Description,
  Delete,
  Visibility
} from '@mui/icons-material';
import api from '../services/api';

interface FileUploadProps {
  type: 'user-image' | 'profile-picture' | 'activity-document';
  activityId?: number;
  onUploadSuccess?: (fileData: any) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  type, 
  activityId, 
  onUploadSuccess 
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const getUploadConfig = () => {
    switch (type) {
      case 'user-image':
        return {
          endpoint: '/api/storage/upload/user-image',
          accept: 'image/*',
          maxSize: 10 * 1024 * 1024, // 10MB
          label: 'User Image'
        };
      case 'profile-picture':
        return {
          endpoint: '/api/storage/upload/profile-picture',
          accept: 'image/*',
          maxSize: 5 * 1024 * 1024, // 5MB
          label: 'Profile Picture'
        };
      case 'activity-document':
        return {
          endpoint: '/api/storage/upload/activity-document',
          accept: '.pdf,.doc,.docx,image/*',
          maxSize: 15 * 1024 * 1024, // 15MB
          label: 'Activity Document'
        };
      default:
        throw new Error('Invalid upload type');
    }
  };

  const config = getUploadConfig();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file size
    if (file.size > config.maxSize) {
      setError(`File size must be less than ${config.maxSize / (1024 * 1024)}MB`);
      return;
    }

    setSelectedFile(file);
    setError(null);
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      if (type === 'activity-document' && activityId) {
        formData.append('activity_id', activityId.toString());
      }

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await api.post(config.endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent: any) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(progress);
          }
        }
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.data) {
        setUploadResult(response.data);
        onUploadSuccess?.(response.data);
        setSelectedFile(null);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError(null);
    setUploadProgress(0);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Card sx={{ maxWidth: 600, margin: 'auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Upload {config.label}
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {uploadResult && (
          <Alert severity="success" sx={{ mb: 2 }}>
            File uploaded successfully!
          </Alert>
        )}

        {!selectedFile && !uploadResult && (
          <Box
            sx={{
              border: '2px dashed #ccc',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'action.hover'
              }
            }}
            onClick={() => document.getElementById('file-input')?.click()}
          >
            <CloudUpload sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
            <Typography variant="body1" gutterBottom>
              Click to select file or drag and drop
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Max size: {config.maxSize / (1024 * 1024)}MB
            </Typography>
            <input
              id="file-input"
              type="file"
              accept={config.accept}
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </Box>
        )}

        {selectedFile && (
          <Paper sx={{ p: 2, mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box>
                {type.includes('image') ? (
                  <Image color="primary" />
                ) : (
                  <Description color="primary" />
                )}
              </Box>
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body1">
                  {selectedFile.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formatFileSize(selectedFile.size)}
                </Typography>
              </Box>
              <IconButton onClick={handleDelete} color="error">
                <Delete />
              </IconButton>
            </Box>
          </Paper>
        )}

        {uploading && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" gutterBottom>
              Uploading... {uploadProgress}%
            </Typography>
            <LinearProgress variant="determinate" value={uploadProgress} />
          </Box>
        )}

        {uploadResult && (
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="body1" gutterBottom>
              Upload Successful!
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Chip 
                label={`Size: ${formatFileSize(uploadResult.data?.file_size || 0)}`}
                size="small"
              />
              <Chip 
                label={`Type: ${uploadResult.data?.file_type || 'Unknown'}`}
                size="small"
              />
            </Box>
            {uploadResult.data?.public_url && (
              <Button
                startIcon={<Visibility />}
                onClick={() => window.open(uploadResult.data.public_url, '_blank')}
                sx={{ mt: 1 }}
                size="small"
              >
                View File
              </Button>
            )}
          </Paper>
        )}

        {selectedFile && !uploading && (
          <Button
            variant="contained"
            onClick={handleUpload}
            startIcon={<CloudUpload />}
            fullWidth
          >
            Upload {config.label}
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUpload;