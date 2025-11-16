import { TokenStorage } from '@domain/repositories/TokenStorage';

/**
 * Безопасное хранилище токенов в памяти
 * Токены не сохраняются в localStorage/sessionStorage для защиты от XSS атак
 * При перезагрузке страницы пользователю нужно будет войти заново
 */
export class MemoryTokenStorage implements TokenStorage {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  getAccessToken(): string | null {
    return this.accessToken;
  }

  getRefreshToken(): string | null {
    return this.refreshToken;
  }

  setTokens(accessToken: string, refreshToken: string): void {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
  }

  clearTokens(): void {
    this.accessToken = null;
    this.refreshToken = null;
  }

  hasTokens(): boolean {
    return this.accessToken !== null && this.refreshToken !== null;
  }
}

