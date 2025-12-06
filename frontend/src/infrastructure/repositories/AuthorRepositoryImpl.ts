import { AxiosInstance } from 'axios';
import { ApiClient } from '../http/ApiClient';
import { Author } from '@domain/entities/Author';
import { AuthorPayload } from '@domain/entities/Author';
import { AuthorRepository, ListAuthorsParams } from '@domain/repositories/AuthorRepository';

export class AuthorRepositoryImpl implements AuthorRepository {
  private client: AxiosInstance;

  constructor(apiClient: ApiClient) {
    this.client = apiClient.getClient();
  }

  async listAuthors(params: ListAuthorsParams): Promise<Author[]> {
    const { query, skip = 0, limit = 20 } = params;

    if (query?.trim()) {
      const response = await this.client.get<Author[]>('/authors/search/', {
        params: { query: query.trim(), limit },
      });
      return response.data;
    }

    const response = await this.client.get<Author[]>('/authors/', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getAuthorById(authorId: number): Promise<Author> {
    const response = await this.client.get<Author>(`/authors/${authorId}/`);
    return response.data;
  }

  async createAuthor(payload: AuthorPayload): Promise<Author> {
    const response = await this.client.post<Author>('/authors/', payload);
    return response.data;
  }

  async updateAuthor(authorId: number, payload: Partial<AuthorPayload>): Promise<Author> {
    const response = await this.client.patch<Author>(`/authors/${authorId}/`, payload);
    return response.data;
  }

  async deleteAuthor(authorId: number): Promise<void> {
    await this.client.delete(`/authors/${authorId}/`);
  }
}






