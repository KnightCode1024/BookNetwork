import { AuthorRepository } from '@domain/repositories/AuthorRepository';

export class DeleteAuthorUseCase {
  constructor(private authorRepository: AuthorRepository) {}

  async execute(authorId: number): Promise<void> {
    await this.authorRepository.deleteAuthor(authorId);
  }
}





