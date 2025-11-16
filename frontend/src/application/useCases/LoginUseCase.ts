import { AuthRepository } from '@domain/repositories/AuthRepository';
import { TokenStorage } from '@domain/repositories/TokenStorage';
import { LoginCredentials, TokenPair } from '@domain/entities/Auth';

export class LoginUseCase {
  constructor(
    private authRepository: AuthRepository,
    private tokenStorage: TokenStorage
  ) {}

  async execute(credentials: LoginCredentials): Promise<TokenPair> {
    const tokens = await this.authRepository.login(credentials);
    this.tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
    return tokens;
  }
}

