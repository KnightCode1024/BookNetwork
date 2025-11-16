import { AuthRepository } from '@domain/repositories/AuthRepository';
import { TokenStorage } from '@domain/repositories/TokenStorage';

export class LogoutUseCase {
  constructor(
    private authRepository: AuthRepository,
    private tokenStorage: TokenStorage
  ) {}

  async execute(): Promise<void> {
    await this.authRepository.logout();
    this.tokenStorage.clearTokens();
  }
}

