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

interface RegisterFormValues {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export const RegisterPage = () => {
  const navigate = useNavigate();
  const { registerUseCase, getCurrentUserUseCase } = useAuth();
  const { setAuthenticated, setUser } = useAuthStore();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const form = useForm<RegisterFormValues>({
    initialValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validate: {
      username: (value) => (value.length < 2 ? 'Имя пользователя должно содержать минимум 2 символа' : null),
      email: (value) => (value ? (/^\S+@\S+$/.test(value) ? null : 'Неверный формат email') : null),
      password: (value) => (value.length < 6 ? 'Пароль должен содержать минимум 6 символов' : null),
      confirmPassword: (value, values) =>
        value !== values.password ? 'Пароли не совпадают' : null,
    },
  });

  const handleSubmit = async (values: RegisterFormValues) => {
    setError(null);
    setLoading(true);

    try {
      const { confirmPassword, email, ...registerData } = values;
      // Если email пустой, отправляем undefined/null вместо пустой строки
      const dataToSend = {
        ...registerData,
        email: email && email.trim() ? email.trim() : undefined,
      };
      await registerUseCase.execute(dataToSend);
      setAuthenticated(true);
      // Загружаем информацию о пользователе
      const user = await getCurrentUserUseCase.execute();
      setUser(user);
      navigate('/');
    } catch (err: unknown) {
      let errorMessage = 'Ошибка регистрации. Попробуйте снова.';
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
        Регистрация
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

            <TextInput
              label="Email"
              placeholder="Введите email"
              type="email"
              {...form.getInputProps('email')}
            />

            <PasswordInput
              label="Пароль"
              placeholder="Введите пароль"
              required
              {...form.getInputProps('password')}
            />

            <PasswordInput
              label="Подтвердите пароль"
              placeholder="Повторите пароль"
              required
              {...form.getInputProps('confirmPassword')}
            />

            <Button type="submit" fullWidth loading={loading}>
              Зарегистрироваться
            </Button>

            <Text ta="center" size="sm">
              Уже есть аккаунт?{' '}
              <Anchor component={Link} to="/login">
                Войти
              </Anchor>
            </Text>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
};

