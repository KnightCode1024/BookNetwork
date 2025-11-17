import { useEffect, useMemo, useState } from 'react';
import {
  Container,
  Title,
  Stack,
  Paper,
  Group,
  Button,
  TextInput,
  Loader,
  Center,
  ScrollArea,
  Table,
  Text,
  Badge,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Author } from '@domain/entities/Author';
import { AuthorRepositoryImpl } from '@infrastructure/repositories/AuthorRepositoryImpl';
import { useAuth } from '../providers/AuthProvider';
import { AuthorForm, AuthorFormValues } from '../components/AuthorForm';
import { ListAuthorsUseCase } from '@application/useCases/author/ListAuthorsUseCase';
import { CreateAuthorUseCase } from '@application/useCases/author/CreateAuthorUseCase';
import { UpdateAuthorUseCase } from '@application/useCases/author/UpdateAuthorUseCase';
import { DeleteAuthorUseCase } from '@application/useCases/author/DeleteAuthorUseCase';
import { GetAuthorByIdUseCase } from '@application/useCases/author/GetAuthorByIdUseCase';
import { AuthorPayload } from '@domain/entities/Author';

type FormMode = 'create' | 'edit';

const formatDate = (value: string) => {
  try {
    return new Intl.DateTimeFormat('ru-RU').format(new Date(value));
  } catch {
    return value;
  }
};

const mapFormToPayload = (values: AuthorFormValues): AuthorPayload => ({
  ...values,
  date_birth: new Date(values.date_birth).toISOString(),
  date_death: new Date(values.date_death).toISOString(),
});

const AUTHORS_LIMIT = 10;

export const AuthorsPage = () => {
  const { apiClient } = useAuth();

  const authorRepository = useMemo(() => new AuthorRepositoryImpl(apiClient), [apiClient]);
  const listAuthorsUseCase = useMemo(() => new ListAuthorsUseCase(authorRepository), [authorRepository]);
  const createAuthorUseCase = useMemo(() => new CreateAuthorUseCase(authorRepository), [authorRepository]);
  const updateAuthorUseCase = useMemo(() => new UpdateAuthorUseCase(authorRepository), [authorRepository]);
  const deleteAuthorUseCase = useMemo(() => new DeleteAuthorUseCase(authorRepository), [authorRepository]);
  const getAuthorByIdUseCase = useMemo(() => new GetAuthorByIdUseCase(authorRepository), [authorRepository]);

  const [authors, setAuthors] = useState<Author[]>([]);
  const [listLoading, setListLoading] = useState<boolean>(false);
  const [formMode, setFormMode] = useState<FormMode>('create');
  const [selectedAuthor, setSelectedAuthor] = useState<Author | null>(null);
  const [searchValue, setSearchValue] = useState('');
  const [activeQuery, setActiveQuery] = useState('');
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [fetchingAuthor, setFetchingAuthor] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const fetchAuthors = async (options?: { append?: boolean; offset?: number; query?: string }) => {
    const isSearch = Boolean(options?.query ?? activeQuery);
    const offset = options?.offset ?? (options?.append ? skip + AUTHORS_LIMIT : 0);
    const queryToUse = options?.query ?? activeQuery;

    setListLoading(true);
    try {
      const data = await listAuthorsUseCase.execute({
        skip: isSearch ? 0 : offset,
        limit: AUTHORS_LIMIT,
        query: queryToUse || undefined,
      });

      if (options?.append && !isSearch) {
        setAuthors((prev) => [...prev, ...data]);
      } else {
        setAuthors(data);
      }

      setHasMore(!isSearch && data.length === AUTHORS_LIMIT);
      setSkip(isSearch ? 0 : offset);
      if (options?.query !== undefined) {
        setActiveQuery(options.query);
      }
    } catch (error) {
      console.error(error);
      notifications.show({
        color: 'red',
        title: 'Не удалось загрузить авторов',
        message: 'Попробуйте обновить страницу или повторить запрос позже.',
      });
    } finally {
      setListLoading(false);
    }
  };

  useEffect(() => {
    fetchAuthors();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const resetForm = () => {
    setFormMode('create');
    setSelectedAuthor(null);
  };

  const handleFormSubmit = async (values: AuthorFormValues) => {
    const payload = mapFormToPayload(values);
    setFormSubmitting(true);

    try {
      if (formMode === 'edit' && selectedAuthor) {
        await updateAuthorUseCase.execute(selectedAuthor.id, payload);
        notifications.show({
          color: 'green',
          title: 'Автор обновлён',
          message: `${selectedAuthor.name} ${selectedAuthor.surname} обновлён.`,
        });
      } else {
        await createAuthorUseCase.execute(payload);
        notifications.show({
          color: 'green',
          title: 'Автор создан',
          message: 'Новый автор успешно добавлен.',
        });
      }
      resetForm();
      fetchAuthors({ query: activeQuery });
    } catch (error) {
      console.error(error);
      notifications.show({
        color: 'red',
        title: 'Ошибка при сохранении',
        message: 'Проверьте корректность данных и попробуйте ещё раз.',
      });
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleEditClick = async (authorId: number) => {
    setFetchingAuthor(true);
    try {
      const author = await getAuthorByIdUseCase.execute(authorId);
      setSelectedAuthor(author);
      setFormMode('edit');
    } catch (error) {
      console.error(error);
      notifications.show({
        color: 'red',
        title: 'Не удалось получить данные автора',
        message: 'Повторите попытку позже.',
      });
    } finally {
      setFetchingAuthor(false);
    }
  };

  const handleDelete = async (authorId: number) => {
    const author = authors.find((item) => item.id === authorId);
    if (!author) {
      return;
    }
    const confirmed = window.confirm(`Удалить автора ${author.name} ${author.surname}?`);
    if (!confirmed) {
      return;
    }
    setDeletingId(authorId);
    try {
      await deleteAuthorUseCase.execute(authorId);
      notifications.show({
        color: 'teal',
        title: 'Автор удалён',
        message: `${author.name} ${author.surname} был удалён.`,
      });
      if (selectedAuthor?.id === authorId) {
        resetForm();
      }
      fetchAuthors({ query: activeQuery });
    } catch (error) {
      console.error(error);
      notifications.show({
        color: 'red',
        title: 'Ошибка удаления',
        message: 'Не удалось удалить автора. Попробуйте позже.',
      });
    } finally {
      setDeletingId(null);
    }
  };

  const handleSearch = () => {
    fetchAuthors({ query: searchValue.trim() });
  };

  const handleResetSearch = () => {
    setSearchValue('');
    fetchAuthors({ query: '' });
  };

  const handleLoadMore = () => {
    fetchAuthors({ append: true, offset: skip + AUTHORS_LIMIT });
  };

  const formInitialValues =
    formMode === 'edit' && selectedAuthor
      ? {
        name: selectedAuthor.name,
        surname: selectedAuthor.surname,
        patronymic: selectedAuthor.patronymic,
        bio: selectedAuthor.bio,
        date_birth: selectedAuthor.date_birth,
        date_death: selectedAuthor.date_death,
      }
      : undefined;

  return (
    <Container size="xl" py="xl">
      <Stack gap="xl">
        <Title order={1}>Управление авторами</Title>

        <Paper withBorder p="lg" shadow="sm">
          <Stack gap="md">
            <Title order={3}>Поиск авторов</Title>
            <Group align="flex-end">
              <TextInput
                label="Имя или фамилия"
                placeholder="Введите поисковый запрос"
                value={searchValue}
                onChange={(event) => setSearchValue(event.currentTarget.value)}
                style={{ flexGrow: 1 }}
              />
              <Button onClick={handleSearch} loading={listLoading && Boolean(searchValue.trim())}>
                Найти
              </Button>
              <Button variant="default" onClick={handleResetSearch} disabled={!activeQuery && !searchValue}>
                Сбросить
              </Button>
              <Button variant="light" onClick={() => fetchAuthors({ query: activeQuery })} loading={listLoading}>
                Обновить
              </Button>
            </Group>
          </Stack>
        </Paper>

        <Paper withBorder p="lg" shadow="sm">
          <Stack gap="md">
            <Group justify="space-between">
              <Title order={3}>Список авторов</Title>
              <Badge color={activeQuery ? 'grape' : 'blue'} variant="light">
                {activeQuery ? 'Режим поиска' : 'Полный список'}
              </Badge>
            </Group>

            <ScrollArea>
              {listLoading && authors.length === 0 ? (
                <Center py="xl">
                  <Loader />
                </Center>
              ) : authors.length === 0 ? (
                <Center py="xl">
                  <Text c="dimmed">Авторы не найдены</Text>
                </Center>
              ) : (
                <Table striped highlightOnHover withTableBorder>
                  <Table.Thead>
                    <Table.Tr>
                      <Table.Th>ID</Table.Th>
                      <Table.Th>Имя</Table.Th>
                      <Table.Th>Период жизни</Table.Th>
                      <Table.Th>Биография</Table.Th>
                      <Table.Th />
                    </Table.Tr>
                  </Table.Thead>
                  <Table.Tbody>
                    {authors.map((author) => (
                      <Table.Tr key={author.id}>
                        <Table.Td>{author.id}</Table.Td>
                        <Table.Td>
                          <Stack gap={0} style={{ maxWidth: 200 }}>
                            <Text fw={600}>
                              {author.name} {author.surname}
                            </Text>
                            {author.patronymic && (
                              <Text size="sm" c="dimmed">
                                {author.patronymic}
                              </Text>
                            )}
                          </Stack>
                        </Table.Td>
                        <Table.Td>
                          <Stack gap={0}>
                            <Text size="sm">{formatDate(author.date_birth)}</Text>
                            <Text size="sm">{formatDate(author.date_death)}</Text>
                          </Stack>
                        </Table.Td>
                        <Table.Td>
                          <Text size="sm" lineClamp={3}>
                            {author.bio}
                          </Text>
                        </Table.Td>
                        <Table.Td>
                          <Group gap="xs" justify="flex-end">
                            <Button
                              size="xs"
                              variant="subtle"
                              onClick={() => handleEditClick(author.id)}
                              loading={fetchingAuthor && selectedAuthor?.id === author.id}
                            >
                              Редактировать
                            </Button>
                            <Button
                              size="xs"
                              color="red"
                              variant="light"
                              onClick={() => handleDelete(author.id)}
                              loading={deletingId === author.id}
                            >
                              Удалить
                            </Button>
                          </Group>
                        </Table.Td>
                      </Table.Tr>
                    ))}
                  </Table.Tbody>
                </Table>
              )}
            </ScrollArea>

            {hasMore && (
              <Button onClick={handleLoadMore} loading={listLoading} variant="default">
                Загрузить ещё
              </Button>
            )}
          </Stack>
        </Paper>

        <Paper withBorder p="lg" shadow="sm">
          <Stack gap="md">
            <Group justify="space-between">
              <Title order={3}>{formMode === 'create' ? 'Добавить автора' : 'Редактировать автора'}</Title>
              {formMode === 'edit' && (
                <Button variant="default" onClick={resetForm} disabled={formSubmitting || fetchingAuthor}>
                  Новый автор
                </Button>
              )}
            </Group>
            <AuthorForm
              initialValues={formInitialValues}
              submitLabel={formMode === 'create' ? 'Создать' : 'Сохранить'}
              loading={formSubmitting || fetchingAuthor}
              onSubmit={handleFormSubmit}
              onCancel={formMode === 'edit' ? resetForm : undefined}
            />
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
};


