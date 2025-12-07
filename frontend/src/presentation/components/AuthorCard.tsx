import { Paper, Stack, Text, Group, Badge } from '@mantine/core';
import { Author } from '@domain/entities/Author';

interface AuthorCardProps {
  author: Author;
  onClick?: () => void;
}

const formatDate = (value: string) => {
  try {
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(new Date(value));
  } catch {
    return value;
  }
};

export const AuthorCard = ({ author, onClick }: AuthorCardProps) => {
  const fullName = `${author.name} ${author.surname}${author.patronymic ? ` ${author.patronymic}` : ''}`;
  const birthDate = formatDate(author.date_birth);
  const deathDate = formatDate(author.date_death);
  const lifespan = `${birthDate} - ${deathDate}`;

  return (
    <Paper
      p="md"
      withBorder
      shadow="sm"
      radius="xs"
      style={{
        cursor: onClick ? 'pointer' : 'default',
        height: '100%',
        borderColor: '#8b4513',
        borderWidth: '2px',
        borderStyle: 'double',
        backgroundColor: '#fef9e7',
      }}
      onClick={onClick}
    >
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <Stack gap={4}>
            <Text
              fw={700}
              size="lg"
              c="#8b4513"
              style={{
                fontFamily: '"Times New Roman", "Georgia", "Times", serif',
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
            >
              {fullName}
            </Text>
            <Text
              size="sm"
              c="#654321"
              style={{ fontFamily: '"Times New Roman", "Georgia", "Times", serif' }}
            >
              {lifespan}
            </Text>
          </Stack>
          <Badge
            variant="light"
            style={{
              border: '1px solid #8b4513',
              color: '#8b4513',
              fontFamily: '"Times New Roman", "Georgia", "Times", serif',
            }}
          >
            ID: {author.id}
          </Badge>
        </Group>

        {author.bio && (
          <Text
            size="sm"
            lineClamp={4}
            c="#654321"
            style={{
              fontFamily: '"Times New Roman", "Georgia", "Times", serif',
              lineHeight: '1.6',
            }}
          >
            {author.bio}
          </Text>
        )}
      </Stack>
    </Paper>
  );
};

