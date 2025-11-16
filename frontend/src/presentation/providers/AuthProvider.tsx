import React, { useEffect, ReactNode, createContext, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { LocalStorageTokenStorage } from '@infrastructure/storage/LocalStorageTokenStorage';
import { ApiClient } from '@infrastructure/http/ApiClient';
import { AuthRepositoryImpl } from '@infrastructure/repositories/AuthRepositoryImpl';
import { LoginUseCase } from '@application/useCases/LoginUseCase';
import { RegisterUseCase } from '@application/useCases/RegisterUseCase';
import { LogoutUseCase } from '@application/useCases/LogoutUseCase';
import { GetCurrentUserUseCase } from '@application/useCases/GetCurrentUserUseCase';
import { useAuthStore } from '@application/store/authStore';

// Создаем singleton экземпляры
// Используем LocalStorageTokenStorage для сохранения токенов между перезагрузками
const tokenStorage = new LocalStorageTokenStorage();
const apiClient = new ApiClient(tokenStorage);
const authRepository = new AuthRepositoryImpl(apiClient);
const loginUseCase = new LoginUseCase(authRepository, tokenStorage);
const registerUseCase = new RegisterUseCase(authRepository, tokenStorage);
const logoutUseCase = new LogoutUseCase(authRepository, tokenStorage);
const getCurrentUserUseCase = new GetCurrentUserUseCase(authRepository);

interface AuthContextValue {
  loginUseCase: LoginUseCase;
  registerUseCase: RegisterUseCase;
  logoutUseCase: LogoutUseCase;
  getCurrentUserUseCase: GetCurrentUserUseCase;
  tokenStorage: LocalStorageTokenStorage;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const navigate = useNavigate();
  const { isAuthenticated, logout: logoutStore, setUser, setLoading } = useAuthStore();

  useEffect(() => {
    const loadUser = async () => {
      try {
        const hasTokens = tokenStorage.hasTokens();
        if (hasTokens) {
          try {
            const user = await getCurrentUserUseCase.execute();
            setUser(user);
            useAuthStore.getState().setAuthenticated(true);
          } catch (error) {
            // Если не удалось загрузить пользователя, очищаем токены
            console.error('Failed to load user:', error);
            tokenStorage.clearTokens();
            useAuthStore.getState().setAuthenticated(false);
          }
        } else {
          useAuthStore.getState().setAuthenticated(false);
        }
      } catch (error) {
        console.error('Error in loadUser:', error);
        useAuthStore.getState().setAuthenticated(false);
      } finally {
        // Всегда устанавливаем isLoading в false
        setLoading(false);
      }
    };

    loadUser();

    // Таймаут на случай, если что-то пошло не так
    const timeout = setTimeout(() => {
      if (useAuthStore.getState().isLoading) {
        console.warn('Auth loading timeout, setting isLoading to false');
        setLoading(false);
      }
    }, 5000);

    return () => clearTimeout(timeout);
  }, [setUser, setLoading]);

  const handleLogout = async () => {
    await logoutUseCase.execute();
    logoutStore();
    navigate('/login');
  };

  // Создаем обертку для logoutUseCase с навигацией
  const logoutUseCaseWithNavigation: LogoutUseCase = {
    execute: handleLogout,
  } as LogoutUseCase;

  const value: AuthContextValue = {
    loginUseCase,
    registerUseCase,
    logoutUseCase: logoutUseCaseWithNavigation,
    getCurrentUserUseCase,
    tokenStorage,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

