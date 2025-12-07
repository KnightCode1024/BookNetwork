import { AxiosInstance } from 'axios';
import { ApiClient } from '../http/ApiClient';
import { FeedResponse } from '@domain/entities/Feed';
import { FeedRepository, GetFeedParams } from '@domain/repositories/FeedRepository';

export class FeedRepositoryImpl implements FeedRepository {
  private client: AxiosInstance;

  constructor(apiClient: ApiClient) {
    this.client = apiClient.getClient();
  }

  async getFeed(params: GetFeedParams): Promise<FeedResponse> {
    const { offset = 0, limit = 20 } = params;
    
    // Отправляем только базовые параметры offset и limit
    const queryParams: Record<string, unknown> = {
      offset,
      limit,
    };

    console.log('FeedRepository: Making request to /feed/ with params:', queryParams);
    console.log('FeedRepository: Client baseURL:', this.client.defaults.baseURL);

    try {
      const response = await this.client.get<FeedResponse>('/feed/', {
        params: queryParams,
      });
      console.log('FeedRepository: Response received:', response);
      console.log('FeedRepository: Response data:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('FeedRepository: Error making request:', error);
      console.error('FeedRepository: Error response:', error.response);
      console.error('FeedRepository: Error message:', error.message);
      throw error;
    }
  }
}

