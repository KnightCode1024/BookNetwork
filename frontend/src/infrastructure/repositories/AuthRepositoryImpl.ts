import { AuthRepository } from '@domain/repositories/AuthRepository';
import { TokenPair, LoginCredentials, RegisterData } from '@domain/entities/Auth';
import { User } from '@domain/entities/User';
import { ApiClient } from '../http/ApiClient';

export class AuthRepositoryImpl implements AuthRepository {
  constructor(private apiClient: ApiClient) {}

  async login(credentials: LoginCredentials): Promise<TokenPair> {
    const response = await this.apiClient.getClient().post<TokenPair>(
      '/auth/login/',
      credentials
    );
    return response.data;
  }

  async register(data: RegisterData): Promise<TokenPair> {
    // Убираем undefined поля, чтобы не отправлять их на бэкенд
    const payload: Record<string, unknown> = {
      username: data.username,
      password: data.password,
    };
    
    // Добавляем email только если он есть
    if (data.email && data.email.trim()) {
      payload.email = data.email.trim();
    }
    
    const response = await this.apiClient.getClient().post<TokenPair>(
      '/auth/register/',
      payload
    );
    return response.data;
  }

  async refreshToken(refreshToken: string): Promise<TokenPair> {
    const response = await this.apiClient.getClient().post<TokenPair>(
      '/auth/refresh/',
      { refresh_token: refreshToken }
    );
    return response.data;
  }

  async logout(): Promise<void> {
    // На бэкенде может не быть logout endpoint, просто очищаем токены на клиенте
    return Promise.resolve();
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.apiClient.getClient().get<User>('/auth/me/');
    return response.data;
  }
}

