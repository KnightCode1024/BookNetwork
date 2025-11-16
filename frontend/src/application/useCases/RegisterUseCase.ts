import { AuthRepository } from '@domain/repositories/AuthRepository';
import { TokenStorage } from '@domain/repositories/TokenStorage';
import { RegisterData, TokenPair } from '@domain/entities/Auth';

export class RegisterUseCase {
  constructor(
    private authRepository: AuthRepository,
    private tokenStorage: TokenStorage
  ) {}

  async execute(data: RegisterData): Promise<TokenPair> {
    const tokens = await this.authRepository.register(data);
    this.tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
    return tokens;
  }
}

