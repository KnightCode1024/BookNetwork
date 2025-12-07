import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { TokenStorage } from '@domain/repositories/TokenStorage';
import { TokenPair } from '@domain/entities/Auth';

// Определяем baseURL для API
// В dev режиме всегда используем пустую строку для прокси Vite
// Прокси Vite будет перенаправлять запросы на backend (внутри Docker сети)
// В production используем полный URL из env
const API_BASE_URL = import.meta.env.DEV || import.meta.env.MODE === 'development'
  ? '' // В dev режиме используем прокси Vite
  : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');

export class ApiClient {
  private client: AxiosInstance;
  private tokenStorage: TokenStorage;
  private isRefreshing = false;
  private failedQueue: Array<{
    resolve: (value?: unknown) => void;
    reject: (reason?: unknown) => void;
  }> = [];

  constructor(tokenStorage: TokenStorage) {
    this.tokenStorage = tokenStorage;
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - добавляет access token к каждому запросу
    this.client.interceptors.request.use(
      (config) => {
        const token = this.tokenStorage.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - обрабатывает 401 и обновляет токены
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & {
          _retry?: boolean;
        };

        // Если ошибка 401 и это не запрос на refresh/login/register
        if (
          error.response?.status === 401 &&
          originalRequest &&
          !originalRequest._retry &&
          !originalRequest.url?.includes('/auth/refresh') &&
          !originalRequest.url?.includes('/auth/login') &&
          !originalRequest.url?.includes('/auth/register')
        ) {
          if (this.isRefreshing) {
            // Если уже идет обновление токена, добавляем запрос в очередь
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject });
            })
              .then(() => {
                const token = this.tokenStorage.getAccessToken();
                if (originalRequest.headers) {
                  originalRequest.headers.Authorization = `Bearer ${token}`;
                }
                return this.client(originalRequest);
              })
              .catch((err) => {
                return Promise.reject(err);
              });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          const refreshToken = this.tokenStorage.getRefreshToken();
          if (!refreshToken) {
            this.tokenStorage.clearTokens();
            return Promise.reject(error);
          }

          try {
            // Используем тот же клиент для консистентности
            const response = await this.client.post<TokenPair>(
              '/auth/refresh/',
              { refresh_token: refreshToken }
            );

            const { access_token, refresh_token } = response.data;
            this.tokenStorage.setTokens(access_token, refresh_token);

            // Обрабатываем очередь запросов
            this.processQueue(null);

            // Повторяем оригинальный запрос
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
            }
            return this.client(originalRequest);
          } catch (refreshError) {
            this.processQueue(refreshError);
            this.tokenStorage.clearTokens();
            return Promise.reject(refreshError);
          } finally {
            this.isRefreshing = false;
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private processQueue(error: unknown): void {
    this.failedQueue.forEach((promise) => {
      if (error) {
        promise.reject(error);
      } else {
        promise.resolve();
      }
    });
    this.failedQueue = [];
  }

  getClient(): AxiosInstance {
    return this.client;
  }
}

