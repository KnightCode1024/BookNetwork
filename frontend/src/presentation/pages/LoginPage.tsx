import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container,
  Paper,
  Title,
  TextInput,
  PasswordInput,
  Button,
  Stack,
  Text,
  Anchor,
  Alert,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAuth } from '../providers/AuthProvider';
import { useAuthStore } from '@application/store/authStore';

interface LoginFormValues {
  username: string;
  password: string;
}

export const LoginPage = () => {
  const navigate = useNavigate();
  const { loginUseCase, getCurrentUserUseCase } = useAuth();
  const { setAuthenticated, setUser } = useAuthStore();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const form = useForm<LoginFormValues>({
    initialValues: {
      username: '',
      password: '',
    },
    validate: {
      username: (value) => (value.length < 2 ? 'Имя пользователя должно содержать минимум 2 символа' : null),
      password: (value) => (value.length < 6 ? 'Пароль должен содержать минимум 6 символов' : null),
    },
  });

  const handleSubmit = async (values: LoginFormValues) => {
    setError(null);
    setLoading(true);

    try {
      await loginUseCase.execute(values);
      setAuthenticated(true);
      // Загружаем информацию о пользователе
      const user = await getCurrentUserUseCase.execute();
      setUser(user);
      navigate('/');
    } catch (err: unknown) {
      let errorMessage = 'Ошибка входа. Проверьте данные.';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (err && typeof err === 'object' && 'response' in err) {
        // Обработка Axios ошибок
        const axiosError = err as { response?: { data?: { detail?: string | string[] } } };
        if (axiosError.response?.data?.detail) {
          const detail = axiosError.response.data.detail;
          errorMessage = Array.isArray(detail) ? detail.join(', ') : detail;
        }
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title ta="center" mb="xl">
        Вход в систему
      </Title>

      <Paper withBorder shadow="md" p={30} radius="md">
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack gap="md">
            {error && (
              <Alert color="red" title="Ошибка">
                {error}
              </Alert>
            )}

            <TextInput
              label="Имя пользователя"
              placeholder="Введите имя пользователя"
              required
              {...form.getInputProps('username')}
            />

            <PasswordInput
              label="Пароль"
              placeholder="Введите пароль"
              required
              {...form.getInputProps('password')}
            />

            <Button type="submit" fullWidth loading={loading}>
              Войти
            </Button>

            <Text ta="center" size="sm">
              Нет аккаунта?{' '}
              <Anchor component={Link} to="/register">
                Зарегистрироваться
              </Anchor>
            </Text>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
};

