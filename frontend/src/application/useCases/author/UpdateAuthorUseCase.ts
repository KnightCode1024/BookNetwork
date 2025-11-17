import { Author, AuthorPayload } from '@domain/entities/Author';
import { AuthorRepository } from '@domain/repositories/AuthorRepository';

export class UpdateAuthorUseCase {
  constructor(private authorRepository: AuthorRepository) {}

  async execute(authorId: number, payload: Partial<AuthorPayload>): Promise<Author> {
    return this.authorRepository.updateAuthor(authorId, payload);
  }
}


