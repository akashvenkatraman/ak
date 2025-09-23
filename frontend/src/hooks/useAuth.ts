import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { User, LoginCredentials, UserCreate } from '../types';
import { authApi } from '../services/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<{ success: boolean; user: User }>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const refreshUser = useCallback(async () => {
    try {
      const response = await authApi.getCurrentUser();
      const userData = response.data;
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (error) {
      console.error('Error refreshing user:', error);
      logout();
    }
  }, []);

  const updateUser = useCallback((userData: Partial<User>) => {
    setUser(prev => {
      if (prev) {
        const updatedUser = { ...prev, ...userData };
        // Update localStorage with the new user data
        localStorage.setItem('user', JSON.stringify(updatedUser));
        return updatedUser;
      }
      return null;
    });
  }, []);

  // Check if user is logged in on app start
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const savedUser = localStorage.getItem('user');

        if (token && savedUser) {
          console.log('🔐 Initializing auth with saved user...');
          setUser(JSON.parse(savedUser));
          
          // Verify token with server (but don't block if it fails)
          try {
            await refreshUser();
            console.log('🔐 Token verification successful');
          } catch (error) {
            console.warn('🔐 Token verification failed, but keeping user logged in:', error);
            // Don't logout on verification failure, just keep the saved user
          }
        } else {
          console.log('🔐 No saved authentication found');
        }
      } catch (error) {
        console.error('🔐 Error initializing auth:', error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, [refreshUser]);

  const login = async (credentials: LoginCredentials) => {
    try {
      console.log('🔐 useAuth: Starting login...');
      console.log('🔐 useAuth: Credentials:', credentials);
      setIsLoading(true);
      
      console.log('🔐 useAuth: Calling authApi.login...');
      const response = await authApi.login(credentials);
      console.log('🔐 useAuth: Response received:', response);
      
      const { access_token, user: userData } = response.data;
      console.log('🔐 useAuth: User data:', userData);

      // Store authentication data
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Update state
      setUser(userData);
      console.log('🔐 useAuth: Login completed successfully');
      
      // Return success to indicate login completed
      return { success: true, user: userData };
    } catch (error) {
      console.error('🔐 useAuth: Login error:', error);
      // Clear any partial state
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setUser(null);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: UserCreate) => {
    try {
      setIsLoading(true);
      await authApi.register(userData);
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
    updateUser,
  };

  return React.createElement(AuthContext.Provider, { value }, children);
};

export { AuthContext };
