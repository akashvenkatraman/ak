import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  CloudUpload,
  Download,
  Delete,
  AttachFile,
  CheckCircle,
} from '@mui/icons-material';
import { fileApi } from '../services/api';
import { FileStorage } from '../types';

interface FileManagerProps {
  activityId: number;
  canUpload?: boolean;
  canDelete?: boolean;
  onFileUploaded?: () => void;
  onFileDeleted?: () => void;
}

const FileManager: React.FC<FileManagerProps> = ({
  activityId,
  canUpload = false,
  canDelete = false,
  onFileUploaded,
  onFileDeleted,
}) => {
  const [files, setFiles] = useState<FileStorage[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = useCallback(async () => {
    try {
      setLoading(true);
      console.log('Loading files for activity:', activityId);
      const response = await fileApi.getActivityFiles(activityId);
      console.log('Files response:', response.data);
      setFiles(response.data);
    } catch (err: any) {
      setError('Failed to load files');
      console.error('Error loading files:', err);
    } finally {
      setLoading(false);
    }
  }, [activityId]);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size too large. Maximum 10MB allowed.');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      await fileApi.uploadFile(activityId, file);
      await loadFiles();
      onFileUploaded?.();
      
      // Show success message
      setError('');
      alert(`File "${file.name}" uploaded successfully!`);
    } catch (err: any) {
      console.error('Error uploading file:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to upload file';
      setError(`Upload failed: ${errorMessage}`);
      alert(`Upload failed: ${errorMessage}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (file: FileStorage) => {
    try {
      console.log('Downloading file:', file.id, file.original_name);
      const response = await fileApi.downloadFile(file.id);
      console.log('Download response:', response);
      
      const blob = new Blob([response.data], { type: file.file_type });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.original_name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      // Show success message
      setError('');
      alert(`File "${file.original_name}" downloaded successfully!`);
      
      // Reload files to update download count
      await loadFiles();
    } catch (err: any) {
      console.error('Error downloading file:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to download file';
      setError(`Download failed: ${errorMessage}`);
      alert(`Download failed: ${errorMessage}`);
    }
  };

  // View functionality removed to reduce complexity and work pressure
  // Teachers can download files directly for viewing

  const handleDelete = async (file: FileStorage) => {
    if (!window.confirm(`Are you sure you want to delete "${file.original_name}"?`)) {
      return;
    }

    try {
      await fileApi.deleteFile(file.id);
      await loadFiles();
      onFileDeleted?.();
    } catch (err: any) {
      setError('Failed to delete file');
      console.error('Error deleting file:', err);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileType: string) => {
    if (fileType.startsWith('image/')) return '🖼️';
    if (fileType.startsWith('video/')) return '🎥';
    if (fileType.startsWith('audio/')) return '🎵';
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('word')) return '📝';
    if (fileType.includes('excel') || fileType.includes('spreadsheet')) return '📊';
    return '📎';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={2}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {canUpload && (
        <Box mb={2}>
          <input
            accept="*/*"
            style={{ display: 'none' }}
            id="file-upload"
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label htmlFor="file-upload">
            <Button
              variant="outlined"
              component="span"
              startIcon={uploading ? <CircularProgress size={20} /> : <CloudUpload />}
              disabled={uploading}
              fullWidth
            >
              {uploading ? 'Uploading...' : 'Upload Certificate/File'}
            </Button>
          </label>
        </Box>
      )}

      {files.length === 0 ? (
        <Card>
          <CardContent>
            <Box textAlign="center" py={4}>
              <AttachFile sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No files uploaded
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {canUpload ? 'Upload certificates or supporting documents' : 'No files available'}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      ) : (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {files.map((file) => (
            <Card key={file.id} sx={{ p: 2, borderRadius: 2, boxShadow: 1 }}>
              <Box display="flex" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={2}>
                <Box display="flex" alignItems="center" flex={1} minWidth={0}>
                  <Typography sx={{ mr: 2, fontSize: '1.5rem', flexShrink: 0 }}>
                    {getFileIcon(file.file_type)}
                  </Typography>
                  <Box flex={1} minWidth={0}>
                    <Typography 
                      variant="subtitle1" 
                      fontWeight={600}
                      sx={{ 
                        wordBreak: 'break-word',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 1,
                        WebkitBoxOrient: 'vertical'
                      }}
                    >
                      {file.original_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      {formatFileSize(file.file_size)} • {file.file_type}
                    </Typography>
                    <Box display="flex" gap={1} flexWrap="wrap">
                      <Chip
                        label={`${file.download_count} downloads`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.75rem' }}
                      />
                      <Chip
                        label={`${file.view_count} views`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.75rem' }}
                      />
                      {file.is_certificate && (
                        <Chip
                          label="Certificate"
                          size="small"
                          color="primary"
                          icon={<CheckCircle sx={{ fontSize: '0.875rem' }} />}
                          sx={{ fontSize: '0.75rem' }}
                        />
                      )}
                    </Box>
                  </Box>
                </Box>
                <Box display="flex" gap={1} alignItems="center" flexShrink={0}>
                  <Button
                    variant="contained"
                    startIcon={<Download />}
                    onClick={() => handleDownload(file)}
                    size="small"
                    sx={{ 
                      minWidth: 'auto',
                      px: 2,
                      py: 1,
                      borderRadius: 2,
                      textTransform: 'none',
                      fontWeight: 600,
                      fontSize: '0.875rem'
                    }}
                  >
                    Download
                  </Button>
                  {canDelete && (
                    <IconButton
                      onClick={() => handleDelete(file)}
                      title="Delete file"
                      color="error"
                      size="small"
                    >
                      <Delete />
                    </IconButton>
                  )}
                </Box>
              </Box>
            </Card>
          ))}
        </Box>
      )}

    </Box>
  );
};

export default FileManager;
