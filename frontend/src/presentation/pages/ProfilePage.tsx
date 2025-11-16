import { useEffect, useState } from 'react';
import {
  Container,
  Title,
  Paper,
  Stack,
  Text,
  Group,
  Button,
  Loader,
  Center,
  Alert,
  Badge,
} from '@mantine/core';
import { useAuth } from '../providers/AuthProvider';
import { useAuthStore } from '@application/store/authStore';
import { User } from '@domain/entities/User';

export const ProfilePage = () => {
  const { getCurrentUserUseCase } = useAuth();
  const { user: storeUser } = useAuthStore();
  const [user, setUser] = useState<User | null>(storeUser);
  const [loading, setLoading] = useState(!storeUser);
  const [error, setError] = useState<string | null>(null);

  const loadUser = async () => {
    setLoading(true);
    setError(null);
    try {
      const userData = await getCurrentUserUseCase.execute();
      setUser(userData);
      useAuthStore.getState().setUser(userData);
    } catch (err: unknown) {
      const errorMessage =
        err instanceof Error ? err.message : 'Не удалось загрузить информацию о пользователе';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!storeUser) {
      loadUser();
    }
  }, []);

  if (loading) {
    return (
      <Center h="50vh">
        <Loader size="lg" />
      </Center>
    );
  }

  if (error) {
    return (
      <Container size="md" py="xl">
        <Alert color="red" title="Ошибка" mb="md">
          {error}
        </Alert>
        <Button onClick={loadUser}>Попробовать снова</Button>
      </Container>
    );
  }

  if (!user) {
    return (
      <Container size="md" py="xl">
        <Alert color="yellow" title="Внимание">
          Информация о пользователе недоступна
        </Alert>
      </Container>
    );
  }

  return (
    <Container size="md" py="xl">
      <Stack gap="md">
        <Title order={1}>Профиль</Title>

        <Paper p="md" withBorder>
          <Stack gap="md">
            <Group justify="space-between" align="flex-start">
              <div>
                <Text size="lg" fw={500} mb="xs">
                  {user.username}
                </Text>
                {user.email && (
                  <Text size="sm" c="dimmed">
                    {user.email}
                  </Text>
                )}
              </div>
              <Badge color={user.is_active ? 'green' : 'red'} size="lg">
                {user.is_active ? 'Активен' : 'Неактивен'}
              </Badge>
            </Group>

            <Group gap="xs" mt="md">
              <Text size="sm" fw={500}>
                ID:
              </Text>
              <Text size="sm" c="dimmed">
                {user.id}
              </Text>
            </Group>

            {user.created_at && (
              <Group gap="xs">
                <Text size="sm" fw={500}>
                  Дата регистрации:
                </Text>
                <Text size="sm" c="dimmed">
                  {new Date(user.created_at).toLocaleDateString('ru-RU', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </Text>
              </Group>
            )}

            <Group mt="md">
              <Button onClick={loadUser} variant="outline">
                Обновить информацию
              </Button>
            </Group>
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
};

