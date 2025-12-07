import { Text, Group, Anchor, Box } from '@mantine/core';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Box
      py="md"
      px="xl"
      style={{
        borderTop: '3px double #8b4513',
        backgroundColor: '#fef9e7',
        backgroundImage: `
          repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(139, 69, 19, 0.05) 2px,
            rgba(139, 69, 19, 0.05) 4px
          )
        `,
        width: '100%',
        maxWidth: '100%',
      }}
    >
      <Group justify="space-between" align="center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Text size="sm" c="#8b4513" style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}>
          © {currentYear} Переплёт. Все права защищены.
        </Text>
        <Group gap="md">
          <Anchor
            href="#"
            size="sm"
            c="#8b4513"
            style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}
          >
            О проекте
          </Anchor>
          <Anchor
            href="#"
            size="sm"
            c="#8b4513"
            style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}
          >
            Контакты
          </Anchor>
        </Group>
      </Group>
    </Box>
  );
};

