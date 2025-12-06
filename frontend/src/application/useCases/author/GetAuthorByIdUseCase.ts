import { Author } from '@domain/entities/Author';
import { AuthorRepository } from '@domain/repositories/AuthorRepository';

export class GetAuthorByIdUseCase {
  constructor(private authorRepository: AuthorRepository) {}

  async execute(authorId: number): Promise<Author> {
    return this.authorRepository.getAuthorById(authorId);
  }
}






