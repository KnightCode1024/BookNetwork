import { TokenPair, LoginCredentials, RegisterData } from '../entities/Auth';
import { User } from '../entities/User';

export interface AuthRepository {
  login(credentials: LoginCredentials): Promise<TokenPair>;
  register(data: RegisterData): Promise<TokenPair>;
  refreshToken(refreshToken: string): Promise<TokenPair>;
  logout(): Promise<void>;
  getCurrentUser(): Promise<User>;
}

