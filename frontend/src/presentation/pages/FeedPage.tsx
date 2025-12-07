import { useEffect, useMemo, useState } from 'react';
import {
  Container,
  Title,
  Stack,
  Paper,
  Text,
  Group,
  Badge,
  Loader,
  Center,
  Button,
  Avatar,
  Divider,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useAuth } from '../providers/AuthProvider';
import { FeedRepositoryImpl } from '@infrastructure/repositories/FeedRepositoryImpl';
import { GetFeedUseCase } from '@application/useCases/feed/GetFeedUseCase';
import { ReviewFeed } from '@domain/entities/Feed';

const FEED_LIMIT = 20;

const formatDate = (dateString: string) => {
  try {
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(dateString));
  } catch {
    return dateString;
  }
};

const StarRating = ({ stars }: { stars: number }) => {
  return (
    <Group gap={2}>
      {[1, 2, 3, 4, 5].map((star) => (
        <Text
          key={star}
          size="sm"
          fw={700}
          c={star <= stars ? 'yellow.6' : 'gray.5'}
        >
          ★
        </Text>
      ))}
    </Group>
  );
};

interface ReviewCardProps {
  review: ReviewFeed;
}

const ReviewCard = ({ review }: ReviewCardProps) => {
  // Проверяем наличие всех необходимых данных
  if (!review || !review.user || !review.book || !review.book.author || !review.book.genre) {
    return (
      <Paper
        p="md"
        withBorder
        shadow="sm"
        radius="xs"
        style={{
          borderColor: '#8b4513',
          borderWidth: '2px',
          borderStyle: 'double',
          backgroundColor: '#fef9e7',
        }}
      >
        <Text c="red" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
          Ошибка: неполные данные отзыва
        </Text>
      </Paper>
    );
  }

  const username = review.user?.username || 'Неизвестный';
  const userInitial = username[0]?.toUpperCase() || '?';
  const title = review.title || 'Без названия';
  const content = review.content || '';
  const likesCount = typeof review.likes_count === 'number' ? review.likes_count : 0;
  const stars = typeof review.stars === 'number' ? review.stars : 0;
  const bookTitle = review.book?.title || 'Неизвестная книга';
  const authorName = review.book?.author?.name || '';
  const authorSurname = review.book?.author?.surname || '';
  const genreName = review.book?.genre?.name || 'Неизвестный жанр';
  const createdAt = review.created_at || new Date().toISOString();

  return (
    <Paper
      p="md"
      withBorder
      shadow="sm"
      radius="xs"
      style={{
        borderColor: '#8b4513',
        borderWidth: '2px',
        borderStyle: 'double',
        backgroundColor: '#fef9e7',
      }}
    >
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <Stack gap={4} style={{ flex: 1 }}>
            <Group gap="xs" align="center">
              <Avatar size="sm" radius="xl" color="brown" style={{ border: '2px solid #8b4513' }}>
                {userInitial}
              </Avatar>
              <Text fw={700} size="sm" c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
                {username}
              </Text>
              <Text size="xs" c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
                {formatDate(createdAt)}
              </Text>
            </Group>
            <Text
              fw={700}
              size="lg"
              c="#654321"
              style={{
                fontFamily: '"Times New Roman", "Georgia", "Times", serif',
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
            >
              {title}
            </Text>
          </Stack>
          <Group gap="xs">
            <StarRating stars={stars} />
            <Badge color="red" variant="light" style={{ border: '1px solid #8b4513' }}>
              ❤ {likesCount}
            </Badge>
          </Group>
        </Group>

        <Divider color="#8b4513" />

        <Stack gap="xs">
          <Group gap="xs" align="center">
            <Text size="sm" fw={700} c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              Книга:
            </Text>
            <Text size="sm" fw={600} c="#654321" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              {bookTitle}
            </Text>
          </Group>
          <Group gap="xs" align="center">
            <Text size="sm" fw={700} c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              Автор:
            </Text>
            <Text size="sm" c="#654321" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              {authorName} {authorSurname}
            </Text>
          </Group>
          <Group gap="xs" align="center">
            <Text size="sm" fw={700} c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              Жанр:
            </Text>
            <Badge size="sm" variant="light" style={{ border: '1px solid #8b4513', color: '#8b4513' }}>
              {genreName}
            </Badge>
          </Group>
        </Stack>

        <Divider color="#8b4513" />

        <Text
          size="sm"
          c="#654321"
          style={{
            whiteSpace: 'pre-wrap',
            fontFamily: '"Times New Roman", "Georgia", "Times", serif',
            lineHeight: '1.8',
          }}
        >
          {content}
        </Text>
      </Stack>
    </Paper>
  );
};

export const FeedPage = () => {
  const { apiClient } = useAuth();

  const feedRepository = useMemo(() => new FeedRepositoryImpl(apiClient), [apiClient]);
  const getFeedUseCase = useMemo(() => new GetFeedUseCase(feedRepository), [feedRepository]);

  const [reviews, setReviews] = useState<ReviewFeed[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [total, setTotal] = useState(0);

  const fetchFeed = async (append = false) => {
    const currentOffset = append ? offset : 0;
    setLoading(true);
    try {
      const response = await getFeedUseCase.execute({
        offset: currentOffset,
        limit: FEED_LIMIT,
      });

      console.log('Feed response:', response);

      // Проверяем, что response существует и содержит reviews
      if (!response) {
        throw new Error('Пустой ответ от сервера');
      }

      // Проверяем, что reviews существует и является массивом
      const reviewsList = Array.isArray(response.reviews) ? response.reviews : [];
      
      console.log('Reviews list:', reviewsList);

      if (append) {
        setReviews((prev) => {
          const prevList = Array.isArray(prev) ? prev : [];
          return [...prevList, ...reviewsList];
        });
      } else {
        setReviews(reviewsList);
      }

      const currentOffsetValue = typeof response.offset === 'number' ? response.offset : 0;
      setOffset(currentOffsetValue + reviewsList.length);
      setHasMore(typeof response.has_more === 'boolean' ? response.has_more : false);
      setTotal(typeof response.total === 'number' ? response.total : 0);
    } catch (error) {
      console.error('Ошибка загрузки ленты:', error);
      console.error('Детали ошибки:', error instanceof Error ? error.stack : error);
      notifications.show({
        color: 'red',
        title: 'Не удалось загрузить ленту',
        message: error instanceof Error ? error.message : 'Попробуйте обновить страницу или повторить запрос позже.',
      });
      // Устанавливаем пустой массив в случае ошибки
      if (!append) {
        setReviews([]);
        setTotal(0);
        setHasMore(false);
        setOffset(0);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleLoadMore = () => {
    fetchFeed(true);
  };

  return (
    <Container size="xl" py="xl">
      <Stack gap="xl">
        <Group justify="space-between" align="center">
          <Title
            order={1}
            c="#8b4513"
            style={{
              fontFamily: '"Times New Roman", "Georgia", "Times", serif',
              textTransform: 'uppercase',
              letterSpacing: '3px',
              textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
            }}
          >
            Лента отзывов
          </Title>
          <Badge size="lg" variant="light" style={{ border: '2px solid #8b4513', color: '#8b4513' }}>
            Всего: {total}
          </Badge>
        </Group>

        {loading && (!reviews || reviews.length === 0) ? (
          <Center py="xl">
            <Loader size="lg" />
          </Center>
        ) : !reviews || reviews.length === 0 ? (
          <Center py="xl">
            <Text c="dimmed" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
              Отзывы не найдены
            </Text>
          </Center>
        ) : (
          <>
            <Stack gap="md">
              {reviews.map((review) => (
                <ReviewCard key={review.id} review={review} />
              ))}
            </Stack>

            {hasMore && (
              <Center>
                <Button onClick={handleLoadMore} loading={loading} variant="default">
                  Загрузить ещё
                </Button>
              </Center>
            )}
          </>
        )}
      </Stack>
    </Container>
  );
};

