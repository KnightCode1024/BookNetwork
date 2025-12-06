import { useEffect } from 'react';
import { useForm } from '@mantine/form';
import { Stack, TextInput, Textarea, Group, Button } from '@mantine/core';

export interface AuthorFormValues {
  name: string;
  surname: string;
  patronymic: string;
  bio: string;
  date_birth: string;
  date_death: string;
}

const mapDateToInput = (value?: string) => {
  if (!value) {
    return '';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  return date.toISOString().slice(0, 10);
};

interface AuthorFormProps {
  initialValues?: Partial<AuthorFormValues>;
  submitLabel: string;
  loading?: boolean;
  onSubmit: (values: AuthorFormValues) => void | Promise<void>;
  onCancel?: () => void;
}

const defaultValues: AuthorFormValues = {
  name: '',
  surname: '',
  patronymic: '',
  bio: '',
  date_birth: '',
  date_death: '',
};

export const AuthorForm = ({ initialValues, submitLabel, loading, onSubmit, onCancel }: AuthorFormProps) => {
  const form = useForm<AuthorFormValues>({
    initialValues: defaultValues,
    validate: {
      name: (value) => (value.trim().length < 2 ? 'Имя должно содержать минимум 2 символа' : null),
      surname: (value) => (value.trim().length < 2 ? 'Фамилия должна содержать минимум 2 символа' : null),
      bio: (value) => (value.trim().length < 10 ? 'Биография должна быть более развёрнутой' : null),
      date_birth: (value) => (!value ? 'Дата рождения обязательна' : null),
      date_death: (value, values) => {
        if (!value) {
          return 'Дата смерти обязательна';
        }
        if (value && values.date_birth && value < values.date_birth) {
          return 'Дата смерти не может быть раньше даты рождения';
        }
        return null;
      },
    },
  });

  useEffect(() => {
    if (initialValues) {
      form.setValues({
        ...defaultValues,
        ...initialValues,
        date_birth: mapDateToInput(initialValues.date_birth),
        date_death: mapDateToInput(initialValues.date_death),
      });
    } else {
      form.setValues(defaultValues);
    }
  }, [initialValues]);

  return (
    <form onSubmit={form.onSubmit(onSubmit)}>
      <Stack gap="sm">
        <Group grow>
          <TextInput label="Имя" placeholder="Александр" required {...form.getInputProps('name')} />
          <TextInput label="Фамилия" placeholder="Пушкин" required {...form.getInputProps('surname')} />
        </Group>

        <TextInput label="Отчество" placeholder="Сергеевич" {...form.getInputProps('patronymic')} />

        <Group grow>
          <TextInput type="date" label="Дата рождения" required {...form.getInputProps('date_birth')} />
          <TextInput type="date" label="Дата смерти" required {...form.getInputProps('date_death')} />
        </Group>

        <Textarea
          label="Биография"
          minRows={4}
          autosize
          placeholder="Краткое описание жизни и творчества..."
          {...form.getInputProps('bio')}
        />

        <Group justify="flex-end">
          {onCancel && (
            <Button variant="default" onClick={onCancel} disabled={loading}>
              Отмена
            </Button>
          )}
          <Button type="submit" loading={loading}>
            {submitLabel}
          </Button>
        </Group>
      </Stack>
    </form>
  );
};






