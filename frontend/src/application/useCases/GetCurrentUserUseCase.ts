import { AuthRepository } from '@domain/repositories/AuthRepository';
import { User } from '@domain/entities/User';

export class GetCurrentUserUseCase {
  constructor(private authRepository: AuthRepository) {}

  async execute(): Promise<User> {
    return await this.authRepository.getCurrentUser();
  }
}

