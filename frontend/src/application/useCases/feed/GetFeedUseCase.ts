import { FeedResponse, FeedFilters } from '@domain/entities/Feed';
import { FeedRepository, GetFeedParams } from '@domain/repositories/FeedRepository';

export class GetFeedUseCase {
  constructor(private feedRepository: FeedRepository) {}

  async execute(params: GetFeedParams): Promise<FeedResponse> {
    return this.feedRepository.getFeed(params);
  }
}

