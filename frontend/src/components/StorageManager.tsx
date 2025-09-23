import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Paper
} from '@mui/material';
import {
  Image,
  Description,
  Delete,
  Visibility,
  CloudUpload,
  Storage,
  Refresh
} from '@mui/icons-material';
import api from '../services/api';

interface FileInfo {
  name: string;
  size: number;
  last_modified: string;
  public_url: string;
}

interface StorageStatus {
  storage_usage: {
    total_size_mb: number;
    user_images_count: number;
    profile_pictures_count: number;
    activity_documents_count: number;
    total_files: number;
  };
  buckets: {
    user_images: FileInfo[];
    profile_pictures: FileInfo[];
    activity_documents: FileInfo[];
  };
}

const StorageManager: React.FC = () => {
  const [storageStatus, setStorageStatus] = useState<StorageStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean;
    file: FileInfo | null;
    bucket: string;
  }>({ open: false, file: null, bucket: '' });

  const fetchStorageStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/api/storage/storage/status');
      setStorageStatus(response.data.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch storage status');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStorageStatus();
  }, []);

  const handleDeleteFile = async () => {
    if (!deleteDialog.file || !deleteDialog.bucket) return;

    try {
      await api.delete('/api/storage/files/delete', {
        data: {
          file_path: deleteDialog.file.name,
          bucket_name: deleteDialog.bucket
        }
      });
      
      setDeleteDialog({ open: false, file: null, bucket: '' });
      fetchStorageStatus(); // Refresh the list
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete file');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension || '')) {
      return <Image color="primary" />;
    }
    return <Description color="primary" />;
  };

  const renderFileList = (files: FileInfo[], bucketName: string) => {
    if (files.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Storage sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
          <Typography variant="body1" color="text.secondary">
            No files uploaded yet
          </Typography>
        </Box>
      );
    }

    return (
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
        {files.map((file, index) => (
          <Card key={index} sx={{ minWidth: 250, maxWidth: 300 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                {getFileIcon(file.name)}
                <Typography variant="body2" sx={{ ml: 1, flexGrow: 1 }}>
                  {file.name.split('/').pop()}
                </Typography>
              </Box>
              
              <Typography variant="caption" color="text.secondary" display="block">
                Size: {formatFileSize(file.size)}
              </Typography>
              
              <Typography variant="caption" color="text.secondary" display="block">
                Modified: {formatDate(file.last_modified)}
              </Typography>

              <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                <IconButton
                  size="small"
                  onClick={() => window.open(file.public_url, '_blank')}
                  color="primary"
                >
                  <Visibility />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => setDeleteDialog({ 
                    open: true, 
                    file, 
                    bucket: bucketName 
                  })}
                  color="error"
                >
                  <Delete />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!storageStatus) {
    return (
      <Alert severity="warning">
        No storage data available
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">
          Storage Manager
        </Typography>
        <Button
          startIcon={<Refresh />}
          onClick={fetchStorageStatus}
          variant="outlined"
        >
          Refresh
        </Button>
      </Box>

      {/* Storage Usage Summary */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Storage Usage
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {storageStatus.storage_usage.total_size_mb.toFixed(1)} MB
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Storage Used
            </Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {storageStatus.storage_usage.total_files}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Files
            </Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {storageStatus.storage_usage.user_images_count}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              User Images
            </Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {storageStatus.storage_usage.profile_pictures_count}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Profile Pictures
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* File Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={selectedTab} onChange={(e, newValue) => setSelectedTab(newValue)}>
          <Tab 
            label={`User Images (${storageStatus.storage_usage.user_images_count})`} 
            icon={<Image />}
          />
          <Tab 
            label={`Profile Pictures (${storageStatus.storage_usage.profile_pictures_count})`} 
            icon={<Image />}
          />
          <Tab 
            label={`Activity Documents (${storageStatus.storage_usage.activity_documents_count})`} 
            icon={<Description />}
          />
        </Tabs>
      </Box>

      {/* File Lists */}
      {selectedTab === 0 && renderFileList(storageStatus.buckets.user_images, 'user-images')}
      {selectedTab === 1 && renderFileList(storageStatus.buckets.profile_pictures, 'profile-pictures')}
      {selectedTab === 2 && renderFileList(storageStatus.buckets.activity_documents, 'activity-documents')}

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialog.open} onClose={() => setDeleteDialog({ open: false, file: null, bucket: '' })}>
        <DialogTitle>Delete File</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this file? This action cannot be undone.
          </Typography>
          {deleteDialog.file && (
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              File: {deleteDialog.file.name}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialog({ open: false, file: null, bucket: '' })}>
            Cancel
          </Button>
          <Button onClick={handleDeleteFile} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default StorageManager;