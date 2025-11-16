import { Link } from 'react-router-dom';
import {
  Container,
  Group,
  Button,
  Text,
  Menu,
  Avatar,
  Burger,
  Drawer,
  Stack,
  Box,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { useAuth } from '../providers/AuthProvider';
import { useAuthStore } from '@application/store/authStore';

export const Header = () => {
  const { logoutUseCase } = useAuth();
  const { isAuthenticated, user } = useAuthStore();
  const [opened, { toggle, close }] = useDisclosure(false);

  const handleLogout = async () => {
    await logoutUseCase.execute();
    close();
  };

  return (
    <Box h={60} px="md" style={{ borderBottom: '1px solid var(--mantine-color-gray-3)' }}>
      <Container size="xl" h="100%">
        <Group h="100%" justify="space-between">
          {/* Логотип/Название */}
          <Text
            component={Link}
            to="/"
            fw={700}
            size="xl"
            c="blue"
            style={{ textDecoration: 'none' }}
          >
            BookNetwork
          </Text>

          {/* Desktop Navigation */}
          <Group visibleFrom="sm" gap="xs">
            {isAuthenticated ? (
              <>
                <Menu shadow="md" width={200}>
                  <Menu.Target>
                    <Button variant="subtle" leftSection={<Avatar size="sm" radius="xl" />}>
                      {user?.username || 'Пользователь'}
                    </Button>
                  </Menu.Target>
                  <Menu.Dropdown>
                    <Menu.Label>Аккаунт</Menu.Label>
                    {user?.email && <Menu.Item disabled>{user.email}</Menu.Item>}
                    <Menu.Divider />
                    <Menu.Item component={Link} to="/profile">
                      Профиль
                    </Menu.Item>
                    <Menu.Divider />
                    <Menu.Item color="red" onClick={handleLogout}>
                      Выйти
                    </Menu.Item>
                  </Menu.Dropdown>
                </Menu>
              </>
            ) : (
              <>
                <Button variant="default" component={Link} to="/login">
                  Вход
                </Button>
                <Button component={Link} to="/register">
                  Регистрация
                </Button>
              </>
            )}
          </Group>

          {/* Mobile Burger */}
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
        </Group>
      </Container>

      {/* Mobile Drawer */}
      <Drawer opened={opened} onClose={close} title="Меню" position="right">
        <Stack gap="md">
          {isAuthenticated ? (
            <>
              <Text fw={500}>Привет, {user?.username || 'Пользователь'}!</Text>
              {user?.email && <Text size="sm" c="dimmed">{user.email}</Text>}
              <Button variant="default" fullWidth component={Link} to="/profile" onClick={close}>
                Профиль
              </Button>
              <Button color="red" fullWidth onClick={handleLogout}>
                Выйти
              </Button>
            </>
          ) : (
            <>
              <Button variant="default" fullWidth component={Link} to="/login" onClick={close}>
                Вход
              </Button>
              <Button fullWidth component={Link} to="/register" onClick={close}>
                Регистрация
              </Button>
            </>
          )}
        </Stack>
      </Drawer>
    </Box>
  );
};

