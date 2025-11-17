import { Author } from '@domain/entities/Author';
import { AuthorRepository, ListAuthorsParams } from '@domain/repositories/AuthorRepository';

export class ListAuthorsUseCase {
  constructor(private authorRepository: AuthorRepository) {}

  async execute(params: ListAuthorsParams): Promise<Author[]> {
    return this.authorRepository.listAuthors(params);
  }
}


