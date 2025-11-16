import { Container, Title, Stack, Text, Paper, Button, Group } from '@mantine/core';
import { useAuthStore } from '@application/store/authStore';
import { useAuth } from '../providers/AuthProvider';
import { Link } from 'react-router-dom';

export const HomePage = () => {
  const { user, isAuthenticated } = useAuthStore();
  const { getCurrentUserUseCase } = useAuth();

  const handleRefreshUser = async () => {
    try {
      const updatedUser = await getCurrentUserUseCase.execute();
      useAuthStore.getState().setUser(updatedUser);
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  };

  return (
    <Container size="md" py="xl">
      <Stack gap="md">
        <Title order={1}>Добро пожаловать в Переплёт!</Title>
        
        {!isAuthenticated && (
          <Paper p="md" withBorder>
            <Stack gap="md">
              <Text>Вы не авторизованы. Пожалуйста, войдите в систему.</Text>
              <Group>
                <Button component={Link} to="/login" variant="filled">
                  Войти
                </Button>
                <Button component={Link} to="/register" variant="outline">
                  Зарегистрироваться
                </Button>
              </Group>
            </Stack>
          </Paper>
        )}

        {isAuthenticated && !user && (
          <Paper p="md" withBorder>
            <Stack gap="md">
              <Text>Информация о пользователе загружается...</Text>
              <Button onClick={handleRefreshUser} variant="outline">
                Обновить информацию
              </Button>
            </Stack>
          </Paper>
        )}

        {user && (
          <Paper p="md" withBorder>
            <Stack gap="xs">
              <Text size="lg" fw={500}>
                Привет, <strong>{user.username}</strong>!
              </Text>
              {user.email && (
                <Text size="sm" c="dimmed">
                  Email: {user.email}
                </Text>
              )}
              <Button onClick={handleRefreshUser} variant="subtle" size="xs" mt="xs">
                Обновить информацию
              </Button>
            </Stack>
          </Paper>
        )}
      </Stack>
    </Container>
  );
};

