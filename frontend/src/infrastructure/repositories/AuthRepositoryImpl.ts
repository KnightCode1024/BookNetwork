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
    // Формируем payload для регистрации
    const payload: Record<string, unknown> = {
      username: data.username,
      password: data.password,
    };
    
    // Добавляем email только если он есть и не пустой
    // Если email не передан или пустой, не добавляем его в payload
    // Бэкенд ожидает либо валидный EmailStr, либо None (но не undefined)
    if (data.email && data.email.trim()) {
      payload.email = data.email.trim();
    }
    // Если email не передан, не добавляем поле вообще
    
    console.log('Register payload:', payload);
    
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

