export interface AuthorFeed {
  id: number;
  name: string;
  surname: string;
  patronymic: string;
}

export interface GenreFeed {
  id: number;
  name: string;
}

export interface BookFeed {
  id: number;
  title: string;
  description: string;
  publication_year: number;
  author: AuthorFeed;
  genre: GenreFeed;
}

export interface UserFeed {
  id: number;
  username: string;
}

export type ReviewStars = 1 | 2 | 3 | 4 | 5;

export interface ReviewFeed {
  id: number;
  title: string;
  content: string;
  stars: ReviewStars;
  likes_count: number;
  created_at: string;
  updated_at: string;
  user: UserFeed;
  book: BookFeed;
}

export interface FeedResponse {
  reviews: ReviewFeed[];
  total: number;
  offset: number;
  limit: number;
  has_more: boolean;
}

export interface FeedFilters {
  book_id?: number;
  user_id?: number;
  genre_id?: number;
  author_id?: number;
  min_stars?: number;
  max_stars?: number;
  order_by?: 'newest' | 'oldest' | 'highest_rated';
}

