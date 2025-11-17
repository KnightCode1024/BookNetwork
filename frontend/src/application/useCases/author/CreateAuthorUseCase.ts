import { Author, AuthorPayload } from '@domain/entities/Author';
import { AuthorRepository } from '@domain/repositories/AuthorRepository';

export class CreateAuthorUseCase {
  constructor(private authorRepository: AuthorRepository) {}

  async execute(payload: AuthorPayload): Promise<Author> {
    return this.authorRepository.createAuthor(payload);
  }
}


