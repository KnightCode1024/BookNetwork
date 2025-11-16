import { Container, Text, Group, Anchor } from '@mantine/core';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Container size="xl" py="md" style={{ borderTop: '1px solid var(--mantine-color-gray-3)' }}>
      <Group justify="space-between" align="center">
        <Text size="sm" c="dimmed">
          © {currentYear} Переплёт. Все права защищены.
        </Text>
        <Group gap="md">
          <Anchor href="#" size="sm" c="dimmed">
            О проекте
          </Anchor>
          <Anchor href="#" size="sm" c="dimmed">
            Контакты
          </Anchor>
        </Group>
      </Group>
    </Container>
  );
};

