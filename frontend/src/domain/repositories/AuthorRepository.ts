import { Author, AuthorPayload } from '../entities/Author';

export interface ListAuthorsParams {
  skip?: number;
  limit?: number;
  query?: string;
}

export interface AuthorRepository {
  listAuthors(params: ListAuthorsParams): Promise<Author[]>;
  getAuthorById(authorId: number): Promise<Author>;
  createAuthor(payload: AuthorPayload): Promise<Author>;
  updateAuthor(authorId: number, payload: Partial<AuthorPayload>): Promise<Author>;
  deleteAuthor(authorId: number): Promise<void>;
}


