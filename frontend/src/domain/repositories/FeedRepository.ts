import { FeedResponse, FeedFilters } from '@domain/entities/Feed';

export interface GetFeedParams {
  offset?: number;
  limit?: number;
  filters?: FeedFilters;
}

export interface FeedRepository {
  getFeed(params: GetFeedParams): Promise<FeedResponse>;
}

