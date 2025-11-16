import { TokenStorage } from '@domain/repositories/TokenStorage';

const ACCESS_TOKEN_KEY = 'booknetwork_access_token';
const REFRESH_TOKEN_KEY = 'booknetwork_refresh_token';

/**
 * Хранилище токенов в localStorage
 * 
 * ВАЖНО: localStorage уязвим к XSS атакам.
 * Для production рекомендуется использовать httpOnly cookies на бэкенде.
 * 
 * Преимущества:
 * - Токены сохраняются между перезагрузками страницы
 * - Удобно для пользователя
 * 
 * Недостатки:
 * - Токены доступны через JavaScript (риск XSS)
 * - Не рекомендуется для хранения чувствительных данных
 */
export class LocalStorageTokenStorage implements TokenStorage {
  getAccessToken(): string | null {
    try {
      return localStorage.getItem(ACCESS_TOKEN_KEY);
    } catch (error) {
      console.error('Failed to get access token from localStorage:', error);
      return null;
    }
  }

  getRefreshToken(): string | null {
    try {
      return localStorage.getItem(REFRESH_TOKEN_KEY);
    } catch (error) {
      console.error('Failed to get refresh token from localStorage:', error);
      return null;
    }
  }

  setTokens(accessToken: string, refreshToken: string): void {
    try {
      localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
      localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    } catch (error) {
      console.error('Failed to save tokens to localStorage:', error);
      // Если localStorage переполнен или недоступен, пробуем очистить старые данные
      try {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
        localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
      } catch (retryError) {
        console.error('Failed to save tokens after cleanup:', retryError);
      }
    }
  }

  clearTokens(): void {
    try {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    } catch (error) {
      console.error('Failed to clear tokens from localStorage:', error);
    }
  }

  hasTokens(): boolean {
    return this.getAccessToken() !== null && this.getRefreshToken() !== null;
  }
}

